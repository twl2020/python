import os
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox


def pdf_to_images(input_pdf, output_folder, dpi=300, image_format="png"):
    """将 PDF 每一页保存为图片"""
    doc = fitz.open(input_pdf)

    # 创建输出文件夹（如果不存在）
    os.makedirs(output_folder, exist_ok=True)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=dpi)

        # 保存图片
        image_path = os.path.join(output_folder, f"page_{page_num + 1}.{image_format}")
        pix.save(image_path)

    doc.close()
    return len(doc)  # 返回转换的页数


def select_pdf_and_output():
    """GUI 选择 PDF 和输出文件夹"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 选择 PDF 文件
    input_pdf = filedialog.askopenfilename(
        title="选择 PDF 文件",
        filetypes=[("PDF 文件", "*.pdf")]
    )
    if not input_pdf:
        return None, None, None

    # 选择输出文件夹
    output_folder = filedialog.askdirectory(title="选择输出文件夹")
    if not output_folder:
        return None, None, None

    # 输入 DPI（分辨率）
    dpi = simpledialog.askinteger(
        "输入 DPI",
        "请输入图片分辨率 (DPI, 推荐 150-300):",
        initialvalue=300,
        minvalue=72,
        maxvalue=1200
    )
    if not dpi:
        return None, None, None

    return input_pdf, output_folder, dpi


if __name__ == "__main__":
    input_pdf, output_folder, dpi = select_pdf_and_output()

    if all([input_pdf, output_folder, dpi]):
        total_pages = pdf_to_images(input_pdf, output_folder, dpi)
        messagebox.showinfo(
            "转换完成",
            f"成功转换 {total_pages} 页！\n图片保存在：{output_folder}"
        )
    else:
        messagebox.showwarning("取消", "操作已取消")