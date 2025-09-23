# PhotoWatermark

PhotoWatermark 是一个Python程序，用于自动在图片上添加基于拍摄时间的文本水印。该程序读取图片的EXIF信息，提取拍摄时间，并将该时间作为水印添加到图片上。

## 功能特点

- 自动读取图片EXIF信息中的拍摄时间
- 支持自定义水印字体大小、颜色和位置
- 批量处理图片并保存到指定目录

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
python main.py
```

按照提示输入图片路径和水印设置即可。