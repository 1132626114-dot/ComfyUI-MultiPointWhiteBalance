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
git clone https://github.com/yourusername/ComfyUI-MultiPointWhiteBalance.git
Restart ComfyUI.

📖 Usage Guide
Prerequisite
KJNodes custom node pack must be installed (provides the PointsEditor node).

Workflow Overview
Create a blurred copy of your image (only needed for noisy backgrounds – see below).

On the image used for sampling (original or blurred), use PointsEditor to add several green points on the background (white/neutral areas).

Connect the points to Gray Balance from Point (or Exposure Match from Point) to compute gains.

Feed the computed JSON gains together with the original (sharp) image into the corresponding Apply… node.

Use a segmentation node (e.g., BiRefNet) to extract a foreground mask, and composite the corrected background with the original foreground.

Two Common Use Cases
Group A – Normal White Background (already clean)
No blur is used. The original image is directly fed into PointsEditor to select sample points on the background.

Gains (white balance or exposure) are computed from the original image and then applied to the same original image.

A segmentation node extracts the foreground mask, and the corrected background is composited with the untouched foreground.

This preserves sharp product details while evening out minor background color casts.

Group B – Noisy / Stained White Background
A strong Gaussian blur is applied first (e.g., radius 15–40) to suppress color noise, dust spots, or uneven illumination.

The blurred image is used only for point selection and gain calculation – the gains are then applied to the original sharp image.

A foreground mask (e.g., from BiRefNet) ensures that only the background is corrected, leaving the product completely unchanged.

This method effectively cleans heavily contaminated backgrounds while retaining full product detail.

Parameters
Gray Balance from Point
positive_coords (must be connected to PointsEditor output)

Automatically computes the average RGB of all points and shifts it to neutral gray (R = G = B = average).

Outputs a JSON string containing r_gain, g_gain, b_gain, etc.

Exposure Match from Point
positive_coords (same as above)

target_luminance – desired brightness of the sampled points (0 = black, 1 = white). Default 0.9647 ≈ RGB 246.

Outputs a JSON string containing a single gain value.

Apply White Balance Gain / Apply Exposure Gain
images – the original sharp image.

balance_data / exposure_data – connect the JSON output from the corresponding compute node.

🔧 Notes
Sample points should be chosen from uniform, non‑highlight, non‑shadow areas of the background.

If the background has uneven illumination, a single gain may not make every point reach the target, but the average will match.

For heavily stained or noisy backgrounds, always use a strong blur when computing gains.

The output images from the compute nodes (Gray Balance from Point etc.) are only for preview; the final correction is applied via the Apply… nodes.

🎨 Advanced: Using a Mask for Background‑Only Correction
If you need to brighten or color‑correct only the background while preserving the original foreground (product), you can incorporate a mask. For example:

Use a segmentation node (e.g., 🔥BiRefNet, Segment Anything, or any other matting tool) to extract a mask of the foreground.

Invert the mask to obtain a background mask.

Apply the white balance or exposure gain using a Composite or Apply Mask workflow:

Keep the foreground unchanged.

Apply the correction only to the background region (using the background mask).

This approach is especially useful when the product itself contains white areas that should not be altered. You are free to choose any segmentation node that works well with your images.

📜 License
MIT License

🙏 Acknowledgements
Thanks to KJNodes for providing the PointsEditor node.

Inspired by real‑world needs in e‑commerce photography white‑balance correction.

📧 Contact
Please open an issue on GitHub for questions or suggestions.

ComfyUI 多点平均白平衡工具包
为电商产品图设计的自定义节点包。通过对图像的模糊副本手动选点，计算白平衡或曝光增益，再应用到原始清晰图像上，实现精准的颜色与亮度校正。

✨ 特性
无需编程 – 使用 KJNodes 的 PointsEditor 节点可视化选点。

多点平均 – 自动计算多个采样点的平均 RGB 或亮度，提高稳定性。

背景优先 – 专为白色/纯色背景优化，避免前景白色物体干扰。

两步流程 – 在模糊图上计算增益，应用到原始清晰图，既校正背景又保留产品细节。

白平衡与曝光分离 – 独立节点分别处理色偏和整体亮度。

