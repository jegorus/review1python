import pygame
from Graphics import GraphicsClass
from Vocabulary import VocabularyClass
from MainScreen import MainScreenClass

screen_height = 720
screen_width = 1280


class RunningProcessClass:
    MyGraphics = GraphicsClass(screen_height, screen_width)
    MyMainScreen = MainScreenClass(MyGraphics)
    MyVocabulary = VocabularyClass()
    __number_of_words_printed = None
    text_to_print = None  # список со словами для печати
    frame = None  # окно, которое видит пользователь: главное меню (1) или окно с печатью (2)
    current_word = None  # слово, которое вводится пользователем на данный момент
    current_letter = None  # буква, которая вводится на данный момент
    waiting_for_space = None
    is_correct = None  # режим, который показывает, не допущена ли на данный момент ошибка
    running = None  # приложение работает, пока True
    print_start_point = None  # слово, с которого начинается вывод на экран слов, которые нужно напечатать
    clock = None
    current_time = None
    start_timer = None
    typing_time = None  # длительность одной сессии печати
    timer_indent = None
    is_done = None  # значит, что сессия печати была пройдена до конца
    is_interrupted = True  #
    keys_typed = 0
    started_to_type = None
    click = None
    ms_in_sec = 1000
    sec_in_min = 60
    avg_symbols_in_word = 5  # принято считать, что в среднем слово на английском содержит 5 символов.
    # Поэтому для вычисления скорости печати в словах (wpm) количество напечатанных символов делится на 5

    def set_default(self):
        self.__number_of_words_printed = 30
        self.text_to_print = []
        self.frame = 1
        self.current_word = 0
        self.current_letter = 0
        self.waiting_for_space = False
        self.is_correct = True
        self.print_start_point = 0
        self.clock = pygame.time.Clock()
        self.current_time = 0
        self.start_timer = 0
        self.typing_time = 20
        self.timer_indent = 200
        self.is_done = True
        self.click = False
        self.started_to_type = False

    def __init__(self):
        self.set_default()
        self.running = True

    def typing_screen(self):
        # отвечает за меню печати
        while len(self.text_to_print) < self.__number_of_words_printed:
            new_word = self.MyVocabulary.get_random_word()
            self.text_to_print.append(new_word)

        for i in range(self.print_start_point, len(self.text_to_print)):
            self.MyGraphics.show_line_new_word(self.text_to_print[i], i,
                                               self.current_word, self.current_letter, self.is_correct)
            if self.MyGraphics.current_line > 2:
                break
        self.MyGraphics.current_line = 1
        self.MyGraphics.textX = self.MyGraphics.textX_start
        self.MyGraphics.textY = self.MyGraphics.textY_center

        time_left = self.typing_time * self.ms_in_sec - (self.current_time - self.start_timer)
        if time_left < 0:
            self.is_done = True
        self.MyGraphics.print_line(f"{time_left // (self.ms_in_sec * self.sec_in_min)}:"
                                   f"{((time_left % (self.ms_in_sec * self.sec_in_min)) // self.ms_in_sec):02d}",
                                   self.MyGraphics.textX_center + self.timer_indent, self.MyGraphics.textY_start)

    def get_event(self):
        # считывает input и обрабатывает события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

            if self.frame == 2:
                if event.type == pygame.KEYDOWN:
                    if not self.started_to_type:
                        self.started_to_type = True
                        self.start_timer = pygame.time.get_ticks()

                    if event.key == pygame.K_ESCAPE:
                        self.is_interrupted = True
                        self.set_default()
                    elif not self.waiting_for_space:
                        if ord('a') <= event.key <= ord('z'):
                            if chr(event.key) == self.text_to_print[self.current_word][self.current_letter]:
                                self.keys_typed += 1
                                self.is_correct = True
                                self.current_letter += 1
                                if len(self.text_to_print[self.current_word]) <= self.current_letter:
                                    self.waiting_for_space = True
                            else:
                                self.is_correct = False
                        else:
                            self.is_correct = False
                    else:
                        if event.key == pygame.K_SPACE:
                            self.waiting_for_space = False
                            self.is_correct = True
                            self.keys_typed += 1
                            self.current_word += 1
                            self.current_letter = 0
                            new_word = self.MyVocabulary.get_random_word()
                            self.text_to_print.append(new_word)
                        else:
                            self.is_correct = False

    def main_loop(self):
        # Основной цикл, после выхода из цикла будет выход из приложения
        self.running = True
        while self.running:
            if not self.started_to_type:
                time_delay = 100
                self.start_timer = pygame.time.get_ticks() + time_delay
            self.current_time = pygame.time.get_ticks()
            fps = 60
            self.clock.tick(fps)

            self.get_event()
            if self.keys_typed == 0:
                typing_speed = 0
            else:
                typing_speed = ((self.sec_in_min / self.typing_time) * self.keys_typed) / self.avg_symbols_in_word
            if self.frame == 1:  # вывести окно главного экрана
                mx, my = pygame.mouse.get_pos()
                button_x_coord = 490
                button_y_coord = 290
                button_x_size = 300
                button_session = pygame.Rect(button_x_coord, button_y_coord,
                                             button_x_size, self.MyGraphics.font_size * 1.5)
                button_music = pygame.Rect(button_x_coord, button_y_coord + 2 * self.MyGraphics.font_size,
                                           button_x_size, self.MyGraphics.font_size * 1.5)

                self.MyMainScreen.draw_main_screen(button_session, button_music)
                self.MyGraphics.draw_stat(not self.is_interrupted, round(typing_speed))

                if button_session.collidepoint((mx, my)):
                    if self.click:
                        self.MyGraphics.mistakesNumber = 0
                        self.MyGraphics.is_mistaken = False
                        self.frame = 2
                        self.keys_typed = 0
                        self.is_done = False
                        self.is_interrupted = False

                if button_music.collidepoint((mx, my)):
                    if self.click:
                        self.MyGraphics.set_music()

                    # вычисление скорости печати
            elif self.frame == 2:
                self.MyGraphics.fill_screen(self.MyGraphics.cl_black)
                self.typing_screen()
                typing_speed = (self.sec_in_min * self.ms_in_sec /
                                (self.current_time - self.start_timer) * self.keys_typed) / self.avg_symbols_in_word
                self.MyGraphics.draw_stat(not self.is_interrupted, round(typing_speed))

            pygame.display.update()
            if self.is_done:
                self.set_default()

    def create_window(self):
        self.MyGraphics.create_window()

    def set_title_and_icon(self):
        self.MyGraphics.set_title_and_icon()

    def set_music(self):
        self.MyGraphics.set_music()
