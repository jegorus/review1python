import pygame
from Graphics import GraphicsClass
from Vocabulary import VocabularyClass


class RunningProcessClass:
    screen_height = 720
    screen_width = 1280
    MyGraphics = GraphicsClass(screen_height, screen_width)
    MyVocabulary = VocabularyClass()
    __number_of_words_printed = None
    text_to_print = None  # список со словами для печати
    frame = None  # сцена: главное меню (1) или окно с печатью (2)
    current_word = None  # слово, которое вводится пользователем на данный момент
    current_letter = None  # буква, которая вводится на данный момент
    waiting_for_space = None
    is_correct = None  # режим, который показывает, не допущена ли на данный момент ошибка
    running = None  # приложение работает, пока True
    print_start_point = None  # слово, с которого начинается вывод на экран слов, которые нужно напечатать
    clock = None
    current_time = None
    start_timer = None
    typing_time = None
    welcome_indent = None
    timer_indent = None
    is_done = None  # значит, что сессия печати была пройдена до конца
    is_interrupted = True  #
    keys_typed = 0

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
        self.welcome_indent = 50
        self.timer_indent = 200
        self.is_done = True

    def __init__(self):
        self.set_default()
        self.running = True

    def main_screen(self):
        # отвечает за главное меню
        self.MyGraphics.print_line('Welcome to JegorType', self.MyGraphics.textX_center + self.welcome_indent,
                                   self.MyGraphics.textY_start)
        self.MyGraphics.print_line('Press 1 to continue:',
                                   self.MyGraphics.textX_center + self.welcome_indent * 2, self.MyGraphics.textY_center)
        self.MyGraphics.print_line('Press 2 to turn on/off the music:',
                                   self.MyGraphics.textX_center + self.welcome_indent * 2,
                                   self.MyGraphics.textY_center + self.MyGraphics.font_size)
        self.MyGraphics.print_line('Statistics:', 950, 500)
        if not self.is_interrupted:
            self.MyGraphics.print_line(f"Mistakes: {self.MyGraphics.mistakesNumber}",
                                       900, 500 + self.MyGraphics.font_size * 2)
            if self.keys_typed == 0:
                typing_speed = 0
            else:
                typing_speed = ((60 / self.typing_time) * self.keys_typed) / 5
            self.MyGraphics.print_line(f"Speed: {round(typing_speed)} WPM",
                                       900, 500 + self.MyGraphics.font_size * 3)
        else:
            self.MyGraphics.print_line("Mistakes: X",
                                       900, 500 + self.MyGraphics.font_size * 2)
            self.MyGraphics.print_line("Speed: X",
                                       900, 500 + self.MyGraphics.font_size * 3)

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

        time_left = self.typing_time * 1000 - (self.current_time - self.start_timer)
        if time_left < 0:
            self.is_done = True
        self.MyGraphics.print_line(f"{time_left // 60000}:{((time_left % 60000) // 1000):02d}",
                                   self.MyGraphics.textX_center + self.timer_indent, self.MyGraphics.textY_start)

    def get_event(self):
        # считывает input и обрабатывает события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.frame == 1:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.MyGraphics.mistakesNumber = 0
                        self.MyGraphics.is_mistaken = False
                        self.frame = 2
                        self.keys_typed = 0
                        self.is_done = False
                        self.is_interrupted = False
                        self.start_timer = pygame.time.get_ticks()
                    if event.key == pygame.K_2:
                        self.MyGraphics.set_music()
            elif self.frame == 2:
                if event.type == pygame.KEYDOWN:
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
            self.MyGraphics.fill_screen(self.MyGraphics.cl_black)
            self.get_event()
            if self.frame == 1:
                self.main_screen()
            elif self.frame == 2:
                self.typing_screen()
            self.current_time = pygame.time.get_ticks()
            self.clock.tick(60)
            pygame.display.update()
            if self.is_done:
                self.set_default()

    def create_window(self):
        self.MyGraphics.create_window()

    def set_title_and_icon(self):
        self.MyGraphics.set_title_and_icon()

    def set_music(self):
        self.MyGraphics.set_music()
