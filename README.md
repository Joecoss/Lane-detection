# Lane detection
本项目针对传统车道线检测鲁棒性较差的现象，通过运用YOLOV7与DeepLabv3+的图像深度学习算法对特定数据集进行模型训练，开发了一款能调用车载摄像头来识别道路环境，并用语音告知驾驶员偏离车道，前方车距等驾驶信息的偏离预警系统，辅助驾驶员更加安全高效的行驶。
![可视化](https://user-images.githubusercontent.com/89328970/220098900-36f5d74c-816d-4b66-95ee-b54f9d7d1861.JPG)

## 模型权重文件下载

由于体积较大，模型权重文件未直接存储在仓库中，请从 GitHub Release 页面下载：

1. yolov7 权重文件 `yolov7_weights.pth`：
   - [下载地址](https://github.com/Joecoss/Lane-detection/releases/tag/v1.0.0)
   - 下载后放置于 `Yolov7/model_data/` 目录下

2. deeplabv3+ 权重文件 `ep400-loss0.006-val_loss0.005.pth`：
   - [下载地址](https://github.com/Joecoss/Lane-detection/releases/tag/v1.0.0)
   - 下载后放置于 `deeplabv3/model_data/` 目录下

# GUI
![image](https://user-images.githubusercontent.com/89328970/220099687-7fb6ae20-8f9e-4df9-b516-f2961db1353c.png)
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
