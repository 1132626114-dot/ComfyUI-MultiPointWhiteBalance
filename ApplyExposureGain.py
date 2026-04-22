import torch
import json

class ApplyExposureGain:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "exposure_data": ("*", {"tooltip": "JSON string from ExposureMatchFromPoint (contains 'gain')"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply"
    CATEGORY = "image/color"

    def apply(self, images, exposure_data):
        if not isinstance(exposure_data, str):
            try:
                exposure_data = str(exposure_data)
            except:
                exposure_data = "{}"
        try:
            data = json.loads(exposure_data)
            gain = data.get("gain", 1.0)
        except Exception as e:
            print(f"Error parsing exposure_data: {e}")
            gain = 1.0

        batch = []
        for img in images:
            corrected = img.clone()
            corrected = torch.clamp(corrected * gain, 0.0, 1.0)
            batch.append(corrected.unsqueeze(0))

        return (torch.cat(batch, dim=0),)

NODE_CLASS_MAPPINGS = {
    "ApplyExposureGain": ApplyExposureGain,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ApplyExposureGain": "Apply Exposure Gain",
}
