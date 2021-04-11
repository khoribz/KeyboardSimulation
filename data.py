import random


def export_of_data(speed, mistakes):
    """
    Экспорт игровых данных: скорости и количества ошибок
    :param speed: скорость игрока в последнем сеансе
    :param mistakes: количество ошибок игрока в последнем сеансе
    """
    with open('data.txt', 'w') as data_file:
        data_file.write("speed:\n" + str(speed) + '\n')
        data_file.write("mistakes:\n" + str(mistakes))


def import_of_speed():
    """
    Импорт скорости печатания
    :return: показатель скорости
    """
    with open('data.txt') as data_file:
        speed = data_file.read().split('\n')[1]
    return speed


def import_of_mistakes():
    """
    Импорт количества ошибок
    :return: количество ошибок
    """
    with open('data.txt') as data_file:
        mistakes = data_file.read().split('\n')[3]
    return mistakes


def import_text():
    """
    Импорт текста путем рандома из файлов, которые есть в папке
    :return: строка с текстом из файла
    """
    arr_texts = ['texts/1.txt', 'texts/2.txt', 'texts/3.txt', 'texts/4.txt', 'texts/5.txt',
                 'texts/6.txt', 'texts/7.txt', 'texts/8.txt', 'texts/9.txt', 'texts/10.txt']
    with open(arr_texts[random.randint(0, len(arr_texts) - 1)]) as data_file:
        words = data_file.read()
        words = words[:-1]
    return words
