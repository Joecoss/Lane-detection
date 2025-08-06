# Lane Detection System / 车道线检测系统

[English](#english) | [中文](#chinese)

<a name="chinese"></a>
## 中文文档

本项目针对传统车道线检测鲁棒性较差的现象，通过运用YOLOV7与DeepLabv3+的图像深度学习算法对特定数据集进行模型训练，开发了一款能调用车载摄像头来识别道路环境，并用语音告知驾驶员偏离车道，前方车距等驾驶信息的偏离预警系统，辅助驾驶员更加安全高效的行驶。

<a name="english"></a>
## English Documentation

This project addresses the poor robustness of traditional lane detection systems by developing a lane departure warning system that utilizes YOLOV7 and DeepLabv3+ deep learning algorithms. The system processes input from vehicle-mounted cameras to recognize road conditions and provides voice notifications about lane departure and vehicle distance, helping drivers navigate more safely and efficiently.

![可视化](https://user-images.githubusercontent.com/89328970/220098900-36f5d74c-816d-4b66-95ee-b54f9d7d1861.JPG)

### 环境要求 / Requirements

#### 中文
- Python 3.8 或更高版本
- CUDA 11.0 或更高版本（用于 GPU 加速，推荐）
- PyTorch >= 1.7.0
- OpenCV-Python
- 其他依赖见 requirements.txt

#### English
- Python 3.8 or higher
- CUDA 11.0 or higher (for GPU acceleration, recommended)
- PyTorch >= 1.7.0
- OpenCV-Python
- See requirements.txt for other dependencies

### 快速安装 / Quick Installation

#### 中文
1. 克隆仓库：
```bash
git clone https://github.com/Joecoss/Lane-detection.git
cd Lane-detection
```

2. 创建并激活虚拟环境（推荐）：
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

#### English
1. Clone the repository:
```bash
git clone https://github.com/Joecoss/Lane-detection.git
cd Lane-detection
```

2. Create and activate virtual environment (recommended):
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 模型权重文件下载 / Model Weights Download

#### 中文
由于体积较大，模型权重文件未直接存储在仓库中，请从 GitHub Release 页面下载：

1. yolov7 权重文件 `yolov7_weights.pth`：
   - [下载地址](https://github.com/Joecoss/Lane-detection/releases/tag/v1.0.0)
   - 下载后放置于 `Yolov7/model_data/` 目录下

2. deeplabv3+ 权重文件 `ep400-loss0.006-val_loss0.005.pth`：
   - [下载地址](https://github.com/Joecoss/Lane-detection/releases/tag/v1.0.0)
   - 下载后放置于 `deeplabv3/model_data/` 目录下

#### English
Due to their large size, model weight files are not stored directly in the repository. Please download them from the GitHub Release page:

1. yolov7 weights file `yolov7_weights.pth`:
   - [Download Link](https://github.com/Joecoss/Lane-detection/releases/tag/v1.0.0)
   - Place in the `Yolov7/model_data/` directory after downloading

2. deeplabv3+ weights file `ep400-loss0.006-val_loss0.005.pth`:
   - [Download Link](https://github.com/Joecoss/Lane-detection/releases/tag/v1.0.0)
   - Place in the `deeplabv3/model_data/` directory after downloading

### 使用说明 / Usage Instructions

#### 图形界面 / Graphical User Interface (GUI)
![image](https://user-images.githubusercontent.com/89328970/220099687-7fb6ae20-8f9e-4df9-b516-f2961db1353c.png)

#### 中文
##### 运行步骤

1. 启动图形界面：
```bash
python GUI.py
```

2. 功能说明：
   - 实时检测：点击"开始检测"按钮，将调用摄像头进行实时车道线检测
   - 图片检测：点击"选择图片"按钮，可以选择本地图片进行检测
   - 视频检测：点击"选择视频"按钮，可以选择本地视频文件进行检测
   - 停止：点击"停止"按钮可以终止当前检测任务

##### 项目结构
```
Lane-detection/
├── GUI.py              # 图形界面主程序
├── main.py             # 核心功能实现
├── Lane_line/         # 车道线检测模块
├── Yolov7/            # YOLO v7 目标检测模块
└── deeplabv3/         # DeepLabv3+ 语义分割模块
```

#### English
##### Running Steps

1. Launch the GUI:
```bash
python GUI.py
```

2. Features:
   - Real-time Detection: Click "Start Detection" to use camera for real-time lane detection
   - Image Detection: Click "Select Image" to choose a local image for detection
   - Video Detection: Click "Select Video" to choose a local video file for detection
   - Stop: Click "Stop" to terminate the current detection task

##### Project Structure
```
Lane-detection/
├── GUI.py              # Main GUI program
├── main.py             # Core functionality implementation
├── Lane_line/         # Lane detection module
├── Yolov7/            # YOLO v7 object detection module
└── deeplabv3/         # DeepLabv3+ semantic segmentation module
```
# 参考文献
[1]Chien-Yao Wang、Alexey Bochkovskiy、Hong-Yuan Mark Liao， 《YOLOv7: Trainable bag-of-freebies sets new state-of-the-art for real-time object detectors》， https://www.semanticscholar.org/reader/3aed4648f7857c1d5e9b1da4c3afaf97463138c3 ， 访问时间  
[2]Liang-Chieh Chen、 Yukun Zhu、 George Papandreou etc， 《Encoder-Decoder with Atrous Separable Convolution for Semantic Image Segmentation》， 1802.02611.pdf (arxiv.org)， 访问时间  
[3]CSDN（2022），(67条消息) 睿智的目标检测61——Pytorch搭建YoloV7目标检测平台_Bubbliiiing的博客-CSDN博客_pytorch yolov7  
[4]Github（2022），YOLOV：You Only Look Once目标检测模型在pytorch当中的实现，GitHub-bubbliiiing/yolov7-pytorch，访问时间
[5]Github（2022），DeepLabv3+:Encoder-Decoder with Atrous Separable Convolution语义分割模型在pytorch当中的实现，GitHub - bubbliiiing/deeplabv3-plus-pytorch  
[6]Github（2022），高级寻车项目，GitHub - ajsmilutin/CarND-Advanced-Lane-Lines  
[7]Github（2022），飞桨ELSeg，PaddleSeg/EISeg at release/2.6·PaddlePaddle/PaddleSeg·GitHub  
[8]python软件基金会， tkinter-python接口到Tcl/Tk， tkinter — Python 接口到 Tcl/Tk — Python 3.11.1 文档  
[9]阿斯顿·张、李沐、亚历山大·J·斯莫拉， 动手学深度学习（M）， 人民邮电出版  
