import operator

import color
import global_file
import print_file


def check_letter(event, cnt, text):
    """
    Проверка вводимого символа на совпадение с правильным
    :param event: поступивший символ
    :param cnt: счетчик по строке из файла, по этому индексу сверяется event
    :param text: текст который нужно ввести в виде строки
    :return: True - если символ совпал, False - если символ не совпал, end_of_file - если файл закончен
    """
    return_for_end = "end_of_file"
    if cnt >= len(text):
        return return_for_end
    else:
        return event == text[cnt]


def keyboard_creation():
    """
    Создание клавиатуры на окне
    """
    keyboard_image = "pictures/keyboard2.jpg"
    keyboard = global_file.pg.image.load(keyboard_image)
    keyboard_location = (50, 250)
    global_file.display.blit(keyboard, keyboard_location)


def heatmap_sort(heatmap):
    """
    Сортировка словаря ошибочных символов
    :param heatmap: словарь ошибочных символов
    :return: массив из не более, чем 3 пар ошибочных символов и их количества
    """
    sorted_keys = sorted(heatmap.items(), key=operator.itemgetter(1))
    sorted_keys.reverse()
    input_heatmap = []
    size_of_output_map = 3
    if len(sorted_keys) > size_of_output_map:
        for i in range(size_of_output_map):
            input_heatmap.append(sorted_keys[i])
    else:
        input_heatmap = list(sorted_keys)
    return input_heatmap


def create_window():
    """
    Создание макета окна клавиатурного тренажера
    """
    global_file.display.fill(color.WHITE)
    global_file.display.blit(global_file.bg.image, global_file.bg.rect)
    global_file.clock.tick(global_file.FPS)
    keyboard_creation()
    text_for_speed = "Symbols per second ---"
    place_for_speed = (50, 500)
    font_size_for_speed = 20
    text_for_mistakes = "Mistakes ---"
    place_for_mistakes = (600, 500)
    font_size_for_mistakes = 20
    print_file.print_text(text_for_speed, color.BLACK, place_for_speed, font_size_for_speed)
    print_file.print_text(text_for_mistakes, color.BLACK, place_for_mistakes, font_size_for_mistakes)
