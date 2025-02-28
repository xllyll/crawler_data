from PIL import Image
import io
import pytesseract
from playwright.sync_api import sync_playwright
def get_captcha_text(image_data):
    """使用 Tesseract 识别验证码图片"""
    # 将图片数据转换为 PIL 图像对象
    image = Image.open(io.BytesIO(image_data))
    # 可选：对图片进行预处理（如灰度化、二值化等）
    # image = image.convert('L')  # 转换为灰度图
    # image = image.point(lambda x: 0 if x < 128 else 255, '1')  # 二值化

    # 使用 Tesseract 进行 OCR 识别
    captcha_text = pytesseract.image_to_string(image).strip()
    print(f"识别结果: {captcha_text}")
    return captcha_text