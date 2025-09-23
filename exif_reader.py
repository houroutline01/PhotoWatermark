import exifread
from datetime import datetime


class EXIFReader:
    """读取图片EXIF信息的类"""
    
    @staticmethod
    def get_exif_data(image_path):
        """
        获取图片的EXIF数据
        :param image_path: 图片路径
        :return: EXIF数据字典
        """
        try:
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f)
            return tags
        except Exception as e:
            print(f"读取EXIF信息时出错: {e}")
            return None
    
    @staticmethod
    def extract_datetime(exif_data):
        """
        从EXIF数据中提取拍摄时间
        :param exif_data: EXIF数据字典
        :return: 拍摄时间字符串 (YYYY-MM-DD)
        """
        if not exif_data:
            return None
            
        # 查找日期时间标签
        datetime_tags = ['EXIF DateTimeOriginal', 'Image DateTime', 'EXIF DateTimeDigitized']
        
        for tag in datetime_tags:
            if tag in exif_data:
                try:
                    # 尝试解析日期时间
                    datetime_str = str(exif_data[tag])
                    # 通常格式为: 2023:01:15 14:30:22
                    dt = datetime.strptime(datetime_str, '%Y:%m:%d %H:%M:%S')
                    return dt.strftime('%Y-%m-%d')
                except ValueError:
                    continue
        
        return None