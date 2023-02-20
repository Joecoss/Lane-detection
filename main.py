from deeplabv3.deeplab import DeeplabV3
from Yolov7.yolo import YOLO
from PIL import Image
import numpy as np
import cv2
from Lane_line.lane import Lane_line

def Lane_draw(lane, image_yolo, image_thresh_binary):
    # 透视变换局部变量
    src_corners = [(415, 335), (585, 335), (1000, 600), (0, 600)]
    # src_corners = [(430, 335), (560, 335), (1000, 600), (0, 600)]
    dst_corners = [(0, 0), (1000, 0), (1000, 600), (0, 600)]
    M = cv2.getPerspectiveTransform(np.float32(src_corners), np.float32(dst_corners))
    N = cv2.getPerspectiveTransform(np.float32(dst_corners), np.float32(src_corners))
    # 透视变换成鸟瞰图
    aerial_view = lane.perspective_transform(image_thresh_binary, M)
    # 获取左右车道线的曲线坐标
    left_fit, right_fit, out_img, True_False = lane.find_line_fit(np.array(aerial_view))
    if True_False == 1:
        left_fitx, right_fitx, ploty = lane.get_fit_xy(out_img, left_fit, right_fit)
        # 绘制车道掩膜鸟瞰图
        mask_aerial_view = lane.project_back(np.array(aerial_view), left_fitx, right_fitx, ploty)
        result = Lane(lane, mask_aerial_view, np.array(image_yolo), left_fitx, right_fitx, N)
        return result
    else:
        return img

# 功能坐标的绘制及图像融合
def Lane(lane, mask_aerial_view, image_yolo, pts_left, pts_right,N):
    # 将549行的左右曲线点和左右曲线中点的横坐标存放在left_right的列表中
    left = np.int_(pts_left[549])
    right = np.int_(pts_right[549])
    left_right = [left, right, int((left+right)/2)]
    if len(left_right) > 1:
        # 进行功能坐标的绘制
        image = cv2.line(mask_aerial_view, (left_right[0], 549), (left_right[1], 549), (255, 0, 0), 3)
        image_blue_left = cv2.line(image, (left_right[0], 524), (left_right[0], 574), (255, 0, 0), 5)
        image_blue_right = cv2.line(image_blue_left, (left_right[1], 524), (left_right[1], 574), (255, 0, 0), 5)
        image_bule_center = cv2.line(image_blue_right, (left_right[2], 534), (left_right[2], 564), (255, 0, 0), 3)
        image_white_center = cv2.line(image_bule_center, (500, 524), (500, 574), (255, 255, 255), 5)
        if left_right[2] < 480:
            ation_text = "left"
            mask_aerial_view = cv2.arrowedLine(np.array(image_white_center), (500, 549), (left_right[2], 549), (0, 0, 255),
                                     thickness=3, line_type=cv2.LINE_4, shift=0, tipLength=0.2)
        elif left_right[2] > 520:
            ation_text = "right"
            mask_aerial_view = cv2.arrowedLine(np.array(image_white_center), (500, 549), (left_right[2], 549), (0, 0, 255),
                                     thickness=3, line_type=cv2.LINE_4, shift=0, tipLength=0.2)
        else:
            ation_text = "center"
            mask_aerial_view = cv2.line(np.array(image_white_center), (480, 549), (520, 549), (255, 0, 255), 5)
        # 车道掩膜鸟瞰图透视变换回车道掩膜前视图
        mask_front_view = lane.perspective_transform(mask_aerial_view, N)
        # 图像融合
        result = cv2.addWeighted(image_yolo, 1, mask_front_view, 0.7, 0)
        # 在图像上绘制转向文本
        result = cv2.putText(result, "ation: "+ation_text, (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
        return result

if __name__ == '__main__':
    yolo = YOLO()
    deeplab = DeeplabV3()
    lane = Lane_line()
    img = cv2.imread("./image/night_img1130.jpg")
    img = cv2.resize(img, (1000, 600))
    img = Image.fromarray(np.uint8(img))
    image_yolo = yolo.detect_image(img)
    image, image_thresh_binary = deeplab.detect_image(img)
    result = Lane_draw(lane, np.array(image_yolo), np.array(image_thresh_binary))
    while True:
        cv2.imshow("frame", result)
        cv2.waitKey(1) & 0xff