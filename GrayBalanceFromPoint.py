import torch
import json

class GrayBalanceFromPoint:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "positive_coords": ("*", {"tooltip": "Connect PointsEditor positive_coords output"}),  # 无文本框，仅连线
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "balance_data")
    FUNCTION = "apply"
    CATEGORY = "image/color"

    def apply(self, images, positive_coords):
        # 如果 positive_coords 不是字符串，尝试转换（安全起见）
        if not isinstance(positive_coords, str):
            # 可能是 bytes 或其他类型，转为字符串
            try:
                positive_coords = str(positive_coords)
            except:
                raise ValueError("positive_coords must be a JSON string from PointsEditor")
        
        if not positive_coords or not positive_coords.strip():
            raise ValueError("positive_coords is empty. Please connect PointsEditor output.")
        
        try:
            points = json.loads(positive_coords)
            if not isinstance(points, list) or len(points) == 0:
                raise ValueError("positive_coords must be a non-empty list")
        except Exception as e:
            raise ValueError(f"Failed to parse positive_coords: {e}")

        # 取批次中的第一张图像作为参考（所有图像使用相同的增益）
        ref_img = images[0]  # (H, W, C)
        H, W, _ = ref_img.shape

        # 提取所有点的 RGB 值
        r_sum = 0.0
        g_sum = 0.0
        b_sum = 0.0
        n = len(points)
        for pt in points:
            x = pt.get("x")
            y = pt.get("y")
            if x is None or y is None:
                raise ValueError("Invalid point format, missing x or y")
            xi = min(max(x, 0), W-1)
            yi = min(max(y, 0), H-1)
            rgb = ref_img[yi, xi, :3]
            r_sum += rgb[0].item()
            g_sum += rgb[1].item()
            b_sum += rgb[2].item()

        avg_r = r_sum / n
        avg_g = g_sum / n
        avg_b = b_sum / n

        # 目标灰值：三个通道的平均值
        target_gray = (avg_r + avg_g + avg_b) / 3.0

        # 计算增益，避免除零
        eps = 1e-6
        gain_r = target_gray / (avg_r + eps)
        gain_g = target_gray / (avg_g + eps)
        gain_b = target_gray / (avg_b + eps)

        # 记录增益数据
        data = {
            "r_gain": round(gain_r, 6),
            "g_gain": round(gain_g, 6),
            "b_gain": round(gain_b, 6),
            "avg_source_rgb": [round(avg_r, 4), round(avg_g, 4), round(avg_b, 4)],
            "target_gray": round(target_gray, 4),
            "points_count": n
        }
        data_json = json.dumps(data, indent=2)

        # 应用到所有输入图像
        batch = []
        for img in images:
            corrected = img.clone()
            corrected[..., 0] = torch.clamp(img[..., 0] * gain_r, 0.0, 1.0)
            corrected[..., 1] = torch.clamp(img[..., 1] * gain_g, 0.0, 1.0)
            corrected[..., 2] = torch.clamp(img[..., 2] * gain_b, 0.0, 1.0)
            batch.append(corrected.unsqueeze(0))

        return (torch.cat(batch, dim=0), data_json)

NODE_CLASS_MAPPINGS = {
    "GrayBalanceFromPoint": GrayBalanceFromPoint,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "GrayBalanceFromPoint": "Gray Balance from Point (Multi-point)",
}
