import pygame as pg
import random
import sys
import time
from pygame.locals import K_SPACE, K_LSHIFT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
GREEN = (0, 255, 0)
YELLOW = (225, 225, 0)
RED = (255, 0, 0)

FPS = 30
display_width = 800
display_height = 600

pg.init()
display = pg.display.set_mode((display_width, display_height))
pg.display.set_caption("KEYBOARD SIMULATOR")
clock = pg.time.Clock()
font = pg.font.Font(None, 32)
input_box = pg.Rect(50, 525, 700, 30)
text_box = pg.Rect(50, 80, 700, 150)
notifications = (300, 15)
font_type = 'font.ttf'

textAlignLeft = 0
textAlignRight = 1
textAlignCenter = 2
textAlignBlock = 3


# Функция, которая импортирует заданный текст в прямоугольник, из которого показывается текст
# Документация этой функции будет чуть позже
def draw_text(surface, text, color, rect, align=textAlignLeft):
    line_space = 10  # растояние между строками
    space_width = 10   # растояние между словами
    list_of_words = text.split(" ")
    image_list = [font.render(word, True, color) for word in list_of_words]
    max_len = rect[2] - 10
    line_len_list = [0]
    line_list = [[]]
    for image in image_list:
        width = image.get_width()
        line_len = line_len_list[-1] + len(line_list[-1]) * space_width + width
        if len(line_list[-1]) == 0 or line_len <= max_len:
            line_len_list[-1] += width
            line_list[-1].append(image)
        else:
            line_len_list.append(width)
            line_list.append([image])

    line_bottom = rect[1]
    last_line = 0
    for line_len, lineImages in zip(line_len_list, line_list):
        line_left = rect[0] + 10
        if align == textAlignRight:
            line_left += + rect[2] - line_len - space_width * (len(lineImages)-1)
        elif align == textAlignCenter:
            line_left += (rect[2] - line_len - space_width * (len(lineImages)-1)) // 2
        elif align == textAlignBlock and len(lineImages) > 1:
            space_width = (rect[2] - line_len) // (len(lineImages)-1)
        if line_bottom + line_space > rect[1] + rect[3]:
            break
        last_line += 1
        for i, image in enumerate(lineImages):
            x, y = line_left + i*space_width, line_bottom
            surface.blit(image, (round(x), y))
            line_left += image.get_width()
        line_bottom += line_space + line_space

    if last_line < len(line_list):
        draw_words = sum([len(line_list[i]) for i in range(last_line)])
        remaining_text = ""
        for text in list_of_words[draw_words:]:
            remaining_text += text + " "
        return remaining_text
    return ""


# Проверка вводимого символа на совпадение с нужным
def check_letter(event, cnt, text):
    if cnt >= len(text):
        return "end_of_file"
    else:
        if event == text[cnt]:
            return "True"
        else:
            return "False"


# Экспорт игровых данных: скорости и количества ошибок
def export_of_data(speed, mistakes):
    f = open('data.txt', 'w')
    f.write("speed:\n" + str(speed) + '\n')
    f.write("mistakes:\n" + str(mistakes))
    f.close()


# Импорт скорости печатания
def import_of_speed():
    f = open('data.txt')
    speed = f.read().split('\n')[1]
    return speed


# Импорт количества ошибок
def import_of_mistakes():
    f = open('data.txt')
    mistakes = list(str(f.read()).split('\n'))[3]
    return mistakes


# Импорт текста путем рандома из файлов, которые есть в папке
def import_text():
    arr_texts = ['texts/1.txt', 'texts/2.txt', 'texts/3.txt', 'texts/4.txt', 'texts/5.txt']
    f = open(arr_texts[random.randint(0, 4)])
    words = f.read()
    words = words[:-1]
    f.close()
    return words


# Создание клавиатуры на окне
def keyboard_creation():
    keyboard = pg.image.load('keyboard2.jpg')
    display.blit(keyboard, (50, 250))


# Написание текста
def print_text(message, font_color, place, font_size):
    font_of_notifications = pg.font.Font(font_type, font_size)
    text = font_of_notifications.render(message, True, font_color)
    display.blit(text, place)


