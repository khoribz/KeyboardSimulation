import time

import pygame as pg

import color
import functions
import global_file


def draw_text(screen, text, color_of_text, rect):
    """
    Функция, которая импортирует заданный текст в прямоугольник, из которого показывается текст
    :param screen: дисплей, на котором прорисовывается текст
    :param text: текст, который нужно написать
    :param color_of_text: цвет текста, который нужно написать
    :param rect: прямоугольник,в котором нужно написать текст
    """
    rect_x = rect[0]  # координата X нашего окна
    rect_y = rect[1]  # координата У нашего окна
    rect_w = rect[2]  # ширина нашего окна
    rect_h = rect[3]  # высота нашего окна
    line_space = 20  # расстояние между строками
    space_width = 10  # расстояние между словами
    list_of_words = text.split()  # разделяем текст на слова и кладем в лист
    # image_list - получаем лист из картинок слов
    image_list = [global_file.font.render(word, True, color_of_text) for word in list_of_words]
    right_indent = 15  # отступ справа 15
    max_len = rect_w - right_indent  # устанавливаем максимальную длину строки с определенным отступом справа
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
    line_bottom = rect_y  # координата У нашего текста в текущий момент времени
    lines = 0  # количество строк
    height_of_rect = rect_y + rect_h
    for lineImages in line_list:  # пробегаемся по всем строкам
        if line_bottom + line_space > height_of_rect:  # если при переносе очередной строки выходим
            # вниз за границы окна, останавливаем вывод текста
            break
        left_indent = 10  # отступ слева 10
        # line_left - левая граница нашего текста в текущий момент времени с определенным отступом слева 10
        line_left = rect_x + left_indent
        for i, image in enumerate(lineImages):  # пробегаемся по всем словам в строке и печатаем их
            x, y = line_left + i * space_width, line_bottom
            # координата x задается левым отступом и количеством пробелов
            screen.blit(image, (x, y))
            line_left += image.get_width()  # левый отступ увеличивается на ширину добавленного слова
        lines += 1  # переходим на следующую строку
        line_bottom += line_space  # увеличиваем координату У нашего текста на расстояние между строками


def print_text(message, font_color, place, font_size):
    """
    Вывод текста на экран
    :param message: содержимое текста
    :param font_color: цвет текста
    :param place: место текста
    :param font_size: размер текста
    """
    font_of_notifications = pg.font.Font(global_file.font_type, font_size)
    text = font_of_notifications.render(message, True, font_color)
    global_file.display.blit(text, place)


def print_mistakes_and_speed(symbols_per_second, mistakes):
    """
    Вывод переменных скорости и ошибок в окно
    :param symbols_per_second: количество символов в секунду
    :param mistakes: количество ошибок
    """
    place_for_speed = (250, 500)
    font_size_for_speed = 20
    place_for_mistakes = (720, 500)
    font_size_for_mistakes = 20
    print_text(str(symbols_per_second), color.BLACK, place_for_speed, font_size_for_speed)
    print_text(str(mistakes), color.BLACK, place_for_mistakes, font_size_for_mistakes)


def print_for_end(text, symbols_per_second, mistakes, accuracy, heatmap):
    """
    Функция начинает работать при завершении ввода текста
    Она печатает статистику последнего сеанса
    :param text: текст, который нужно написать
    :param symbols_per_second: количество символов в секунду
    :param mistakes: количество ошибок в секунду
    :param accuracy: точность набора текста
    :param heatmap: словарь из ошибочных символов
    """
    print_mistakes_and_speed(symbols_per_second, mistakes)
    font_size = 20
    top_indent = 10
    left_indent_for_data = 300
    left_indent_for_words = 10

    changing_indent_y = top_indent
    first_line = "Total number of typed symbols"
    print_text(first_line, color.BLACK, (global_file.text_box.x +
                                         left_indent_for_words, global_file.text_box.y + changing_indent_y), font_size)
    print_text(f"---  {len(text)}", color.BLACK, (global_file.text_box.x + left_indent_for_data,
                                                  global_file.text_box.y + changing_indent_y), font_size)

    changing_indent_y += font_size
    second_line = "Total number of mistakes"
    print_text(second_line, color.BLACK, (global_file.text_box.x +
                                          left_indent_for_words, global_file.text_box.y + changing_indent_y), font_size)
    print_text(f"---  {mistakes}", color.BLACK, (global_file.text_box.x + left_indent_for_data,
                                                 global_file.text_box.y + changing_indent_y), font_size)

    changing_indent_y += font_size
    third_line = "Accuracy"
    print_text(third_line, color.BLACK, (global_file.text_box.x + left_indent_for_words,
                                         global_file.text_box.y + changing_indent_y), font_size)
    print_text(f"---  {accuracy}%", color.BLACK, (global_file.text_box.x + left_indent_for_data,
                                                  global_file.text_box.y + changing_indent_y), font_size)

    changing_indent_y += font_size
    fourth_line = "Symbols per second"
    print_text(fourth_line, color.BLACK, (global_file.text_box.x +
                                          left_indent_for_words, global_file.text_box.y + changing_indent_y), font_size)
    print_text(f"---  {symbols_per_second}", color.BLACK, (global_file.text_box.x + left_indent_for_data,
                                                           global_file.text_box.y + changing_indent_y), font_size)

    changing_indent_y += font_size
    input_heatmap = functions.heatmap_sort(heatmap)
    fifth_line = "The most erroneous symbols"
    print_text(fifth_line, color.BLACK, (global_file.text_box.x +
                                         left_indent_for_words, global_file.text_box.y + changing_indent_y), font_size)
    print_text(f"---  {input_heatmap}", color.BLACK, (global_file.text_box.x + left_indent_for_data,
                                                      global_file.text_box.y + changing_indent_y), font_size)


def print_word_mistake(timer_for_mistakes):
    """
    Появление надписи MISTAKE на время timer_for_mistakes
    :param timer_for_mistakes: время, в течение которого отображается надпись
    """
    place_for_mistake = (300, 15)
    font_size_for_mistakes = 60
    text_for_mistake = "MISTAKE"
    if timer_for_mistakes - time.time() > 0:
        print_text(text_for_mistake, color.RED, place_for_mistake, font_size_for_mistakes)


def draw_input_text(keyboard_is_active, text_of_input):
    """
    Отрисовка вводимого текста: положение зависит от того, нажималось ли на окно ввода
    :param keyboard_is_active: активна ли клавиатура
    :param text_of_input: текст, который нужно вывести
    """
    input_text_image = global_file.font.render(text_of_input, True, color.BLACK)
    top_indent = 5
    coefficient_for_input_box_on = 0.4
    # input_box_on_indent - отступ вводимого текста от края окна вывода во время включенной клавиатуры
    input_box_on_indent = global_file.input_box.w * coefficient_for_input_box_on
    location_for_input_box_on = global_file.input_box.x + input_box_on_indent
    # location_for_input_box_off - отступ текста от края окна вывода, если клавиатура неактивна
    coefficient_for_input_box_off = 0.3
    location_for_input_box_off = global_file.display_width * coefficient_for_input_box_off
    box_on = (location_for_input_box_on, global_file.input_box.y + top_indent)
    box_off = (location_for_input_box_off, global_file.input_box.y + top_indent)
    box = box_on if keyboard_is_active else box_off
    global_file.display.blit(input_text_image, box)
