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
font_type = 'font.ttf'


# класс для создания фона окна
class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


bg = Background('back.jpg', [0, 0])


# Функция, которая импортирует заданный текст в прямоугольник, из которого показывается текст
# Документация этой функции будет чуть позже
def draw_text(screen, text, color, rect):
    line_space = 20  # растояние между строками
    space_width = 10   # растояние между словами
    list_of_words = text.split(" ")  # разделяем текст на слова и кладем в лист
    image_list = [font.render(word, True, color) for word in list_of_words]   # получаем лист из картинок слов
    max_len = rect[2] - 15  # устанавливаем максимальную длину строки
    line_len_list = [0]  # лист из длин полученных строк
    line_list = [[]]  # лист из полученных строк
    for image in image_list:
        width = image.get_width()
        # длина строки вычисляется как число символов, уже имеющееся в строке,
        # + кол-во слов в строке * длина пробела между словами + длина следующего слова
        line_len = line_len_list[-1] + len(line_list[-1]) * space_width + width
        if line_len <= max_len:  # если строка помещается в нашу область
            line_len_list[-1] += width  # добавляем к имеющейся длине строки размер нового слова
            line_list[-1].append(image)  # добавляем слово в лист состоящий из строк
        else:  # если строка не помещается в нашу область
            line_len_list.append(width)  # добавляем в лист размера строк размер нового слова на следующей строке
            line_list.append([image])  # добавляем в лист следующую строку
    line_bottom = rect[1]  # нижняя граница нашего текста в текущий момент времени
    lines = 0  # количество строк
    for lineImages in line_list:  # пробегаемся по всем строкам
        if line_bottom + line_space > rect[1] + rect[3]:
            break
        line_left = rect[0] + 10  # левая граница нашего текста в текущий момент времени
        for i, image in enumerate(lineImages):   # пробегаемся по всем словам и печатаем их
            x, y = line_left + i * space_width, line_bottom
            screen.blit(image, (x, y))
            line_left += image.get_width()
        lines += 1
        line_bottom += line_space


# Проверка вводимого символа на совпадение с правильным
# event - поступивший символ
# cnt - счетчик по строке из файла, по этому индексу сверяется event
# text - текст который нужно ввести в виде строки
def check_letter(event, cnt, text):
    if cnt >= len(text):
        return "end_of_file"
    else:
        if event == text[cnt]:
            return "True"
        else:
            return "False"


# Экспорт игровых данных: скорости и количества ошибок
# speed - скорость игрока в последнем сеансе
# mistakes - количество ошибок игрока в последнем сеансе
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
    f = open(arr_texts[random.randint(0, len(arr_texts) - 1)])
    words = f.read()
    words = words[:-1]
    f.close()
    return words


# Создание клавиатуры на окне
def keyboard_creation():
    keyboard = pg.image.load('keyboard2.jpg')
    display.blit(keyboard, (50, 250))


# Написание текста
# message - что написать
# font_color - каким цветом написать
# place - в каком месте написать
# font_size - размер шрифта
def print_text(message, font_color, place, font_size):
    font_of_notifications = pg.font.Font(font_type, font_size)
    text = font_of_notifications.render(message, True, font_color)
    display.blit(text, place)


# Создание макета окна клавиатурного тренажера
def create_window():
    display.fill(WHITE)
    display.blit(bg.image, bg.rect)
    clock.tick(FPS)
    keyboard_creation()
    print_text("Symbols per second ---", BLACK, (50, 500), 20)
    print_text("Mistakes ---", BLACK, (600, 500), 20)


# Вывод переменных скорости и ошибок в окно
def print_mistakes_and_speed(symbols_per_second, mistakes):
    print_text(str(symbols_per_second), BLACK, (250, 500), 20)
    print_text(str(mistakes), BLACK, (720, 500), 20)


# Функция начинает работать при завершении ввода текста
# Она печатает статистику последнего сеанса
def print_for_end(text, symbols_per_second, mistakes, accuracy):
    print_mistakes_and_speed(symbols_per_second, mistakes)

    print_text("Total number of typed symbols", BLACK, (text_box.x + 10, text_box.y + 10), 20)
    print_text("---  " + str(len(text)), BLACK, (text_box.x + 300, text_box.y + 10), 20)

    print_text("Total number of mistakes", BLACK, (text_box.x + 10, text_box.y + 30), 20)
    print_text("---  " + str(mistakes), BLACK, (text_box.x + 300, text_box.y + 30), 20)

    print_text("Accuracy", BLACK, (text_box.x + 10, text_box.y + 50), 20)
    print_text("---  " + str(accuracy) + "%", BLACK, (text_box.x + 300, text_box.y + 50), 20)

    print_text("Symbols per second", BLACK, (text_box.x + 10, text_box.y + 70), 20)
    print_text("---  " + str(symbols_per_second), BLACK, (text_box.x + 300, text_box.y + 70), 20)


