# PhotoWatermark

PhotoWatermark 是一个Python程序，用于自动在图片上添加基于拍摄时间的文本水印。该程序读取图片的EXIF信息，提取拍摄时间，并将该时间作为水印添加到图片上。

## 版本

当前版本: v1.0.0

## 功能特点

- 自动读取图片EXIF信息中的拍摄时间
- 支持自定义水印字体大小、颜色和位置
- 批量处理图片并保存到指定目录
- 支持多种图片格式（JPG, PNG, TIFF等）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
python main.py
```

按照提示输入图片路径和水印设置即可。

### 详细使用步骤

1. 运行程序：
   ```bash
   python main.py
   ```

2. 输入图片文件路径或包含图片的目录路径

3. 选择水印位置：
   - 1. 左上角 (top_left)
   - 2. 顶部中央 (top_center)
   - 3. 右上角 (top_right)
   - 4. 中央 (center)
   - 5. 左下角 (bottom_left)
   - 6. 底部中央 (bottom_center)
   - 7. 右下角 (bottom_right) [默认]

4. 输入字体大小（默认20）

5. 输入字体颜色(R,G,B)（默认255,255,255即白色）

6. 程序会自动处理图片并将添加水印后的图片保存到原目录名+"_watermark"的新目录下

## 项目结构

```
PhotoWatermark/
├── main.py              # 主程序入口
├── watermark_processor.py  # 水印处理核心模块
├── exif_reader.py       # EXIF信息读取模块
├── requirements.txt     # 依赖包列表
└── README.md            # 项目说明文档
```

## 技术实现

- 使用Pillow库处理图片和绘制水印
- 使用ExifRead库读取EXIF信息
- 自动适配不同操作系统的字体
- 添加了半透明背景以提高水印可读性