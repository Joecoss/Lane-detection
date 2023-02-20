import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from deeplabv3.deeplab import DeeplabV3
from Yolov7.yolo import YOLO
from PIL import Image
import numpy as np
import cv2
from Lane_line.lane import Lane_line

# 判断空变量
Type_cap = None
Type_name = None

def Lane_draw(lane, img, image_thresh_binary):
    # 透视变换局部变量
    src_corners = [(415, 335), (585, 335), (1000, 600), (0, 600)]
    # dst_corners = [(0, 0), (600, 0), (600, 1000), (0, 1000)]
    dst_corners = [(0, 0), (1000, 0), (1000, 600), (0, 600)]
    M = cv2.getPerspectiveTransform(np.float32(src_corners), np.float32(dst_corners))
    N = cv2.getPerspectiveTransform(np.float32(dst_corners), np.float32(src_corners))
    # 透视变换成俯视图
    image_thresh_binary = lane.perspective_transform(image_thresh_binary, M)
    # 获取左右车道线的曲线坐标
    left_fit, right_fit, out_img, TF = lane.find_line_fit(np.array(image_thresh_binary))
    if TF == 1:
        left_fitx, right_fitx, ploty = lane.get_fit_xy(out_img, left_fit, right_fit)
        # 绘制车道范围再透视变换回原图
        result = lane.project_back(np.array(image_thresh_binary), left_fitx, right_fitx, ploty)
        result = Lane(lane, result, np.array(img), left_fitx, right_fitx, N)
        return result
    else:
        return img

