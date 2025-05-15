import cv2
import numpy as np


def get_dominant_color(image):
    pixels = np.float32(image.reshape(-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.1)
    _, labels, centers = cv2.kmeans(pixels, 5, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(centers[np.argmax(np.unique(labels, return_counts=True)[1])])
    return center


def process_cube_face(image_path):
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    cell_height = h // 3
    cell_width = w // 3
    colors = []
    for i in range(3):
        for j in range(3):
            cell = img[i * cell_height:(i + 1) * cell_height, j * cell_width:(j + 1) * cell_width]
            color = get_dominant_color(cell)
            colors.append(tuple(color))

    with open('cube_face_colors.txt', 'w') as f:
        for i in range(0, 9, 3):
            row = colors[i:i + 3]
            color_names = []
            for color in row:
                b, g, r = color
                if (r > 100 and g < 50 and b < 50):
                    color_names.append("Red")
                elif (g > 100 and r < 50 and b < 50):
                    color_names.append("Green")
                elif (b > 100 and r < 50 and g < 50):
                    color_names.append("Blue")
                elif (r > 100 and g > 100 and b < 50):
                    color_names.append("Yellow")
                elif (r > 100 and b > 100 and g < 50):
                    color_names.append("Orange")
                elif (r < 50 and g < 50 and b < 50):
                    color_names.append("White")
            f.write(' '.join(color_names) + '\n')


if __name__ == "__main__":
    image_path = 'picture/0.546875right_img.png'  # 请将此处替换为实际的魔方图片路径
    process_cube_face(image_path)