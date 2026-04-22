markdown
# ComfyUI MultiPoint White Balance

A custom node pack for e‑commerce product photography. It provides precise white balance and exposure correction by manually selecting multiple points on a blurred copy of the image, then applying the calculated gains to the original sharp image.

---

## ✨ Features

- **No coding required** – visual point selection using `PointsEditor` (from KJNodes).
- **Multi‑point averaging** – robust correction by averaging RGB or luminance from several sample points.
- **Background‑oriented** – optimized for white/neutral backgrounds, avoiding interference from white foreground objects.
- **Two‑step workflow** – compute gains on a blurred copy (to suppress noise/texture), then apply them to the original sharp image.
- **Separate white balance & exposure** – independent nodes for color cast correction and overall brightness adjustment.

## 📦 Nodes

| Node Name | Category | Description |
| :--- | :--- | :--- |
| `Gaussian Blur (Smooth)` | `image/filters` | Simple Gaussian blur. Useful for removing color noise or unevenness from white backgrounds. You may replace it with any other blur node. |
| `Gray Balance from Point (Multi‑point)` | `image/color` | Compute white balance gains (r_gain, g_gain, b_gain) from points on a blurred image. Outputs JSON data. |
| `Apply White Balance Gain` | `image/color` | Apply previously computed white balance gains to the original (sharp) image. |
| `Exposure Match from Point` | `image/color` | Compute exposure gain (single luminance multiplier) from points on a blurred image. Outputs JSON data. |
| `Apply Exposure Gain` | `image/color` | Apply previously computed exposure gain to the original (sharp) image. |

## 🚀 Installation

### Method 1 – ComfyUI Manager (recommended)
1. Open ComfyUI → click `Manager` → `Install Custom Nodes`
2. Search for `ComfyUI MultiPoint White Balance`
3. Click Install, then restart ComfyUI.

### Method 2 – Manual
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/MengYe-Z/ComfyUI-MultiPointWhiteBalance.git
Restart ComfyUI.

## 📖 Usage Guide

### Prerequisite
- **KJNodes** custom node pack must be installed (provides the `PointsEditor` node).

### Workflow Overview
1. Create a blurred copy of your image (only needed for noisy backgrounds – see below).
2. On the image used for sampling (original or blurred), use `PointsEditor` to add several green points on the background (white/neutral areas).
3. Connect the points to `Gray Balance from Point` (or `Exposure Match from Point`) to compute gains.
4. Feed the computed JSON gains together with the **original (sharp) image** into the corresponding `Apply…` node.
5. Use a segmentation node (e.g., BiRefNet) to extract a foreground mask, and composite the corrected background with the original foreground.

### Two Common Use Cases

#### Group A – Normal White Background (already clean)
- **No blur is used**. The original image is directly fed into `PointsEditor` to select sample points on the background.
- Gains (white balance or exposure) are computed from the original image and then applied to the same original image.
- A segmentation node extracts the foreground mask, and the corrected background is composited with the untouched foreground.
- This preserves sharp product details while evening out minor background color casts.

#### Group B – Noisy / Stained White Background
- **A strong Gaussian blur is applied first** (e.g., radius 15–40) to suppress color noise, dust spots, or uneven illumination.
- The blurred image is used **only for point selection and gain calculation** – the gains are then applied to the **original sharp image**.
- A foreground mask (e.g., from BiRefNet) ensures that only the background is corrected, leaving the product completely unchanged.
- This method effectively cleans heavily contaminated backgrounds while retaining full product detail.

### Parameters

#### `Gray Balance from Point`
- `positive_coords` (must be connected to `PointsEditor` output)
- Automatically computes the average RGB of all points and shifts it to neutral gray (R = G = B = average).
- Outputs a JSON string containing `r_gain`, `g_gain`, `b_gain`, etc.

#### `Exposure Match from Point`
- `positive_coords` (same as above)
- `target_luminance` – desired brightness of the sampled points (0 = black, 1 = white). Default `0.9647` ≈ RGB 246.
- Outputs a JSON string containing a single `gain` value.

#### `Apply White Balance Gain` / `Apply Exposure Gain`
- `images` – the **original sharp** image.
- `balance_data` / `exposure_data` – connect the JSON output from the corresponding compute node.

## 🔧 Notes

- Sample points should be chosen from **uniform, non‑highlight, non‑shadow** areas of the background.
- If the background has uneven illumination, a single gain may not make every point reach the target, but the **average** will match.
- For heavily stained or noisy backgrounds, always use a **strong blur** when computing gains.
- The output images from the compute nodes (`Gray Balance from Point` etc.) are only for **preview**; the final correction is applied via the `Apply…` nodes.

### 🎨 Advanced: Using a Mask for Background‑Only Correction

If you need to brighten or color‑correct **only the background** while preserving the original foreground (product), you can incorporate a mask. For example:

1. Use a segmentation node (e.g., 🔥BiRefNet, `Segment Anything`, or any other matting tool) to extract a mask of the foreground.
2. Invert the mask to obtain a **background mask**.
3. Apply the white balance or exposure gain using a `Composite` or `Apply Mask` workflow:  
   - Keep the foreground unchanged.  
   - Apply the correction only to the background region (using the background mask).

This approach is especially useful when the product itself contains white areas that should not be altered. You are free to choose any segmentation node that works well with your images.

## 📜 License

MIT License

## 🙏 Acknowledgements

- Thanks to **KJNodes** for providing the `PointsEditor` node.
- Inspired by real‑world needs in e‑commerce photography white‑balance correction.

## 📧 Contact

Please open an issue on GitHub for questions or suggestions.