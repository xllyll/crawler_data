import base64
import os


# 保存图片
def save_base64_to_png(base64_str, output_path):
    try:
        # 去除可能存在的Base64前缀
        if ',' in base64_str:
            base64_str = base64_str.split(',',  1)[1]()

        # 解码Base64数据
        image_data = base64.b64decode(base64_str)

        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path),  exist_ok=True)

        # 写入文件
        with open(output_path, 'wb') as f:
            f.write(image_data)
        print(f"图片已保存至: {output_path}")

    except Exception as e:
        print(f"保存失败: {str(e)}")