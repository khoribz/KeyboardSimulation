import pygame as pg


FPS = 30
display_width = 800
display_height = 600


class Background(pg.sprite.Sprite):
    """
    Класс для создания фона окна
    """
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


picture_for_back = "pictures/back.jpg"
place_for_back = [0, 0]
bg = Background(picture_for_back, place_for_back)  # создаем фон
pg.init()
display = pg.display.set_mode((display_width, display_height))  # устанавливаем размеры окна тренажера
name_of_display = "KEYBOARD SIMULATOR"
pg.display.set_caption(name_of_display)  # устанавливаем название окна тренажера
clock = pg.time.Clock()
font_size = 32
font = pg.font.Font(None, font_size)  # задаем размер шрифту

input_box_x = 50
input_box_y = 525
input_box_w = 700
input_box_h = 30
input_box = pg.Rect(input_box_x, input_box_y, input_box_w, input_box_h)  # задаем размера окна ввода

test_box_x = 50
test_box_y = 80
test_box_w = 700
test_box_h = 150
text_box = pg.Rect(test_box_x, test_box_y, test_box_w, test_box_h)  # задаем размеры окна, в котором отображается текст
font_type = 'fonts/font.ttf'  # устанавливаем шрифт
