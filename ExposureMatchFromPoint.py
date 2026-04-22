import torch
import json

class ExposureMatchFromPoint:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "positive_coords": ("*", {"tooltip": "Connect PointsEditor positive_coords output"}),
                "target_luminance": ("FLOAT", {"default": 0.9647, "min": 0.0, "max": 1.0, "step": 0.001, "tooltip": "Target brightness for selected points (0=black, 1=white). Default 0.9647 ≈ RGB 246"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "exposure_data")
    FUNCTION = "apply"
    CATEGORY = "image/color"

    def apply(self, images, positive_coords, target_luminance=0.9647):
        # 解析坐标
        if not positive_coords or not positive_coords.strip():
            raise ValueError("positive_coords is empty. Please connect PointsEditor output.")
        if not isinstance(positive_coords, str):
            try:
                positive_coords = str(positive_coords)
            except:
                raise ValueError("positive_coords must be a JSON string")
        try:
            points = json.loads(positive_coords)
            if not isinstance(points, list) or len(points) == 0:
                raise ValueError("positive_coords must be a non-empty list")
        except Exception as e:
            raise ValueError(f"Failed to parse positive_coords: {e}")

        # 取第一张图像作为参考
        ref_img = images[0]  # (H, W, C)
        H, W, _ = ref_img.shape

        # 提取所有点的平均亮度
        l_sum = 0.0
        n = len(points)
        for pt in points:
            x = pt.get("x")
            y = pt.get("y")
            if x is None or y is None:
                raise ValueError("Invalid point format")
            xi = min(max(x, 0), W-1)
            yi = min(max(y, 0), H-1)
            rgb = ref_img[yi, xi, :3]
            l = (rgb[0] + rgb[1] + rgb[2]) / 3.0
            l_sum += l.item()
        avg_l = l_sum / n

        # 计算增益
        eps = 1e-6
        gain = target_luminance / (avg_l + eps)

        # 记录数据
        data = {
            "gain": round(gain, 6),
            "avg_luminance": round(avg_l, 4),
            "target_luminance": round(target_luminance, 4),
            "points_count": n,
        }
        data_json = json.dumps(data, indent=2)

        # 应用到所有图像
        batch = []
        for img in images:
            corrected = img.clone()
            corrected = torch.clamp(corrected * gain, 0.0, 1.0)
            batch.append(corrected.unsqueeze(0))

        return (torch.cat(batch, dim=0), data_json)

NODE_CLASS_MAPPINGS = {
    "ExposureMatchFromPoint": ExposureMatchFromPoint,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ExposureMatchFromPoint": "Exposure Match from Point",
}