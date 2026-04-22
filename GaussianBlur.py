import torch
import math
from torch.nn import functional as F

class GaussianBlur:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "radius": ("FLOAT", {"default": 25.0, "min": 0.0, "max": 100.0, "step": 0.5}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "blur"
    CATEGORY = "image/filters"

    def gaussian_kernel(self, sigma, device):
        if sigma < 0.1:
            sigma = 0.1
        size = int(2 * math.ceil(3 * sigma) + 1)
        if size < 3:
            size = 3
        center = size // 2
        kernel = torch.zeros(size, dtype=torch.float32, device=device)
        for i in range(size):
            x = i - center
            kernel[i] = math.exp(- (x * x) / (2 * sigma * sigma))
        kernel = kernel / kernel.sum()
        return kernel

    def blur_image(self, img, sigma):
        if sigma <= 0.0:
            return img
        device = img.device
        kernel = self.gaussian_kernel(sigma, device)
        # 计算需要填充的边界大小
        pad = kernel.shape[0] // 2
        # img: (H,W,C) -> (1,C,H,W)
        img_perm = img.permute(2, 0, 1).unsqueeze(0)  # (1, C, H, W)
        # 使用反射填充，避免黑边
        img_padded = F.pad(img_perm, (pad, pad, pad, pad), mode='reflect')
        C = img_perm.shape[1]
        # 构建卷积核 (C,1,1,size) 和 (C,1,size,1)
        kernel_h = kernel.view(1, 1, 1, -1).repeat(C, 1, 1, 1)
        kernel_v = kernel.view(1, 1, -1, 1).repeat(C, 1, 1, 1)
        # 先水平卷积，再垂直卷积（无需额外padding，因为已经手动填充过）
        tmp = F.conv2d(img_padded, kernel_h, groups=C)
        blurred_padded = F.conv2d(tmp, kernel_v, groups=C)
        # 裁剪掉填充部分
        blurred = blurred_padded[:, :, pad:-pad, pad:-pad]
        blurred = blurred.squeeze(0).permute(1, 2, 0)
        return blurred

    def blur(self, images, radius):
        sigma = radius / 2.0
        batch = []
        for img in images:
            blurred = self.blur_image(img, sigma)
            batch.append(blurred.unsqueeze(0))
        return (torch.cat(batch, dim=0),)

NODE_CLASS_MAPPINGS = {
    "GaussianBlur": GaussianBlur,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "GaussianBlur": "Gaussian Blur (Smooth)",
}