# При окончании набора текста вызывается эта функция
# Она выводит игровые данные и предлагает заново начать игру
def end_of_game(general_time, mistakes, text):
    try_again_button = pg.image.load("try-again.png")
    while True:
        symbols_per_second = round(len(text) / general_time, 2)
        export_of_data(symbols_per_second, mistakes)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if 500 <= pg.mouse.get_pos()[0] <= 500 + try_again_button.get_width() and 120 <= pg.mouse.get_pos()[1] <= 120 + try_again_button.get_height():
                    run_klav()
        display.fill(WHITE)
        display.blit(bg.image, bg.rect)
        clock.tick(FPS)
        print_text("THE END OF GAME", BLACK, (200, 15), 60)
        accuracy = round((len(text) - mistakes)/len(text), 2) * 100
        print_text("Symbols per second ---", BLACK, (50, 500), 20)
        print_text(str(symbols_per_second), BLACK, (250, 500), 20)
        print_text("Mistakes ---", BLACK, (600, 500), 20)
        print_text(str(mistakes), BLACK, (720, 500), 20)

        print_text("Total number of typed symbols", BLACK, (text_box.x + 10, text_box.y + 10), 20)
        print_text("---  " + str(len(text)), BLACK, (text_box.x + 300, text_box.y + 10), 20)

        print_text("Total number of mistakes", BLACK, (text_box.x + 10, text_box.y + 30), 20)
        print_text("---  " + str(mistakes), BLACK, (text_box.x + 300, text_box.y + 30), 20)

        print_text("Accuracy", BLACK, (text_box.x + 10, text_box.y + 50), 20)
        print_text("---  " + str(accuracy) + "%", BLACK, (text_box.x + 300, text_box.y + 50), 20)

        print_text("Symbols per second", BLACK, (text_box.x + 10, text_box.y + 70), 20)
        print_text("---  " + str(symbols_per_second), BLACK, (text_box.x + 300, text_box.y + 70), 20)

        keyboard_creation()
        input_text = font.render("You typed all the text", True, BLACK)
        display.blit(input_text, (input_box.x + input_box.w * 0.3, input_box.y + 5))

        display.blit(try_again_button, (500, 120))
        pg.draw.rect(display, GRAY, input_box, 3)
        pg.draw.rect(display, BLACK, text_box, 3)
        pg.display.update()


class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


bg = Background('back.jpg', [0, 0])

def run_klav():
    game = True
    keyboard_is_active = False
    text_of_input = 'Нажмите, чтобы ввести текст'
    cnt_in_text = 0
    mistakes = 0
    color_of_input = GRAY
    timer_for_mistakes = 0
    timer_of_game = 0
    import_text_str = import_text()
    symbols_per_second = 0
    last_speed = import_of_speed()
    last_num_of_mistakes = import_of_mistakes()
    last_data = "Your previous result is: Speed - " + str(last_speed) + " Mistakes - " + str(last_num_of_mistakes)
    dct = {}
    while game:
        display.fill(WHITE)
        display.blit(bg.image, bg.rect)
        print_text(last_data, BLACK, (50, 20), 32)
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if input_box.x <= pg.mouse.get_pos()[0] <= input_box.x + input_box.w\
                        and input_box.y <= pg.mouse.get_pos()[1] <= input_box.y + input_box.h:
                    keyboard_is_active = True
                    color_of_input = BLACK
                    last_data = ''
                    if text_of_input == "Нажмите, чтобы ввести текст":
                        text_of_input = ''
                        timer_of_game = time.time()
                else:
                    keyboard_is_active = False
            if event.type == pg.KEYDOWN:
                if keyboard_is_active:
                    if check_letter(event.unicode, cnt_in_text, import_text_str) == "True":
                        cnt_in_text += 1
                        dct.get(event.unicode)
                        text_of_input += event.unicode
                        if event.key == K_SPACE:
                            text_of_input = ''
                    elif check_letter(event.unicode, cnt_in_text, import_text_str) == "end_of_file":
                        end_of_game(time.time() - timer_of_game, mistakes, import_text_str)
                    else:
                        if event.key != K_LSHIFT:
                            mistakes += 1
                            timer_for_mistakes = time.time() + 0.5
        symbols_per_second = round(cnt_in_text / (time.time() - timer_of_game), 2)
        print_text("Symbols per second ---", BLACK, (50, 500), 20)
        print_text(str(symbols_per_second), BLACK, (250, 500), 20)
        print_text("Mistakes ---", BLACK, (600, 500), 20)
        print_text(str(mistakes), BLACK, (720, 500), 20)
        if timer_for_mistakes - time.time() > 0:
            print_text("MISTAKE", RED, notifications, 60)
        keyboard_creation()
        input_text = font.render(text_of_input, True, BLACK)
        if keyboard_is_active:
            display.blit(input_text, (input_box.x + input_box.w * 0.4, input_box.y + 5))
        else:
            display.blit(input_text, (display_width / 3, input_box.y + 5))
        pg.draw.rect(display, color_of_input, input_box, 3)
        pg.draw.rect(display, BLACK, text_box, 3)
        draw_text(display, import_text_str, BLACK, text_box)
        pg.display.update()

run_klav()
