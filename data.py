import os
import random


def export_of_data(speed, mistakes):
    """
    Экспорт игровых данных: скорости и количества ошибок
    :param speed: скорость игрока в последнем сеансе
    :param mistakes: количество ошибок игрока в последнем сеансе
    """
    with open('data.txt', 'w') as data_file:
        data_file.write(f'speed:\n{speed}\n')
        data_file.write(f'mistakes:\n{mistakes}\n')


def import_of_speed():
    """
    Импорт скорости печатания
    :return: показатель скорости
    """
    num_of_speed_line = 1
    with open('data.txt') as data_file:
        speed = data_file.read().split('\n')[num_of_speed_line]
    return speed


def import_of_mistakes():
    """
    Импорт количества ошибок
    :return: количество ошибок
    """
    num_of_mistakes_line = 3
    with open('data.txt') as data_file:
        mistakes = data_file.read().split('\n')[num_of_mistakes_line]
    return mistakes


def import_text():
    """
    Импорт текста путем рандома из файлов, которые есть в папке
    :return: строка с текстом из файла
    """
    list_of_files = os.listdir('texts')  # лист из текстов
    number_files = len(list_of_files)  # число текстов
    num_of_first_file = 1  # номер первого файла
    arr_texts = [f'texts/{i}.txt' for i in range(num_of_first_file, number_files)]
    with open(arr_texts[random.randint(0, len(arr_texts) - 1)]) as data_file:
        words = data_file.read()
    return words
