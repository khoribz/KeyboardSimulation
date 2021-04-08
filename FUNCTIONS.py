import COLOR
import GLOBAL
import PRINT


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


# Создание клавиатуры на окне
def keyboard_creation():
    keyboard = GLOBAL.pg.image.load('pictures/keyboard2.jpg')
    keyboard_location = (50, 250)
    GLOBAL.display.blit(keyboard, keyboard_location)


# Создание макета окна клавиатурного тренажера
def create_window():
    GLOBAL.display.fill(COLOR.WHITE)
    GLOBAL.display.blit(GLOBAL.bg.image, GLOBAL.bg.rect)
    GLOBAL.clock.tick(GLOBAL.FPS)
    keyboard_creation()
    place_for_speed = (50, 500)
    font_size_for_speed = 20
    place_for_mistakes = (600, 500)
    font_size_for_mistakes = 20
    PRINT.print_text("Symbols per second ---", COLOR.BLACK, place_for_speed, font_size_for_speed)
    PRINT.print_text("Mistakes ---", COLOR.BLACK, place_for_mistakes, font_size_for_mistakes)
