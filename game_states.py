import pygame

class States:
    def __init__(self, window_size: tuple[int, int] = (800, 600)):

        # Automatically checks if file is run in a web browser at the end of the main file
        self.is_web = None

        self.debug = True
        self.base_window_size = window_size
        self.base_window_size_ratio = window_size[0] / window_size[1]

        pygame.display.set_caption("Quiz")
        self._win = pygame.display.set_mode(window_size)
        self._outside_win = pygame.Surface(window_size)

        self._mouse_pos = pygame.mouse.get_pos()

        self.ui_render_group = []
        self.question_button_group = []

        self.the_question_group = []
        self.the_question_button_group = []
        self.current_open_question_answer = ""
        self.current_question_points = 0

        self.team_button_group = []
        self.current_selected_team = None

        self._is_open_question = False
        self._current_window = "board"

    def update_screen(self):
        current_window_size = self._win.get_size()

        scale_x  = current_window_size[0] / self.base_window_size[0]
        scale_y = current_window_size[1] / self.base_window_size[1]

        scale = min(scale_x, scale_y)

        new_width = self.base_window_size[0] * scale
        new_height = self.base_window_size[1] * scale

        resize_to = (new_width, new_height)

        x_offset = (current_window_size[0] - new_width) / 2
        y_offset = (current_window_size[1] - new_height) / 2

        self._calculate_mouse_pops(x_offset, y_offset, scale)

        if game_states.debug:
            self._win.fill((40, 40, 40))
        else:
            self._win.fill(color=(0, 0, 0))

        match self._current_window:
            case "board":
                for i in self.ui_render_group:
                    i.draw()

                for i in self.question_button_group:
                    i.draw()

                for i in self.team_button_group:
                    i.draw()

            case "question":
                for i in self.the_question_group:
                    i.draw()

                for i in self.the_question_button_group:
                    i.draw()

                for i in self.team_button_group:
                    i.draw()

            case "winner":
                for i in self.the_question_group:
                    i.draw()

        self._win.blit(pygame.transform.scale(self._outside_win, resize_to), (x_offset, y_offset))
        pygame.display.flip()

    @property
    def is_open_question(self):
        return self._is_open_question

    @is_open_question.setter
    def is_open_question(self, value: bool):
        if not value:
            print(value)
            current_team_index = (self.team_button_group.index(self.current_selected_team) + 1 ) % len(self.team_button_group)

            self.current_selected_team = self.team_button_group[current_team_index]

        self._is_open_question = value

    @property
    def current_window(self):
        return self._current_window

    @current_window.setter
    def current_window(self, value):
        self._current_window = value

    @property
    def mouse_pos(self):
        return self._mouse_pos

    def _calculate_mouse_pops(self, x_offset, y_offset, scale):
        current_mouse_pos = pygame.mouse.get_pos()

        virtual_mouse_x = (current_mouse_pos[0] - x_offset) / scale
        virtual_mouse_y = (current_mouse_pos[1] - y_offset) / scale
        virtual_mouse_pos = (virtual_mouse_x, virtual_mouse_y)
        self._mouse_pos = virtual_mouse_pos

    @property
    def win(self):
        return self._outside_win


game_states = States((1280, 720))