# При окончании набора текста вызывается эта функция
# Она выводит игровые данные и предлагает заново начать игру
# general_time - общее время ввода текста
# mistakes - количество ошибок за сеанс
# text - текст, который вводился
def end_of_game(general_time, mistakes, text):
    try_again_button = pg.image.load("try-again.png")  # загружается изображение кнопки "TRY AGAIN"
    while True:
        symbols_per_second = round(len(text) / general_time, 2)  # количество символов в секунду с округлением до 2 знаков
        export_of_data(symbols_per_second, mistakes)  # загрузка статистики сеанса в data.txt
        try_again_button_coord = (500, 120)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:  # если нажимается кнопка TRY AGAIN запускается все по новой
                if try_again_button_coord[0] <= pg.mouse.get_pos()[0] <= try_again_button_coord[0] + try_again_button.get_width()\
                      and try_again_button_coord[1] <= pg.mouse.get_pos()[1] <= try_again_button_coord[1] + try_again_button.get_height():
                    run_klav()
        create_window()  # создается окно тренажера
        print_text("THE END OF INPUT", BLACK, (200, 15), 60)
        accuracy = round((len(text) - mistakes)/len(text), 2) * 100  # точность ввода
        print_for_end(text, symbols_per_second, mistakes, accuracy)
        input_text = font.render("You typed all the text", True, BLACK)
        display.blit(input_text, (input_box.x + input_box.w * 0.3, input_box.y + 5))
        display.blit(try_again_button, (500, 120))
        pg.draw.rect(display, GRAY, input_box, 3)
        pg.draw.rect(display, BLACK, text_box, 3)
        pg.display.update()


# появление надписи MISTAKE на время timer_for_mistakes
def print_word_mistake(timer_for_mistakes):
    if timer_for_mistakes - time.time() > 0:
        print_text("MISTAKE", RED, (300, 15), 60)


# отрисовка вводимого текста: положение зависит от того, нажималось ли на окно ввода
def draw_input_text(keyboard_is_active, text_of_input):
    input_text_image = font.render(text_of_input, True, BLACK)
    if keyboard_is_active:
        display.blit(input_text_image, (input_box.x + input_box.w * 0.4, input_box.y + 5))
    else:
        display.blit(input_text_image, (display_width / 3, input_box.y + 5))


# основная функция, обрабатывающая нажатия
def run_klav():
    keyboard_is_active = False  # нажималось ли на окно ввода
    text_of_input = 'Нажмите, чтобы ввести текст' # текст в окне ввода
    cnt_in_text = 0  # какой сейчас символ проверяется
    mistakes = 0  # количество совершенных ошибок
    color_of_input = GRAY  # цвет окна ввода
    timer_for_mistakes = 0  # таймер нужный для вывода надписи MISTAKE на определенное время
    timer_of_game = 0  # таймер для подсчета времени сеанса
    import_text_str = import_text()  # строка, в которую импортируется текст из файла
    last_data = "Your previous result is: Speed - " + str(import_of_speed()) +\
        " Mistakes - " + str(import_of_mistakes())  # строка со статистикой прошлого запуска
    while True:
        create_window()  # создание окна тренажера
        print_text(last_data, BLACK, (50, 20), 32)  # вывод статистики прошлого запуска
        draw_text(display, import_text_str, BLACK, text_box)  # отображение в окне текста, который нужно набрать
        for event in pg.event.get():  # обработка событий
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # проверка нажато ли окно ввода текста, если да - оно активируется
                if input_box.x <= pg.mouse.get_pos()[0] <= input_box.x + input_box.w\
                        and input_box.y <= pg.mouse.get_pos()[1] <= input_box.y + input_box.h:
                    keyboard_is_active = True
                    color_of_input = BLACK
                    last_data = ''  # исчезает статистика прошлого запуска
                    if text_of_input == "Нажмите, чтобы ввести текст":
                        text_of_input = ''  # окно ввода становится пустым
                        timer_of_game = time.time()  # запускается таймер сеанса
            if event.type == pg.KEYDOWN:  # если нажата кнопка на клавиатуре
                if keyboard_is_active:  # если клавиатура активирована
                    if check_letter(event.unicode, cnt_in_text, import_text_str) == "True":
                        # если символ правильный
                        cnt_in_text += 1  # счетчик сдвигается на проверку следующего символа
                        text_of_input += event.unicode  # добавление символа в text_of_input
                        if event.key == K_SPACE:  # если нажат пробел, стирается слово
                            text_of_input = ''
                    elif check_letter(event.unicode, cnt_in_text, import_text_str) == "end_of_file":
                        # если файл закончился переходим в функцию end_of_game
                        end_of_game(time.time() - timer_of_game, mistakes, import_text_str)
                    else:
                        if event.key != K_LSHIFT:  # чтобы дать пользователю время при печатании
                            # заглавных букв дотянуться от SHIFT до клавиши, и это не было ошибкой
                            mistakes += 1
                            timer_for_mistakes = time.time() + 0.5  # задержка MISTAKE на 0.5 секунд
        symbols_per_second = round(cnt_in_text / (time.time() - timer_of_game), 2)  # подсчет скорости
        print_word_mistake(timer_for_mistakes)  # надпись MISTAKE при ошибке
        print_mistakes_and_speed(symbols_per_second, mistakes)  # вывод переменных скорости и ошибок
        draw_input_text(keyboard_is_active, text_of_input)  # отрисовка вводимого слова
        pg.draw.rect(display, color_of_input, input_box, 3)  # отрисовка окна ввода
        pg.draw.rect(display, BLACK, text_box, 3)  # отрисовка окна с текстом
        pg.display.update()


run_klav()
