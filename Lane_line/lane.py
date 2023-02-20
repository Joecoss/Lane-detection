import numpy as np
import cv2

class Lane_line(object):
    # 透视变换
    def perspective_transform(self, img, M_N):
        img_size = (img.shape[1], img.shape[0])
        warped = cv2.warpPerspective(img, M_N, img_size, flags=cv2.INTER_LINEAR)
        return warped

    # 左右车道线的曲线拟合
    def find_line_fit(self, img):
        # 滑动窗口的数量
        nwindows = 50
        # 设置x的检测范围，滑动窗口的宽度的一半，手动指定
        margin = 100
        # 设置最小像素点，阈值用于统计滑动窗口区域内的非零像素个数，小于50的窗口不对x的中心值进行更新
        minpix = 50
        # 1.确定左右车道线的位置
        # 统计直方图
        histogram = np.sum(img[img.shape[0] // 2:, :], axis=0)
        out_img = np.dstack((img, img, img)) * 255
        # 在统计结果中找到左右最大的点的位置，作为左右车道检测的开始点
        # 将统计结果一分为二，划分为左右两个部分，分别定位峰值位置，即为两条车道的搜索位置
        midpoint = np.int(histogram.shape[0] / 2)
        leftx_base = np.argmax(histogram[:midpoint])
        rightx_base = np.argmax(histogram[midpoint:]) + midpoint


        window_height = np.int(img.shape[0] / nwindows)
        # 获取图像中不为0的点
        nonzero = img.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])
        # 车道检测的当前位置
        leftx_current = leftx_base
        rightx_current = rightx_base
        # 用来记录搜索窗口中非零点在nonzeroy和nonzerox中的索引
        left_lane_inds = []
        right_lane_inds = []


        for window in range(nwindows):
            # 设置窗口的y的检测范围，因为图像是（行列）,shape[0]表示y方向的结果，上面是0
            win_y_low = img.shape[0] - (window + 1) * window_height
            win_y_high = img.shape[0] - window * window_height
            # 左车道x的范围
            win_xleft_low = leftx_current - margin
            win_xleft_high = leftx_current + margin
            # 右车道x的范围
            win_xright_low = rightx_current - margin
            win_xright_high = rightx_current + margin

            cv2.rectangle(out_img, (win_xleft_low, win_y_low), (win_xleft_high, win_y_high),
                          (0, 255, 0), 2)
            cv2.rectangle(out_img, (win_xright_low, win_y_low), (win_xright_high, win_y_high),
                          (0, 255, 0), 2)
            # 确定非零点的位置x,y是否在搜索窗口中，将在搜索窗口内的x,y的索引存入left_lane_inds和right_lane_inds中
            good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) &
                              (nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high)).nonzero()[0]
            good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) &
                               (nonzerox >= win_xright_low) & (nonzerox < win_xright_high)).nonzero()[0]
            left_lane_inds.append(good_left_inds)
            right_lane_inds.append(good_right_inds)
            # 如果获取的点的个数大于最小个数，则利用其更新滑动窗口在x轴的位置
            if len(good_left_inds) > minpix:
                leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
            if len(good_right_inds) > minpix:
                rightx_current = np.int(np.mean(nonzerox[good_right_inds]))
        # 将检测出的左右车道点转换为array
        left_lane_inds = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)
        # 获取检测出的左右车道点在图像中的位置
        leftx = nonzerox[left_lane_inds]
        lefty = nonzeroy[left_lane_inds]
        rightx = nonzerox[right_lane_inds]
        righty = nonzeroy[right_lane_inds]
        out_img[nonzeroy[left_lane_inds], nonzerox[left_lane_inds]] = [255, 0, 0]
        out_img[nonzeroy[right_lane_inds], nonzerox[right_lane_inds]] = [0, 0, 255]
        try:
            # 3.用曲线拟合检测出的点,二次多项式拟合，返回的结果是系数
            left_fit = np.polyfit(lefty, leftx, 2)
            right_fit = np.polyfit(righty, rightx, 2)
            return left_fit, right_fit, out_img, 1
        except:
            return 0, 0, 0, 0

    def get_fit_xy(self, img, left_fit, right_fit):
        ploty = np.linspace(0, img.shape[0] - 1, img.shape[0])
        left_fitx = left_fit[0] * ploty ** 2 + left_fit[1] * ploty + left_fit[2]
        right_fitx = right_fit[0] * ploty ** 2 + right_fit[1] * ploty + right_fit[2]
        return left_fitx, right_fitx, ploty

    # 将获取的拟合曲线绘制车道区域掩膜
    def project_back(self, wrap_img, left_fitx, right_fitx, ploty):
        warp_zero = np.zeros_like(wrap_img).astype(np.uint8)
        color_warp = np.dstack((warp_zero, warp_zero, warp_zero))
        pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
        pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
        pts = np.hstack((pts_left, pts_right))
        cv2.fillPoly(color_warp, np.int_([pts]), (0, 255, 0))
        return color_warp