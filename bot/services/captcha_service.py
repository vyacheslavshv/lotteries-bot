from random import randint
from captcha.image import ImageCaptcha


class CaptchaService:
    def __init__(self, event):
        self.event = event

    @staticmethod
    async def generate_captcha():
        code = str(randint(1000, 9999))

        image_captcha = ImageCaptcha(width=350, height=150)
        image_bytes = image_captcha.generate(code)
        image_bytes.seek(0)

        return image_bytes, code
