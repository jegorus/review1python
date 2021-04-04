import pygame
pygame.init()


class GraphicsClass:
    # отвечает за отрисовку и музыку
    __screen_height = None
    __screen_width = None
    __screen = None  # окно с приложением, создается в create window
    font_size = 36
    text_font = pygame.font.Font('freesansbold.ttf', font_size)
    text_indent = 10  # отступы при печати
    textX_start = 10
    textY_start = 10
    textX_center = 400
    textY_center = 300
    textX = textX_start
    textY = textY_center
    text_height_multiplier = 1.1
    cl_white = (255, 255, 255)
    cl_black = (0, 0, 0)
    cl_green = (0, 255, 0)
    cl_red = (255, 0, 0)
    current_line = 1  # переменная показывает, на какой строке на данный момент производится действие
    music_is_playing = False
    mistakesNumber = 0
    is_mistaken = False  # если допущена и не исправлена ошибка, переходит в режим True

    def __init__(self, scr_height, scr_width):
        self.__screen_height = scr_height
        self.__screen_width = scr_width

    def create_window(self):
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))

    def set_title_and_icon(self):
        pygame.display.set_caption("JegorType")
        jegor_type_icon = pygame.image.load('Images/JegorTypeIcon.png')
        pygame.display.set_icon(jegor_type_icon)

    # вызывается только для слов, которые будут на экране для ввода с клавиатуры
    def show_line_new_word(self, new_word, printing_word_number, current_word, current_letter, is_correct):
        pygame.font.Font.set_underline(self.text_font, current_word == printing_word_number)
        text_width, text_height = self.text_font.size(new_word)
        if self.textX + text_width >= self.__screen_width:
            self.textX = self.textX_start
            self.textY += text_height * self.text_height_multiplier
            self.current_line += 1
        if self.current_line == 2 and printing_word_number <= current_word:
            self.current_line = 1
            self.textX = self.textX_start
            self.textY = self.textY_center
            self.fill_screen(self.cl_black)

        if self.current_line <= 2:
            for i in range(len(new_word)):
                if printing_word_number < current_word or (printing_word_number == current_word and i < current_letter):
                    text = self.text_font.render(new_word[i], True, self.cl_green)
                else:
                    text = self.text_font.render(new_word[i], True, self.cl_white)
                    if not is_correct:
                        if not self.is_mistaken:
                            self.mistakesNumber += 1
                            self.is_mistaken = True
                        text = self.text_font.render(new_word[i], True, self.cl_red)
                    else:
                        self.is_mistaken = False
                self.__screen.blit(text, (self.textX, self.textY))
                letter_width, letter_height = self.text_font.size(new_word[i])
                self.textX += letter_width
            self.textX += self.text_indent

    def print_line(self, line, x, y):
        text = self.text_font.render(line, True, self.cl_white)
        self.__screen.blit(text, (x, y))

    def fill_screen(self, cl):
        self.__screen.fill(cl)

    def set_music(self):
        if not self.music_is_playing:
            pygame.mixer.music.load('Audio/Music/JegorType1_1.wav')
            pygame.mixer.music.play(-1)
            self.music_is_playing = True
        else:
            pygame.mixer.music.stop()
            self.music_is_playing = False
