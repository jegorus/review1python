class MainScreenClass:
    welcome_indent = 50

    def __init__(self, graphic_obj):
        self.MyGraphics = graphic_obj

    def draw_main_screen(self, button_session, button_music):
        self.MyGraphics.draw_background_image()
        self.MyGraphics.draw_button(button_session)
        self.MyGraphics.draw_button(button_music)
        self.MyGraphics.print_line('Welcome to JegorType', self.MyGraphics.textX_center + self.welcome_indent,
                                   self.MyGraphics.textY_start)
        self.MyGraphics.print_line('Typing Session',
                                   self.MyGraphics.textX_center + self.welcome_indent * 2, self.MyGraphics.textY_center)
        self.MyGraphics.print_line('Music',
                                   self.MyGraphics.textX_center + self.welcome_indent * 2,
                                   self.MyGraphics.textY_center + self.MyGraphics.font_size * 2)
