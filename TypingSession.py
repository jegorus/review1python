from Vocabulary import VocabularyClass

class TypingSessionClass
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
