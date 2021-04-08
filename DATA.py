import random


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
    f.close()
    return speed


# Импорт количества ошибок
def import_of_mistakes():
    f = open('data.txt')
    mistakes = list(str(f.read()).split('\n'))[3]
    f.close()
    return mistakes


# Импорт текста путем рандома из файлов, которые есть в папке
def import_text():
    arr_texts = ['texts/1.txt', 'texts/2.txt', 'texts/3.txt', 'texts/4.txt', 'texts/5.txt',
                 'texts/6.txt', 'texts/7.txt', 'texts/8.txt', 'texts/9.txt', 'texts/10.txt']
    f = open(arr_texts[random.randint(0, len(arr_texts) - 1)])
    words = f.read()
    words = words[:-1]
    f.close()
    return words