📦 节点列表
节点名称	分类	功能描述
Gaussian Blur (Smooth)	image/filters	简单高斯模糊。用于消除白色背景中的彩噪或不均匀。可替换为其他模糊节点。
Gray Balance from Point (Multi‑point)	image/color	基于模糊图像上的采样点计算白平衡增益（r_gain, g_gain, b_gain），输出 JSON 数据。
Apply White Balance Gain	image/color	将计算好的白平衡增益应用到原始清晰图像。
Exposure Match from Point	image/color	基于模糊图像上的采样点计算曝光增益（单一亮度乘数），输出 JSON 数据。
Apply Exposure Gain	image/color	将计算好的曝光增益应用到原始清晰图像。
🚀 安装
方法一：ComfyUI Manager（推荐）
打开 ComfyUI → 点击 Manager → Install Custom Nodes

搜索 ComfyUI MultiPoint White Balance

点击 Install，重启 ComfyUI

方法二：手动安装
bash
cd ComfyUI/custom_nodes
git clone https://github.com/你的用户名/ComfyUI-MultiPointWhiteBalance.git
重启 ComfyUI。

📖 使用指南
前置要求
必须安装 KJNodes 插件（提供 PointsEditor 节点）。

工作流概述
创建图像的模糊副本（仅当背景有噪声时才需要 – 见下文）。

在用于采样的图像（原始或模糊）上，用 PointsEditor 在背景（白色/中性色区域）添加多个绿色点。

将点坐标连接到 Gray Balance from Point（或 Exposure Match from Point）计算增益。

将计算出的 JSON 增益与 原始清晰图像 一起输入对应的 Apply… 节点。

使用分割节点（例如 BiRefNet）提取前景蒙版，将校正后的背景与原始前景合成。

两个典型使用场景
组 A – 正常白底图（背景干净）
不使用模糊。原始图像直接进入 PointsEditor 进行背景选点。

白平衡或曝光增益直接从原始图像计算，并应用到同一原始图像。

使用分割节点提取前景蒙版，将校正后的背景与未改动的前景合成。

这样既保留了产品的锐利细节，又能修正背景的轻微色偏。

组 B – 有噪声/被污染的白底图
先使用较强的高斯模糊（例如半径 15–40）以压制彩噪、灰尘或不均匀光照。

模糊图像仅用于选点和增益计算，然后将增益应用到原始清晰图像。

通过前景蒙版（例如 BiRefNet）确保仅校正背景，产品完全不变。

这种方法能有效清洁严重污染的背景，同时保持产品细节完整。

参数说明
Gray Balance from Point
positive_coords（必须连接 PointsEditor 输出）

自动计算所有采样点的平均 RGB，并将其调整为中性灰（R = G = B = 平均值）。

输出 JSON 字符串，包含 r_gain, g_gain, b_gain 等。

Exposure Match from Point
positive_coords（同上）

target_luminance – 期望采样点达到的亮度（0=黑，1=白）。默认 0.9647 ≈ RGB 246。

输出 JSON 字符串，包含单个 gain 值。

Apply White Balance Gain / Apply Exposure Gain
images – 原始清晰图像。

balance_data / exposure_data – 连接对应计算节点输出的 JSON 数据。

🔧 注意事项
采样点应选择背景中均匀、无高光、无阴影的区域。

如果背景本身明暗不均，单一增益可能无法让所有点都达到目标值，但平均亮度会达标。

对于严重污染或有噪声的背景，计算增益时必须使用较强的高斯模糊。

计算节点（如 Gray Balance from Point）输出的图像仅用于预览；最终校正通过 Apply… 节点完成。

🎨 进阶用法：使用蒙版单独调整背景
如果你需要仅提亮或校正背景，而保持前景（产品）完全不改变，可以引入蒙版。例如：

使用分割节点（如 🔥BiRefNet、Segment Anything 或其他抠图工具）提取前景蒙版。

反转蒙版得到背景蒙版。

在应用增益时，将白平衡或曝光校正仅作用于背景蒙版覆盖的区域，前景保持不变。

这一技巧在产品本身含有白色区域时尤其有用，可避免误校正。你可以选择任何合适的分割节点来完成这一任务。

📜 许可证
MIT 许可证

🙏 致谢
感谢 KJNodes 提供的 PointsEditor 节点。

灵感来源于电商摄影中白平衡校正的实际需求。