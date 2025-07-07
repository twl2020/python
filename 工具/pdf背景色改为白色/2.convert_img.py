import os
import cv2
import numpy as np
from collections import defaultdict
from sklearn.cluster import KMeans
import tkinter as tk
from tkinter import filedialog, messagebox


def detect_background_color(image_path):
    """
    自动检测图片背景色
    :param image_path: 图片路径
    :return: 主要背景色(BGR格式)
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("无法读取图片，请检查路径是否正确")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, contours, -1, 255, thickness=cv2.FILLED)
    background_mask = cv2.bitwise_not(mask)
    background_pixels = img[background_mask == 255]

    if len(background_pixels) == 0:
        return np.array([255, 255, 255])  # 默认白色背景

    kmeans = KMeans(n_clusters=3, random_state=0).fit(background_pixels)
    counts = defaultdict(int)
    for label in kmeans.labels_:
        counts[label] += 1
    dominant_color = kmeans.cluster_centers_[max(counts, key=counts.get)]
    return dominant_color.astype(int)


def auto_remove_bg(image_path, output_path):
    """
    自动去除背景并保存
    :param image_path: 输入图片路径
    :param output_path: 输出图片路径
    """
    bg_color = detect_background_color(image_path)
    img = cv2.imread(image_path)

    lower = np.maximum(bg_color - 50, 0)
    upper = np.minimum(bg_color + 60, 255)
    mask = cv2.inRange(img, lower, upper)

    result = img.copy()
    result[mask == 255] = [255, 255, 255]  # 替换为白色背景
    cv2.imwrite(output_path, result)


def process_folder(input_folder, output_folder):
    """
    批量处理文件夹中的所有图片
    :param input_folder: 输入文件夹路径
    :param output_folder: 输出文件夹路径
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    processed_files = 0
    for file in os.listdir(input_folder):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                input_path = os.path.join(input_folder, file)
                output_path = os.path.join(output_folder, f"clean_{file}")
                auto_remove_bg(input_path, output_path)
                processed_files += 1
            except Exception as e:
                print(f"处理 {file} 失败: {e}")

    return processed_files


def select_folders():
    """
    GUI 选择输入/输出文件夹
    """
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 选择输入文件夹
    input_folder = filedialog.askdirectory(title="选择输入图片文件夹")
    if not input_folder:
        return None, None

    # 选择输出文件夹
    output_folder = filedialog.askdirectory(title="选择输出文件夹")
    if not output_folder:
        return None, None

    return input_folder, output_folder


if __name__ == "__main__":
    input_folder, output_folder = select_folders()
    if input_folder and output_folder:
        processed_count = process_folder(input_folder, output_folder)
        messagebox.showinfo(
            "完成",
            f"成功处理 {processed_count} 张图片！\n输出路径: {output_folder}"
        )
    else:
        messagebox.showwarning("取消", "操作已取消")