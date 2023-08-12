from PIL import Image
from utils.point import Point
import math

class GIF_Generator:
    def __init__(self):
        self.frame = []
    
    def sliding_window(self, image_path, window_size: Point, start: Point, end: Point, step: int):
        image = Image.open(image_path).convert('RGBA')
        step = abs(step)
        
        try:
            m = (end.y - start.y) / (end.x - start.x)
            b = start.y - m * start.x

            if abs(m) > 1:
                step = -step if end.y - start.y < 0 else step

                for y in range(start.y, end.y, step):
                    x = int((y - b) / m)
                    self.frame.append(image.crop((x, y, x + window_size.x, y + window_size.y)))

            else:
                step = -step if end.x - start.x < 0 else step

                for x in range(start.x, end.x, step):
                    y = int(m * x + b)
                    self.frame.append(image.crop((x, y, x + window_size.x, y + window_size.y)))

        except ZeroDivisionError:
            step = -step if end.y - start.y < 0 else step

            for y in range(start.y, end.y, step):
                self.frame.append(image.crop((start.x, y, start.x + window_size.x, y + window_size.y)))

    def reverse(self):
        self.frame += self.frame[-2::-1]

    # 淡出動畫
    def fade_out(self, images_path: list, fps: int = 60, pause: int = 1):
        pause = pause if pause >= 1 else 1
        images = []

        for path in images_path:
            images.append(Image.open(path).convert('RGBA'))
            
            if images and images[-1].size != images[0].size:
                    images[-1] = images[-1].resize(images[0].size)

        for i in range(1, len(images)):
            for t in range(pause):
                self.frame.append(images[i - 1])
            
            for f in range(fps):
                self.frame.append(Image.blend(images[i - 1], images[i], f / fps))
    
    # to generate the gif
    def generate(self, filename: str, duration: int = 100, loop: int = 0):
        self.frame[0].save(filename, save_all = True, append_images = self.frame[1:], duration = duration, loop = loop)