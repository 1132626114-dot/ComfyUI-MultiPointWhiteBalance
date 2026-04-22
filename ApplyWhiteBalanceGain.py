import torch
import json

class ApplyWhiteBalanceGain:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "balance_data": ("*", {"tooltip": "JSON string from GrayBalanceFromPoint (r_gain, g_gain, b_gain)"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply"
    CATEGORY = "image/color"

    def apply(self, images, balance_data):
        # 如果 balance_data 不是字符串，尝试转换
        if not isinstance(balance_data, str):
            try:
                balance_data = str(balance_data)
            except:
                balance_data = "{}"
        try:
            data = json.loads(balance_data)
            gain_r = data.get("r_gain", 1.0)
            gain_g = data.get("g_gain", 1.0)
            gain_b = data.get("b_gain", 1.0)
        except Exception as e:
            print(f"Error parsing balance_data: {e}")
            gain_r = gain_g = gain_b = 1.0

        batch = []
        for img in images:
            corrected = img.clone()
            corrected[..., 0] = torch.clamp(img[..., 0] * gain_r, 0.0, 1.0)
            corrected[..., 1] = torch.clamp(img[..., 1] * gain_g, 0.0, 1.0)
            corrected[..., 2] = torch.clamp(img[..., 2] * gain_b, 0.0, 1.0)
            batch.append(corrected.unsqueeze(0))

        return (torch.cat(batch, dim=0),)

NODE_CLASS_MAPPINGS = {
    "ApplyWhiteBalanceGain": ApplyWhiteBalanceGain,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ApplyWhiteBalanceGain": "Apply White Balance Gain",
}
