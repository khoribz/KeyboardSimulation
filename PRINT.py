import time

import pygame as pg

import COLOR
import GLOBAL


# Функция, которая импортирует заданный текст в прямоугольник, из которого показывается текст
def draw_text(screen, text, color, rect):
    line_space = 20  # растояние между строками
    space_width = 10   # растояние между словами
    list_of_words = text.split(" ")  # разделяем текст на слова и кладем в лист
    image_list = [GLOBAL.font.render(word, True, color) for word in list_of_words]   # получаем лист из картинок слов
    max_len = rect[2] - 15  # устанавливаем максимальную длину строки, отступ справа 15
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
        line_left = rect[0] + 10  # левая граница нашего текста в текущий момент времени, изначальный отступ слева 10
        for i, image in enumerate(lineImages):   # пробегаемся по всем словам и печатаем их
            x, y = line_left + i * space_width, line_bottom
            screen.blit(image, (x, y))
            line_left += image.get_width()
        lines += 1
        line_bottom += line_space


# Написание текста
# message - что написать
# font_color - каким цветом написать
# place - в каком месте написать
# font_size - размер шрифта
def print_text(message, font_color, place, font_size):
    font_of_notifications = pg.font.Font(GLOBAL.font_type, font_size)
    text = font_of_notifications.render(message, True, font_color)
    GLOBAL.display.blit(text, place)


# Вывод переменных скорости и ошибок в окно
def print_mistakes_and_speed(symbols_per_second, mistakes):
    place_for_speed = (250, 500)
    font_size_for_speed = 20
    place_for_mistakes = (720, 500)
    font_size_for_mistakes = 20
    print_text(str(symbols_per_second), COLOR.BLACK, place_for_speed, font_size_for_speed)
    print_text(str(mistakes), COLOR.BLACK, place_for_mistakes, font_size_for_mistakes)


# Функция начинает работать при завершении ввода текста
# Она печатает статистику последнего сеанса
def print_for_end(text, symbols_per_second, mistakes, accuracy):
    print_mistakes_and_speed(symbols_per_second, mistakes)
    font_size = 20
    top_indent = 10
    left_indent_for_data = 300
    left_indent_for_words = 10
    changing_indent_y = top_indent

    print_text("Total number of typed symbols", COLOR.BLACK, (GLOBAL.text_box.x + left_indent_for_words,
                                                              GLOBAL.text_box.y + changing_indent_y), font_size)
    print_text("---  " + str(len(text)), COLOR.BLACK, (GLOBAL.text_box.x + left_indent_for_data,
                                                       GLOBAL.text_box.y + changing_indent_y), font_size)
    changing_indent_y += font_size

    print_text("Total number of mistakes", COLOR.BLACK, (GLOBAL.text_box.x + left_indent_for_words,
                                                         GLOBAL.text_box.y + changing_indent_y), font_size)
    print_text("---  " + str(mistakes), COLOR.BLACK, (GLOBAL.text_box.x + left_indent_for_data,
                                                      GLOBAL.text_box.y + changing_indent_y), font_size)
    changing_indent_y += font_size

    print_text("Accuracy", COLOR.BLACK, (GLOBAL.text_box.x + left_indent_for_words,
                                         GLOBAL.text_box.y + changing_indent_y), font_size)
    print_text("---  " + str(accuracy) + "%", COLOR.BLACK, (GLOBAL.text_box.x + left_indent_for_data,
                                                            GLOBAL.text_box.y + changing_indent_y), font_size)
    changing_indent_y += font_size

    print_text("Symbols per second", COLOR.BLACK, (GLOBAL.text_box.x + left_indent_for_words,
                                                   GLOBAL.text_box.y + changing_indent_y), font_size)
    print_text("---  " + str(symbols_per_second), COLOR.BLACK, (GLOBAL.text_box.x + left_indent_for_data,
                                                                GLOBAL.text_box.y + changing_indent_y), font_size)


# появление надписи MISTAKE на время timer_for_mistakes
def print_word_mistake(timer_for_mistakes):
    place_for_mistake = (300, 15)
    font_size_for_mistakes = 60
    if timer_for_mistakes - time.time() > 0:
        print_text("MISTAKE", COLOR.RED, place_for_mistake, font_size_for_mistakes)


# отрисовка вводимого текста: положение зависит от того, нажималось ли на окно ввода
def draw_input_text(keyboard_is_active, text_of_input):
    input_text_image = GLOBAL.font.render(text_of_input, True, COLOR.BLACK)
    top_indent = 5
    location_for_input_box_on = GLOBAL.input_box.x + GLOBAL.input_box.w * 0.4
    location_for_input_box_off = GLOBAL.display_width / 3
    if keyboard_is_active:
        GLOBAL.display.blit(input_text_image, (location_for_input_box_on, GLOBAL.input_box.y + top_indent))
    else:
        GLOBAL.display.blit(input_text_image, (location_for_input_box_off, GLOBAL.input_box.y + top_indent))
