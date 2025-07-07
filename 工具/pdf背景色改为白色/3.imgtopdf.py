import img2pdf
import tkinter as tk
from tkinter import filedialog, messagebox

def images_to_pdf(image_paths, output_pdf):
    """
    将多张图片合并为一个PDF
    :param image_paths: 图片路径列表
    :param output_pdf: 输出PDF路径
    """
    try:
        # 检查图片是否有效
        valid_images = []
        for img_path in image_paths:
            try:
                valid_images.append(img_path)
            except Exception as e:
                print(f"跳过无效图片: {img_path} - {e}")

        if not valid_images:
            raise ValueError("没有有效的图片可转换")

        # 转换为PDF
        with open(output_pdf, "wb") as f:
            f.write(img2pdf.convert(valid_images))

        return True
    except Exception as e:
        messagebox.showerror("错误", f"转换失败: {e}")
        return False

def select_images_and_output():
    """
    GUI选择图片和输出PDF路径
    """
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 选择多张图片
    image_paths = filedialog.askopenfilenames(
        title="选择图片",
        filetypes=[("图片文件", "*.png;*.jpg;*.jpeg")]
    )
    if not image_paths:
        return None, None

    # 选择输出PDF路径
    output_pdf = filedialog.asksaveasfilename(
        title="保存PDF",
        defaultextension=".pdf",
        filetypes=[("PDF文件", "*.pdf")]
    )
    if not output_pdf:
        return None, None

    return image_paths, output_pdf

if __name__ == "__main__":
    image_paths, output_pdf = select_images_and_output()
    if image_paths and output_pdf:
        success = images_to_pdf(image_paths, output_pdf)
        if success:
            messagebox.showinfo("完成", f"PDF已保存到:\n{output_pdf}")
    else:
        messagebox.showwarning("取消", "操作已取消")