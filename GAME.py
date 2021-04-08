import sys
import time

import pygame as pg
from pygame.locals import K_LSHIFT
from pygame.locals import K_SPACE

import COLOR
import DATA
import GLOBAL
import FUNCTIONS
import PRINT


# основная функция, обрабатывающая нажатия
def run_keyboard():
    keyboard_is_active = False  # нажималось ли на окно ввода
    text_of_input = 'Нажмите, чтобы ввести текст' # текст в окне ввода
    cnt_in_text = 0  # какой сейчас символ проверяется
    mistakes = 0  # количество совершенных ошибок
    color_of_input = COLOR.GRAY  # цвет окна ввода
    timer_for_mistakes = 0  # таймер нужный для вывода надписи MISTAKE на определенное время
    timer_of_game = 0  # таймер для подсчета времени сеанса
    import_text_str = DATA.import_text()  # строка, в которую импортируется текст из файла
    last_data = "Your previous result is: Speed - " + str(DATA.import_of_speed()) +\
        " Mistakes - " + str(DATA.import_of_mistakes())  # строка со статистикой прошлого запуска
    place_for_last_data = (50, 20)  # место, где выводятся данные прошлого сеанса
    font_size_for_last_data = 32  # шрифт для вывода данных прошлого сеанса
    while True:
        FUNCTIONS.create_window()  # создание окна тренажера
        PRINT.print_text(last_data, COLOR.BLACK, place_for_last_data, font_size_for_last_data)  # вывод статистики прошлого запуска
        PRINT.draw_text(GLOBAL.display, import_text_str, COLOR.BLACK, GLOBAL.text_box)  # отображение в окне текста, который нужно набрать
        for event in pg.event.get():  # обработка событий
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # проверка нажато ли окно ввода текста, если да - оно активируется
                if GLOBAL.input_box.x <= pg.mouse.get_pos()[0] <= GLOBAL.input_box.x + GLOBAL.input_box.w\
                        and GLOBAL.input_box.y <= pg.mouse.get_pos()[1] <= GLOBAL.input_box.y + GLOBAL.input_box.h:
                    keyboard_is_active = True
                    color_of_input = COLOR.BLACK
                    last_data = ''  # исчезает статистика прошлого запуска
                    if text_of_input == "Нажмите, чтобы ввести текст":
                        text_of_input = ''  # окно ввода становится пустым
                        timer_of_game = time.time()  # запускается таймер сеанса
            if event.type == pg.KEYDOWN:  # если нажата кнопка на клавиатуре
                if keyboard_is_active:  # если клавиатура активирована
                    if FUNCTIONS.check_letter(event.unicode, cnt_in_text, import_text_str) == "True":
                        # если символ правильный
                        cnt_in_text += 1  # счетчик сдвигается на проверку следующего символа
                        text_of_input += event.unicode  # добавление символа в text_of_input
                        if event.key == K_SPACE:  # если нажат пробел, стирается слово
                            text_of_input = ''
                    elif FUNCTIONS.check_letter(event.unicode, cnt_in_text, import_text_str) == "end_of_file":
                        # если файл закончился переходим в функцию end_of_game
                        end_of_game(time.time() - timer_of_game, mistakes, import_text_str)
                    else:
                        if event.key != K_LSHIFT:  # чтобы дать пользователю время при печатании
                            # заглавных букв дотянуться от SHIFT до клавиши, и это не было ошибкой
                            mistakes += 1
                            timer_for_mistakes = time.time() + 0.5  # задержка MISTAKE на 0.5 секунд
        symbols_per_second = round(cnt_in_text / (time.time() - timer_of_game), 2)  # подсчет скорости
        PRINT.print_word_mistake(timer_for_mistakes)  # надпись MISTAKE при ошибке
        PRINT.print_mistakes_and_speed(symbols_per_second, mistakes)  # вывод переменных скорости и ошибок
        PRINT.draw_input_text(keyboard_is_active, text_of_input)  # отрисовка вводимого слова

        rect_line_width = 3
        pg.draw.rect(GLOBAL.display, color_of_input, GLOBAL.input_box, rect_line_width)  # отрисовка окна ввода
        pg.draw.rect(GLOBAL.display, COLOR.BLACK, GLOBAL.text_box, rect_line_width)  # отрисовка окна с текстом
        pg.display.update()


# При окончании набора текста вызывается эта функция
# Она выводит игровые данные и предлагает заново начать игру
# general_time - общее время ввода текста
# mistakes - количество ошибок за сеанс
# text - текст, который вводился
def end_of_game(general_time, mistakes, text):
    try_again_button = pg.image.load("pictures/try-again.png")  # загружается изображение кнопки "TRY AGAIN"
    try_again_button_coord = (500, 120) # место для кнопки "TRY AGAIN"
    place_for_inscription = (200, 15)  # место для надписи "THE END OF INPUT"
    font_size_for_inscription = 60  # размер шрифта для надписи "THE END OF INPUT"
    while True:
        symbols_per_second = round(len(text) / general_time, 2)  # количество символов в секунду с округлением до 2 знаков
        DATA.export_of_data(symbols_per_second, mistakes)  # загрузка статистики сеанса в data.txt
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:  # если нажимается кнопка TRY AGAIN запускается все по новой
                if try_again_button_coord[0] <= pg.mouse.get_pos()[0] <= try_again_button_coord[0] + try_again_button.get_width()\
                      and try_again_button_coord[1] <= pg.mouse.get_pos()[1] <= try_again_button_coord[1] + try_again_button.get_height():
                    run_keyboard()
        FUNCTIONS.create_window()  # создается окно тренажера
        PRINT.print_text("THE END OF INPUT", COLOR.BLACK, place_for_inscription, font_size_for_inscription)
        accuracy = round((len(text) - mistakes)/len(text), 2) * 100  # точность ввода
        PRINT.print_for_end(text, symbols_per_second, mistakes, accuracy)

        # обработка окна ввода текста после завершения сеанса
        input_text = GLOBAL.font.render("You typed all the text", True, COLOR.BLACK)
        place_for_input_box_x = GLOBAL.input_box.x + GLOBAL.input_box.w * 0.3
        place_for_input_box_y = GLOBAL.input_box.y + 5
        GLOBAL.display.blit(input_text, (place_for_input_box_x, place_for_input_box_y))

        GLOBAL.display.blit(try_again_button, try_again_button_coord)

        rect_line_width = 3
        pg.draw.rect(GLOBAL.display, COLOR.GRAY, GLOBAL.input_box, rect_line_width)
        pg.draw.rect(GLOBAL.display, COLOR.BLACK, GLOBAL.text_box, rect_line_width)
        pg.display.update()
