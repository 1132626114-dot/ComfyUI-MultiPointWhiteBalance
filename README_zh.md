markdown
# ComfyUI 多点平均白平衡工具包

为电商产品图设计的自定义节点包。通过对图像的模糊副本手动选点，计算白平衡或曝光增益，再应用到原始清晰图像上，实现精准的颜色与亮度校正。

---

## ✨ 特性

- **无需编程** – 使用 KJNodes 的 `PointsEditor` 节点可视化选点。
- **多点平均** – 自动计算多个采样点的平均 RGB 或亮度，提高稳定性。
- **背景优先** – 专为白色/纯色背景优化，避免前景白色物体干扰。
- **两步流程** – 在模糊图上计算增益，应用到原始清晰图，既校正背景又保留产品细节。
- **白平衡与曝光分离** – 独立节点分别处理色偏和整体亮度。

## 📦 节点列表

| 节点名称 | 分类 | 功能描述 |
| :--- | :--- | :--- |
| `Gaussian Blur (Smooth)` | `image/filters` | 简单高斯模糊。用于消除白色背景中的彩噪或不均匀。可替换为其他模糊节点。 |
| `Gray Balance from Point (Multi‑point)` | `image/color` | 基于模糊图像上的采样点计算白平衡增益（r_gain, g_gain, b_gain），输出 JSON 数据。 |
| `Apply White Balance Gain` | `image/color` | 将计算好的白平衡增益应用到原始清晰图像。 |
| `Exposure Match from Point` | `image/color` | 基于模糊图像上的采样点计算曝光增益（单一亮度乘数），输出 JSON 数据。 |
| `Apply Exposure Gain` | `image/color` | 将计算好的曝光增益应用到原始清晰图像。 |

## 🚀 安装

### 方法一：通过 ComfyUI Manager（推荐）
1. 打开 ComfyUI → 点击 `Manager` → `Install Custom Nodes`
2. 搜索 `ComfyUI MultiPoint White Balance`
3. 点击 Install，重启 ComfyUI

### 方法二：手动安装
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/MengYe-Z/ComfyUI-MultiPointWhiteBalance.git
然后重启 ComfyUI。
```

## 📖 使用指南

### 前置要求
- 必须安装 **KJNodes** 插件（提供 `PointsEditor` 节点）。

### 工作流概述
1. 创建图像的模糊副本（仅当背景有噪声时才需要 – 见下文）。
2. 在用于采样的图像（原始或模糊）上，用 `PointsEditor` 在背景（白色/中性色区域）添加多个绿色点。
3. 将点坐标连接到 `Gray Balance from Point`（或 `Exposure Match from Point`）计算增益。
4. 将计算出的 JSON 增益与 **原始清晰图像** 一起输入对应的 `Apply…` 节点。
5. 使用分割节点（例如 BiRefNet）提取前景蒙版，将校正后的背景与原始前景合成。

### 两个典型使用场景

#### 组 A – 正常白底图（背景干净）
- **不使用模糊**。原始图像直接进入 `PointsEditor` 进行背景选点。
- 白平衡或曝光增益直接从原始图像计算，并应用到同一原始图像。
- 使用分割节点提取前景蒙版，将校正后的背景与未改动的前景合成。
- 这样既保留了产品的锐利细节，又能修正背景的轻微色偏。

#### 组 B – 有噪声/被污染的白底图
- **先使用较强的高斯模糊**（例如半径 15–40）以压制彩噪、灰尘或不均匀光照。
- 模糊图像**仅用于选点和增益计算**，然后将增益应用到**原始清晰图像**。
- 通过前景蒙版（例如 BiRefNet）确保仅校正背景，产品完全不变。
- 这种方法能有效清洁严重污染的背景，同时保持产品细节完整。

### 参数说明

#### `Gray Balance from Point`
- `positive_coords`（必须连接 `PointsEditor` 输出）
- 自动计算所有采样点的平均 RGB，并将其调整为中性灰（R = G = B = 平均值）。
- 输出 JSON 字符串，包含 `r_gain`, `g_gain`, `b_gain` 等。

#### `Exposure Match from Point`
- `positive_coords`（同上）
- `target_luminance` – 期望采样点达到的亮度（0 = 黑，1 = 白）。默认 `0.9647` ≈ RGB 246。
- 输出 JSON 字符串，包含单个 `gain` 值。

#### `Apply White Balance Gain` / `Apply Exposure Gain`
- `images` – **原始清晰图像**。
- `balance_data` / `exposure_data` – 连接对应计算节点输出的 JSON 数据。

## 🔧 注意事项

- 采样点应选择背景中**均匀、无高光、无阴影**的区域。
- 如果背景本身明暗不均，单一增益可能无法让所有点都达到目标值，但**平均亮度**会达标。
- 对于严重污染或有噪声的背景，计算增益时必须使用**较强的高斯模糊**。
- 计算节点（如 `Gray Balance from Point`）输出的图像仅用于**预览**；最终校正通过 `Apply…` 节点完成。

### 🎨 进阶用法：使用蒙版单独调整背景

如果你需要**仅提亮或校正背景**，而保持前景（产品）完全不改变，可以引入蒙版。例如：

1. 使用分割节点（如 🔥BiRefNet、`Segment Anything` 或其他抠图工具）提取前景蒙版。
2. 反转蒙版得到**背景蒙版**。
3. 在应用增益时，将白平衡或曝光校正仅作用于背景蒙版覆盖的区域，前景保持不变。

这一技巧在产品本身含有白色区域时尤其有用，可避免误校正。你可以选择任何合适的分割节点来完成这一任务。

## 📜 许可证

MIT 许可证

## 🙏 致谢

- 感谢 **KJNodes** 提供的 `PointsEditor` 节点。
- 灵感来源于电商摄影中白平衡校正的实际需求。

## 📧 联系

如有问题或建议，请在 GitHub Issues 中提出。