import os
import sys
from PIL import Image, ExifTags
import exifread
from datetime import datetime
import argparse


class WatermarkProcessor:
    """处理图片水印的类"""
    
    def __init__(self, font_size=20, font_color=(255, 255, 255), position='bottom_right'):
        """
        初始化水印处理器
        :param font_size: 字体大小
        :param font_color: 字体颜色 (R, G, B)
        :param position: 水印位置
        """
        self.font_size = font_size
        self.font_color = font_color
        self.position = position
    
    def add_watermark(self, image_path, watermark_text, output_path):
        """
        在图片上添加水印
        :param image_path: 原始图片路径
        :param watermark_text: 水印文本
        :param output_path: 输出图片路径
        :return: 是否成功
        """
        try:
            # 打开图片
            image = Image.open(image_path)
            
            # 创建绘图对象
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(image)
            
            # 尝试使用系统字体，如果失败则使用默认字体
            try:
                # Windows系统字体
                font = ImageFont.truetype("arial.ttf", self.font_size)
            except:
                try:
                    # macOS系统字体
                    font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", self.font_size)
                except:
                    try:
                        # Linux系统字体
                        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", self.font_size)
                    except:
                        # 使用默认字体
                        font = ImageFont.load_default()
            
            # 获取文本尺寸
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # 根据位置参数计算水印位置
            img_width, img_height = image.size
            
            if self.position == 'top_left':
                x, y = 10, 10
            elif self.position == 'top_center':
                x, y = (img_width - text_width) // 2, 10
            elif self.position == 'top_right':
                x, y = img_width - text_width - 10, 10
            elif self.position == 'center':
                x, y = (img_width - text_width) // 2, (img_height - text_height) // 2
            elif self.position == 'bottom_left':
                x, y = 10, img_height - text_height - 10
            elif self.position == 'bottom_center':
                x, y = (img_width - text_width) // 2, img_height - text_height - 10
            else:  # 默认为右下角
                x, y = img_width - text_width - 10, img_height - text_height - 10
            
            # 绘制水印（添加半透明背景）
            # 先绘制背景矩形
            background_color = (0, 0, 0, 128)  # 黑色半透明
            draw.rectangle([x-5, y-5, x+text_width+5, y+text_height+5], fill=background_color)
            
            # 绘制文本
            draw.text((x, y), watermark_text, font=font, fill=self.font_color)
            
            # 保存图片
            image.save(output_path)
            return True
        except Exception as e:
            print(f"添加水印时出错: {e}")
            return False


def get_image_files(directory):
    """
    获取目录下的所有图片文件
    :param directory: 目录路径
    :return: 图片文件列表
    """
    image_extensions = ('.jpg', '.jpeg', '.png', '.tiff', '.tif')
    image_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(image_extensions):
                image_files.append(os.path.join(root, file))
    
    return image_files


def create_watermark_directory(original_directory):
    """
    创建水印目录
    :param original_directory: 原始目录路径
    :return: 水印目录路径
    """
    watermark_dir = os.path.join(original_directory, os.path.basename(original_directory) + "_watermark")
    if not os.path.exists(watermark_dir):
        os.makedirs(watermark_dir)
    return watermark_dir