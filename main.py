#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from watermark_processor import WatermarkProcessor, get_image_files, create_watermark_directory
from exif_reader import EXIFReader


def get_user_input():
    """获取用户输入的参数"""
    # 获取图片路径
    while True:
        image_path = input("请输入图片文件路径或包含图片的目录路径: ").strip()
        if os.path.exists(image_path):
            break
        else:
            print("路径不存在，请重新输入！")
    
    # 获取水印位置
    print("\n请选择水印位置:")
    print("1. 左上角 (top_left)")
    print("2. 顶部中央 (top_center)")
    print("3. 右上角 (top_right)")
    print("4. 中央 (center)")
    print("5. 左下角 (bottom_left)")
    print("6. 底部中央 (bottom_center)")
    print("7. 右下角 (bottom_right) [默认]")
    
    position_map = {
        '1': 'top_left',
        '2': 'top_center',
        '3': 'top_right',
        '4': 'center',
        '5': 'bottom_left',
        '6': 'bottom_center',
        '7': 'bottom_right'
    }
    
    position_choice = input("请输入选择 (1-7) [默认7]: ").strip()
    position = position_map.get(position_choice, 'bottom_right')
    
    # 获取字体大小
    while True:
        try:
            font_size = input("请输入字体大小 [默认20]: ").strip()
            if font_size == "":
                font_size = 20
            else:
                font_size = int(font_size)
            break
        except ValueError:
            print("请输入有效的数字！")
    
    # 获取字体颜色
    while True:
        try:
            color_input = input("请输入字体颜色(R,G,B) [默认255,255,255]: ").strip()
            if color_input == "":
                font_color = (255, 255, 255)
            else:
                rgb_values = color_input.split(',')
                if len(rgb_values) != 3:
                    raise ValueError
                font_color = tuple(int(val.strip()) for val in rgb_values)
                # 验证RGB值范围
                if not all(0 <= val <= 255 for val in font_color):
                    raise ValueError
            break
        except ValueError:
            print("请输入有效的RGB颜色值，格式为R,G,B，每个值应在0-255之间！")
    
    return image_path, position, font_size, font_color


def process_images(image_path, position, font_size, font_color):
    """处理图片"""
    # 确定是文件还是目录
    if os.path.isfile(image_path):
        # 如果是文件，获取其所在目录
        directory = os.path.dirname(image_path)
        image_files = [image_path] if image_path.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff', '.tif')) else []
    else:
        # 如果是目录，获取所有图片文件
        directory = image_path
        image_files = get_image_files(image_path)
    
    if not image_files:
        print("未找到图片文件！")
        return
    
    # 创建水印目录
    watermark_dir = create_watermark_directory(directory)
    print(f"水印图片将保存到: {watermark_dir}")
    
    # 初始化水印处理器
    processor = WatermarkProcessor(font_size=font_size, font_color=font_color, position=position)
    
    # 处理每个图片文件
    success_count = 0
    for img_file in image_files:
        print(f"正在处理: {img_file}")
        
        # 读取EXIF信息
        exif_data = EXIFReader.get_exif_data(img_file)
        if not exif_data:
            print(f"  跳过 {img_file} (无法读取EXIF信息)")
            continue
        
        # 提取拍摄时间
        datetime_str = EXIFReader.extract_datetime(exif_data)
        if not datetime_str:
            print(f"  跳过 {img_file} (无法提取拍摄时间)")
            continue
        
        # 生成输出文件路径
        filename = os.path.basename(img_file)
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}_watermark{ext}"
        output_path = os.path.join(watermark_dir, output_filename)
        
        # 添加水印
        if processor.add_watermark(img_file, datetime_str, output_path):
            print(f"  成功添加水印: {output_path}")
            success_count += 1
        else:
            print(f"  添加水印失败: {img_file}")
    
    print(f"\n处理完成！成功处理 {success_count}/{len(image_files)} 张图片。")


def main():
    """主函数"""
    print("=== PhotoWatermark 图片水印工具 ===")
    
    try:
        # 获取用户输入
        image_path, position, font_size, font_color = get_user_input()
        
        # 处理图片
        process_images(image_path, position, font_size, font_color)
        
    except KeyboardInterrupt:
        print("\n\n程序被用户中断。")
    except Exception as e:
        print(f"\n程序运行出错: {e}")


if __name__ == "__main__":
    main()