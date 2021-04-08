import pygame as pg


FPS = 30
display_width = 800
display_height = 600


# класс для создания фона окна
class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


bg = Background('pictures/back.jpg', [0, 0])  # создаем фон
pg.init()
display = pg.display.set_mode((display_width, display_height))  # устанавливаем размеры окна тренажера
pg.display.set_caption("KEYBOARD SIMULATOR")  # устанавливаем название окна тренажера
clock = pg.time.Clock()
font = pg.font.Font(None, 32)  # задаем размер шрифту
input_box = pg.Rect(50, 525, 700, 30)  # задаем размера окна ввода
text_box = pg.Rect(50, 80, 700, 150)  # задаем размеры окна, в котором отображается текст
font_type = 'fonts/font.ttf'  # устанавливаем шрифт
