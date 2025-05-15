import cv2

def cv_img_RGB(
        image = 'test/1.png',
        image_x = 2,
        image_y = 2
        ):
    

    # 读取图片
    image = cv2.imread(image)
    x_x = int(10 * image_x + 4),y_x = int(10 * image_y + 4)
    x_y = int(10 * image_x + 8),y_y = int(10 * image_y + 8)
    # 定义区域坐标 (x1, y1, x2, y2)(30*30)
    x1, y1, x2, y2 = x_x, y_x, x_y, y_y
    # 提取区域图像
    region = image[y1:y2, x1:x2]
    # 计算区域内颜色的平均值
    average_color = cv2.mean(region)[:3]
    print(average_color)
    # 定义颜色范围和对应的抽象称呼
    #'green','red','orange','white','yellow','blue'
    #'绿色', '红色', '橙色', '白色', '黄色', '蓝色'
    color_ranges = {
        'red': ((0, 0, 128), (80, 70, 255)),
        'green': ((0, 128, 0), (120, 255, 80)),
        'blue': ((128, 0, 0), (255, 180, 50)),
        'yellow': ((70, 90, 70), (150, 255, 255)),
        'white': ((128, 0, 128), (255, 50, 255)),
        'orange': ((0, 64, 128), (70, 192, 255))
    }

    # 判断平均颜色属于哪个范围
    for name, (lower, upper) in color_ranges.items():
        if all(lower[i] <= average_color[i] <= upper[i] for i in range(3)):
            print(f"该区域的颜色抽象称呼为: {name}")
            return name
    else:
        print("未找到匹配的颜色称呼")

cv_img_RGB()