def Lane(lane, result, img, pts_left, pts_right,N):
    left = np.int_(pts_left[549])
    right = np.int_(pts_right[549])
    left_right = [left, right, int((left+right)/2)]
    if len(left_right) > 1:
        image = cv2.line(result, (left_right[0], 549), (left_right[1], 549), (255, 0, 0), 3)
        image_blue_left = cv2.line(image, (left_right[0], 524), (left_right[0], 574), (255, 0, 0), 5)
        image_blue_right = cv2.line(image_blue_left, (left_right[1], 524), (left_right[1], 574), (255, 0, 0), 5)
        image_bule_center = cv2.line(image_blue_right, (left_right[2], 534), (left_right[2], 564), (255, 0, 0), 3)
        image_white_center = cv2.line(image_bule_center, (500, 524), (500, 574), (255, 255, 255), 5)

        if left_right[2] < 480:
            ation_text = "left"
            result = cv2.arrowedLine(np.array(image_white_center), (500, 549), (left_right[2], 549), (0, 0, 255),
                                     thickness=3, line_type=cv2.LINE_4, shift=0, tipLength=0.2)
        elif left_right[2] > 520:
            ation_text = "right"
            result = cv2.arrowedLine(np.array(image_white_center), (500, 549), (left_right[2], 549), (0, 0, 255),
                                     thickness=3, line_type=cv2.LINE_4, shift=0, tipLength=0.2)
        else:
            ation_text = "center"
            result = cv2.line(np.array(image_white_center), (480, 549), (520, 549), (255, 0, 255), 5)
        newwarp = lane.perspective_transform(result, N)
        result = cv2.addWeighted(img, 1, newwarp, 0.7, 0)
        result = cv2.putText(result, "ation: "+ation_text, (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1,(0, 255, 0), 2)
        return result

def keshihua():
    global cap
    global capture
    global path
    global Type_name
    global Type_cap
    # 当开启摄像头时，识别输出
    if Type_cap == True:
        while capture.isOpened():
            ret, frame = capture.read()
            if ret == True:
                img = cv2.resize(frame, (1000, 600))
                img = Image.fromarray(np.uint8(img))
                r_image_yolo = yolo.detect_image(img)
                r_image, image_thresh_binary = deeplab.detect_image(img)
                result = Lane_draw(lane, np.array(r_image_yolo), np.array(image_thresh_binary))
                Show_Video(result, 700, 500)
            else:
                break

    # 当为照片时，进行识别输出
    if Type_name == True:
        img = cv2.imread(path)
        img = cv2.resize(img, (1000, 600))
        img = Image.fromarray(np.uint8(img))
        r_image_yolo = yolo.detect_image(img)
        r_image, image_thresh_binary = deeplab.detect_image(img)
        result = Lane_draw(lane, np.array(r_image_yolo), np.array(image_thresh_binary))
        Show_Video(result, 700, 500)
        time.sleep(5)


    # 当为视频时，识别输出
    elif Type_name == False:
        # create_file()
        while cap.isOpened():
            ret, frame = cap.read()
            if ret == True:
                img = cv2.resize(frame, (1000, 600))
                img = Image.fromarray(np.uint8(img))
                r_image_yolo = yolo.detect_image(img)
                r_image, image_thresh_binary = deeplab.detect_image(img)
                result = Lane_draw(lane, np.array(r_image_yolo), np.array(image_thresh_binary))
                Show_Video(result, 700, 500)
            else:
                break




def Yolov7():
    # 当开启摄像头时，识别输出
    if Type_cap == True:
        while capture.isOpened():
            ret, frame = capture.read()
            if ret == True:
                img = cv2.resize(frame, (1000, 600))
                img = Image.fromarray(np.uint8(img))
                r_image_yolo = yolo.detect_image(img)
                Show_Video(r_image_yolo, 700, 500)
            else:
                break

    # 当为照片时，进行识别输出
    if Type_name == True:
        img = cv2.imread(path)
        img = cv2.resize(img, (1000, 600))
        img = Image.fromarray(np.uint8(img))
        r_image_yolo = yolo.detect_image(img)
        Show_Video(r_image_yolo, 700, 500)
        time.sleep(5)

    # 当为视频时，识别输出
    elif Type_name == False:
        # create_file()
        while cap.isOpened():
            ret, frame = cap.read()
            if ret == True:
                img = cv2.resize(frame, (1000, 600))
                img = Image.fromarray(np.uint8(img))
                r_image_yolo = yolo.detect_image(img)
                Show_Video(r_image_yolo, 700, 500)
            else:
                break

def Deeplabv3():
    # 当开启摄像头时，识别输出
    if Type_cap == True:
        while capture.isOpened():
            ret, frame = capture.read()
            if ret == True:
                img = cv2.resize(frame, (1000, 600))
                img = Image.fromarray(np.uint8(img))
                r_image, image_thresh_binary = deeplab.detect_image(img)
                Show_Video(r_image, 700, 500)
            else:
                break


    # 当为照片时，进行识别输出
    if Type_name == True:
        img = cv2.imread(path)
        img = cv2.resize(img, (1000, 600))
        img = Image.fromarray(np.uint8(img))
        r_image, image_thresh_binary = deeplab.detect_image(img)
        Show_Video(r_image, 700, 500)
        time.sleep(5)


    # 当为视频时，识别输出
    elif Type_name == False:
        while cap.isOpened():
            ret, frame = cap.read()
            if ret == True:
                img = cv2.resize(frame, (1000, 600))
                img = Image.fromarray(np.uint8(img))
                r_image, image_thresh_binary = deeplab.detect_image(img)
                Show_Video(r_image, 700, 500)
            else:
                break



# 桌面清除功能
def Desktop():
    Video_canvas.delete('path')
    Video_canvas.delete('video')
#
# 设置背景图片缩放功能
def get_image(filename, width, height):
    im = Image.open(filename).resize((width, height))
    return ImageTk.PhotoImage(im)

# 读取视频转换为帧动画
def Read_Video(cap, w_, h_):
    ref, frame = cap.read()
    tkimage = Resize_Video(frame, w_, h_)
    return tkimage

# 将帧动画按一定比例缩小
def Resize_Video(frame, w_, h_):
    cvimage = cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(cvimage)
    pilImage = pilImage.resize((w_, h_), Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(image=pilImage)
    return tkimage

# 将帧动画显示到窗口
def Show_Video(frame, w_, h_):
    tkmask = Resize_Video(frame, w_, h_)
    Video_canvas.create_image(0, 0, anchor='nw', image=tkmask)
    Video_canvas.update()
    Video_canvas.after(1)


# 标签清除功能
def Label_clear():
    strPathVar.set("")

# 选择文件的途径并显示出来
def path_select():
    global cap
    global srcImage
    global path
    global Type_name
    global Type_cap
    Label_clear()
    path = filedialog.askopenfilename()
    photo = ['.jpg', '.png', '.bmp', 'jpeg']
    video = ['.mp4', '.mov']
    for i in photo:
        if i in path.lower():
            frame = cv2.imread(path)
            srcImage = Resize_Video(frame, 700, 500)
            Video_canvas.create_image(350, 250, anchor='center', image=srcImage, tag="path")
            Video_canvas.update()
            Video_canvas.after(1)
            strPathVar.set(path)
            Type_name = True
            break
        else:
            for j in video:
                if j in path.lower():
                    cap = cv2.VideoCapture(path)
                    strPathVar.set(path)
                    Type_name = False
                    while True:
                        picture = Read_Video(cap, 700, 500)
                        Video_canvas.create_image(0, 0, anchor='nw', image=picture, tag="video")
                        Video_canvas.update()
                        Video_canvas.after(1)
                        continue
                    break
                else:
                    string = "图片(jpg,png,bmp,jpeg), 视频(mp4,mov)"
                    strPathVar.set(string)
                    break

# 选择文件的途径并显示出来
def Model_path_select():
    global Model_path
    Model_path = filedialog.askopenfilename()
    data_pth = ".pth"
    if data_pth in Model_path.lower():
        strModel_data.set(Model_path)
        deeplab._defaults["model_path"] = strModel_data
    else:
        string = "请输入正确语义分割权重（.pth）"
        strModel_data.set(string)


# 打开摄像头
def Open_camera( ):
    global capture
    global Type_cap
    Label_clear()
    Type_cap = True
    Camera(Type_cap)

# 关闭摄像头
def Close_camera():
    global Type_cpa
    Type_cap = False
    Camera(Type_cap)
    Desktop()
    Label_clear()

# 摄像头的显示功能
def Camera(Type_cap):
    global capture
    capture = cv2.VideoCapture(0)
    while capture.isOpened():
        if Type_cap == False:
            capture.release()
            break
        ref, frame = capture.read()
        picture = Resize_Video(frame, 700, 500)
        Video_canvas.create_image(0, 0, anchor='nw', image=picture)
        Video_canvas.update()
        Video_canvas.after(1)
        if Type_cap == False:
            capture.release()
            break
if __name__ == '__main__':
    yolo = YOLO()
    deeplab = DeeplabV3()
    lane = Lane_line()


    # 设置窗口基本信息
    win = tk.Tk()
    win.title("车道线检测系统")
    win.geometry("1000x600")
    win.resizable(height=False, width=False)

    strPathVar = tk.StringVar()
    strModel_data = tk.StringVar()


    # 标题区域
    title_box = tk.Frame(win, width=1000, height=100, borderwidth=0, bg="white")
    title_box.place(x=0)
    # 添加标题
    title = tk.Label(title_box, text="车道线检测系统", fg="black", font=("宋体", 30), bg="white")
    title.place(x=350, y=25)


    # 显示区域
    show_box = tk.Frame(win, width=700, height=500, borderwidth=0, bg="gray", relief="groove")
    show_box.place(x=0, y=100)
    # 视频显示
    Video_canvas = tk.Canvas(show_box, width=700, height=500, borderwidth=2, bg='black')
    im2 = get_image("./image/Road.jpg", 700, 500)
    Video_canvas.create_image(350, 250, image=im2)
    Video_canvas.pack()


    # 功能区域
    work_box = tk.Frame(win, width=300, height=500, borderwidth=0, bg="yellow")
    work_box.place(x=700, y=102)

    #打开本地图像或视频
    open_box = tk.Frame(work_box, width=300, height=130, borderwidth=0, bg="lightblue")
    open_box.place(x=0, y=0)
    # 链接显示
    choose_show = tk.Entry(open_box, width=35, textvariable=strPathVar)
    choose_show.place(x=25, y=40)
    # 添加按键
    choose = tk.Button(open_box, width=35, text="选择文件", bg="lightgray", command=path_select)
    choose.place(x=25, y=90)

    # 权重选择
    weight_box = tk.Frame(work_box, width=300, height=130, borderwidth=0, bg="lightblue")
    weight_box.place(x=0, y=130)
    # 链接显示
    weight_show = tk.Entry(weight_box, width=35, textvariable=strModel_data)
    weight_show.place(x=25, y=30)
    # 按键
    weight_button = tk.Button(weight_box, width=35, text="选择权重", bg="lightgray", command=Model_path_select)
    weight_button.place(x=25, y=80)

    #摄像头操控区域
    camera_box = tk.Frame(work_box, width= 300, height=50, borderwidth=0, bg="lightblue")
    camera_box.place(x=0, y=260)
    # 打开摄像头
    open_camera = tk.Button(camera_box, text="打开摄像头", width=10, bg="lightgray", command=Open_camera)
    open_camera.place(x=30, y=12)
    # 关闭摄像头
    close_camera = tk.Button(camera_box, text="关闭摄像头", width=10, bg="lightgray", command=Close_camera)
    close_camera.place(x=190, y=12)

    # 按键区域
    button_box = tk.Frame(work_box, width=300, height=370, borderwidth=0, bg="lightblue")
    button_box.place(x=0, y=310)

    # 目标检测
    detection = tk.Button(button_box, width=35, text="目标检测", bg="lightgray", command=Yolov7)
    detection.place(x=25, y=25)
    # 语义分割
    split = tk.Button(button_box, width=35, text="语义分割", bg="lightgray", command=Deeplabv3)
    split.place(x=25, y=75)
    #检测可视化
    check = tk.Button(button_box, width=35, text="检测可视化", bg="lightgray", command=keshihua)
    check.place(x=25, y=115)

    win.mainloop()

