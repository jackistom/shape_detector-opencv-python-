import cv2
import time
import imutils
import numpy as np
import os
import binascii

def drawMyContours(winName, image, contours, draw_on_blank):

    if (draw_on_blank):

        temp = np.ones(image.shape, dtype=np.uint8) * 255

        cv2.drawContours(temp, contours, -1, (0, 0, 0), 2)

    else:

        temp = image.copy()

        cv2.drawContours(temp, contours, -1, (0, 0, 255), 2)
    cv2.namedWindow("winName",cv2.WINDOW_NORMAL)
    cv2.imshow(winName, temp)

    cv2.waitKey()


def delet_contours(contours, delete_list):

    delta = 0

    for i in range(len(delete_list)):

        # print("i= ", i)

        del contours[delete_list[i] - delta]

        delta = delta + 1

    return contours

image = cv2.imread("666.jpg", cv2.IMREAD_UNCHANGED)
# print(image.shape)
callback= image.shape

image = cv2.resize(image, (int(0.8 * callback[1]), int(0.8 * callback[0])), interpolation=cv2.INTER_CUBIC)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 1)
size=2
kernel=np.ones((size,size),dtype=np.uint8)
#element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
img_dilation=cv2.dilate(gray,kernel,100)
binary = cv2.morphologyEx(img_dilation, cv2.MORPH_CLOSE, kernel)
ret, binary = cv2.threshold(binary, 160, 255, cv2.THRESH_BINARY_INV)
cv2.namedWindow("binary", cv2.WINDOW_NORMAL)
cv2.imshow("binary", binary)
# 3.查找轮廓
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
drawMyContours("find contours", image, contours, True)
# hierarchy[i]: [Next，Previous，First_Child，Parent]
# 要求没有父级轮廓 因为很多干扰物有 子级轮廓 通过含有不同轮廓的特性 对轮廓进行筛选
delete_list = []  # 新建待删除的轮廓序号列表

c, row, col = hierarchy.shape

for i in range(row):

    if hierarchy[0, i, 2] <3 or hierarchy[0, i, 3] <3:  # 有父轮廓或子轮廓

       delete_list.append(i)

# 根据列表序号删除不符合要求的轮廓

contours = delet_contours(contours, delete_list)

print(len(contours), "contours left after hierarchy filter")

drawMyContours("contours after hierarchy filtering", image, contours, True)

# 5.2使用轮廓长度滤波

min_size = 20

max_size = 1000

delete_list = []

for i in range(len(contours)):

    if (cv2.arcLength(contours[i], True) < min_size) or (cv2.arcLength(contours[i], True) > max_size):

       delete_list.append(i)

# 根据列表序号删除不符合要求的轮廓

contours = delet_contours(contours, delete_list)

print(len(contours), "contours left after length filter")

drawMyContours("contours after length filtering", image, contours, False)

# 6.形状描述子

# 6.1 最小覆盖矩形

result = image.copy()

x, y, w, h = cv2.boundingRect(contours[0])  # （x,y）为矩形左上角的坐标，（w,h）是矩形的宽和高

cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 255), 1)

# 6.2 凸包

hull = cv2.convexHull(contours[1])

cv2.polylines(result, [hull], True, (0, 255, 0), 1)

# 7.画重心

for i in range(len(contours)):
    mom = cv2.moments(contours[i])

    pt = (int(mom['m10'] / mom['m00']), int(mom['m01'] / mom['m00']))  # 使用前三个矩m00, m01和m10计算重心

    cv2.circle(result, pt, 2, (0, 0, 255), 2)  # 画红点

    text = "(" + str(pt[0]) + ", " + str(pt[1]) + ")"

    cv2.putText(result, text, (pt[0] + 10, pt[1] + 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 1, 8, 0);
cv2.namedWindow("center",cv2.WINDOW_NORMAL)

cv2.imshow("center", result)

cv2.waitKey()
print("fially find", len(contours), "contours")


cv2.imshow("morphology", binary)

cv2.waitKey()
