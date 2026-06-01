import asyncio

import pygame
from pygame.locals import *

class States:
    def __init__(self, window_size: tuple[int, int] = (800, 600)):
        self.debug = True
        self.base_window_size = window_size
        self.base_window_size_ratio = window_size[0] / window_size[1]

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

        self.is_open_question = False



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

        if not self.is_open_question:
            for i in self.ui_render_group:
                i.draw()

            for i in self.question_button_group:
                i.draw()

        elif self.is_open_question:
            for i in self.the_question_group:
                i.draw()

            for i in self.the_question_button_group:
                i.draw()

        for i in self.team_button_group:
            i.draw()

        self._win.blit(pygame.transform.scale(self._outside_win, resize_to), (x_offset, y_offset))
        pygame.display.flip()

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



class Button:
    """
    The Base Class for Buttons
    """
    def __init__(self, source: pygame.Surface,
                 position_x: float | int,
                 position_y: float | int,
                 width: float | int,
                 height: float | int,
                 active_background_color: list[int] | tuple[int, int, int] | str | None,
                 inactive_background_color: list[int] | tuple[int, int, int] | str | None,
                 enable_background: bool = True,
                 render_group: list | None = None,):
        """
        Create a Button

        :param source: The Source to draw the Button on
        :param position_x: The X position of the button
        :param position_y: The Y position of the button
        :param width: The Width of the button
        :param height: The Height of the button
        :param active_background_color: The Background color of the button when the mouse is over the button
        :param inactive_background_color: The default background color of the Button
        """
        self.source = source

        self.position_x = position_x
        self.position_y = position_y

        self.width = width
        self.height = height

        self.active_background_color = active_background_color
        self.inactive_background_color = inactive_background_color

        self.rect = pygame.Rect(position_x, position_y, width, height)

        self.enable_background = enable_background
        if active_background_color is None or inactive_background_color is None:
            self.enable_background = False

        if render_group is not None:
            render_group.append(self)

    def draw(self) -> None:
        """
        Draws the Button
        :return: None
        """

        if self.enable_background:
            if self.rect.collidepoint(game_states.mouse_pos):
                pygame.draw.rect(surface=self.source, rect=self.rect, color=self.active_background_color)
            else:
                pygame.draw.rect(surface=self.source, rect=self.rect, color=self.inactive_background_color)

    def collidepoint(self, pos: tuple[int, int]) -> bool:
        """
        Checks if the button collides with the given position

        :param pos: Coordinates to check against
        :return: If the button collides with the given position
        """
        return self.rect.collidepoint(pos)



class TextButton(Button):


    def __init__(self, source: pygame.Surface, position_x: float | int, position_y: float | int, width: float | int, height: float | int,
                 text: str, text_color: list[int] | tuple[int, int, int] | str, text_font: str | None,
                 active_background_color: list[int] | tuple[int, int, int] | None,
                 inactive_background_color: list[int] | tuple[int, int, int] | None, render_group: list | None = None,text_size: int= 24):

        super().__init__(source, position_x, position_y, width, height, active_background_color, inactive_background_color, render_group=render_group)

        self.text = text
        if text_font:
            self.font = pygame.font.Font(text_font, size=text_size)

        else:
            self.font = pygame.font.SysFont("Arial", text_size)

        self.font_render = self.font.render(text=self.text, color=text_color, antialias=True)
        self.text_color = text_color

        self.font_rect = self.font_render.get_rect()
        self.font_rect.center = self.rect.center

    def draw(self) -> None:

        if self.enable_background:
            if self.rect.collidepoint(game_states.mouse_pos):
                pygame.draw.rect(surface=self.source, rect=self.rect, color=self.active_background_color)
            else:
                pygame.draw.rect(surface=self.source, rect=self.rect, color=self.inactive_background_color)

        self.source.blit(self.font_render, self.font_rect)

    def collidepoint(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)


class QuestionButton(TextButton):
    def __init__(self, source: pygame.Surface, position_x: float | int, position_y: float | int,  text: str,
                 active_background_color: list[int] | tuple[int, int, int],
                 inactive_background_color: list[int] | tuple[int, int, int], theme: str, points: str | int):
        super().__init__(source, position_x, position_y, 200, 50, text, "Black", None,
                         active_background_color, inactive_background_color, render_group=game_states.question_button_group)

        self.theme = theme
        self.points = points



class TeamButton(TextButton):
    def __init__(self, source: pygame.Surface, position_x: float | int, position_y: float | int,  text: str,
                 team_color: str | tuple[int, int, int] ):
        super().__init__(source, position_x, position_y, 200, 50, text, "Black", None,
                         None,None, render_group=game_states.team_button_group)

        self.points = 0
        self.team_color = team_color

    def draw(self) -> None:
        """
        Draws the Button
        :return: None
        """
        if game_states.current_selected_team == self:
            self.border_width = 8

            pygame.draw.rect(game_states.win, "green", pygame.Rect(self.rect.x - self.border_width / 2, self.rect.y - self.border_width / 2, self.width + self.border_width, self.height + self.border_width))


        pygame.draw.rect(surface=self.source, rect=self.rect, color=self.team_color)

        self.source.blit(self.font.render(text=str(self.points), antialias=True, color=self.text_color), self.font_rect)

    def collidepoint(self, pos: tuple[int, int]):
        if self.rect.collidepoint(pos):
            game_states.current_selected_team = self


pygame.init()


async def main():
    points = ["100", "200", "300", "400"]
    thema = ["Punktzahl", "Geschichte\nDefinition", "Vorteile", "Nachteile", "Ausbildung\nHandwerk"]
    questions = {
        thema[1]: [
            "Wann entstanden Zünfte?",
            "Gibt es heute noch Zünfte?",
            "Was ist eine Zunft?",
            "Was ist eine Sammelzunft?",
        ],

        thema[2]: [
            "GRATIS PUNKTE",
            "Nennt ein Vorteil einer Zunft",
            "Was geschah, wenn ein Zunftmitglied starb?",
            "Was taten, Zünfte das alle Handwerker genug verdienen?",
        ],

        thema[3]: [
            "Wer war (fast) komplett von\neiner Mitgliedschaft ausgeschlossen?",
            "Welche Berufe wurden als ehrlos angesehen?",
            "Warum gab es weniger Innovation?",
            "GRATIS PUNKTE"
        ],

        thema[4]: [
            "Wer durfte Lehrlinge Ausbilden?",
            "Nenne die 3 Ausbildungstufen",
            "GRATIS PUNKTE",
            "Was passierte, wenn man bei\neiner Qualitätskontrolle durchfiel?",
        ]
    }

    answers = {
        thema[1]: [
            "Im 11./12. Jahrhundert",
            "Ja, diese haben aber andere Aufgaben, z.B. die Sozialhilfe.",
            "Zusammenschluss von Handwerkern\nwelche die gleiche Profession haben.",
            "Eine Zunft wo mehrere Professionen in\neiner Zunft zusammengefasst sind.",
        ],

        thema[2]: [
            "GRATIS PUNKTE",
            "Viele Antwortsmöglichkeiten.",
            "Gemeinsamer Trauermarsch durch die Stadt\noder\nUnterstützung der Witwe und Bezahlung der Beerdigung.",
            "Sie regulierten Preise und Herstellungsmethoden.",
        ],

        thema[3]: [
            "Frauen (andere Gruppen auch Möglich)",
            "z.B. Müller/Totengräber/Henker",
            "Weil Produktionsmethoden vorgeschrieben wurden und\nneuer Erfindungen eingeschränkt waren",
            "GRATIS PUNKTE"
        ],

        thema[4]: [
            "Ein Meister",
            "Lehrling, Geselle und der Meister",
            "GRATIS PUNKTE",
            "Das Produkt wurde weggeschmissen und neu gemacht werden ",
        ]
    }

    collum = [50, 250, 500, 750, 1000]
    row = [100, 200, 300, 400, 500, 600]

    category_amount_button_active_color = (150, 150, 150)
    category_amount_button_inactive_color = (160, 160, 160)

    for collum_index, category in enumerate(list(questions.keys())):
        for row_index, question in enumerate(questions[category]):
            row_test_index = row_index
            collum_test_index = collum_index + 1

            new_button = QuestionButton(game_states.win,
                                        collum[collum_test_index],
                                        row[row_test_index + 1],
                                        "???",
                                        category_amount_button_active_color,
                                        category_amount_button_inactive_color,
                                        category,
                                        points[row_test_index])

    money_button = TextButton(game_states.win, collum[0], row[0], 150, 50, thema[0], "Black", None,
                              category_amount_button_active_color, category_amount_button_inactive_color,
                              game_states.ui_render_group)
    category_button1 = TextButton(game_states.win, collum[1], 100, 200, 50, thema[1], "Black", None,
                                  category_amount_button_active_color, category_amount_button_inactive_color,
                                  game_states.ui_render_group)
    category_button2 = TextButton(game_states.win, collum[2], 100, 200, 50, thema[2], "Black", None,
                                  category_amount_button_active_color, category_amount_button_inactive_color,
                                  game_states.ui_render_group)
    category_button3 = TextButton(game_states.win, collum[3], 100, 200, 50, thema[3], "Black", None,
                                  category_amount_button_active_color, category_amount_button_inactive_color,
                                  game_states.ui_render_group)
    category_button4 = TextButton(game_states.win, collum[4], 100, 200, 50, thema[4], "Black", None,
                                  category_amount_button_active_color, category_amount_button_inactive_color,
                                  game_states.ui_render_group)

    amount_button1 = TextButton(game_states.win, collum[0], row[1], 150, 50, points[0], "Black", None,
                                category_amount_button_active_color, category_amount_button_inactive_color,
                                game_states.ui_render_group)
    amount_button2 = TextButton(game_states.win, collum[0], row[2], 150, 50, points[1], "Black", None,
                                category_amount_button_active_color, category_amount_button_inactive_color,
                                game_states.ui_render_group)
    amount_button3 = TextButton(game_states.win, collum[0], row[3], 150, 50, points[2], "Black", None,
                                category_amount_button_active_color, category_amount_button_inactive_color,
                                game_states.ui_render_group)
    amount_button4 = TextButton(game_states.win, collum[0], row[4], 150, 50, points[3], "Black", None,
                                category_amount_button_active_color, category_amount_button_inactive_color,
                                game_states.ui_render_group)

    # Question Screen
    the_question = TextButton(game_states.win, game_states.win.width / 2, game_states.win.height / 2, 1, 1, "None",
                              "Black", None, None, None, game_states.the_question_group, 40)
    go_back_button = TextButton(game_states.win, 100, 650, 150, 50, "Zurück", "Black", None,
                                category_amount_button_active_color, category_amount_button_inactive_color,
                                game_states.the_question_button_group)
    to_answer = TextButton(game_states.win, 1100, 590, 150, 50, "Antwort", "Black", None,
                           category_amount_button_active_color, category_amount_button_inactive_color,
                           game_states.the_question_button_group)
    give_points_to = TextButton(game_states.win, 1020, 650, 250, 50, "Übergebe Punkte", "Black", None,
                                category_amount_button_active_color, category_amount_button_inactive_color,
                                game_states.the_question_button_group)

    # Always on screen
    team_red = TeamButton(game_states.win, 300, 650, "0", "red")
    team_blue = TeamButton(game_states.win, 550, 650, "0", "blue")
    team_yellow = TeamButton(game_states.win, 800, 650, "0", "yellow")

    run = True
    while run:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_BACKSPACE):
                run = False

            if e.type == MOUSEBUTTONUP and e.button == 1:

                for i in game_states.team_button_group:
                    i.collidepoint(game_states.mouse_pos)

                if game_states.is_open_question:
                    if go_back_button.collidepoint(game_states.mouse_pos):
                        game_states.is_open_question = False

                    if to_answer.collidepoint(game_states.mouse_pos):
                        the_answer = TextButton(game_states.win, game_states.win.width / 2, game_states.win.height / 2, 1,
                                                  1, game_states.current_open_question_answer, "Black",
                                                  None, None, None,
                                                  game_states.the_question_group, 40)

                        game_states.the_question_group = [the_answer]

                    if give_points_to.collidepoint(game_states.mouse_pos):
                        if game_states.current_selected_team is not None:
                            game_states.current_selected_team.points += int(game_states.current_question_points)
                            game_states.is_open_question = False

                else:

                    for i in game_states.question_button_group:
                        if i.collidepoint(game_states.mouse_pos):

                            question_theme = i.theme
                            question_points = i.points
                            game_states.current_question_points = question_points

                            question_text = questions[question_theme][points.index(question_points)]

                            the_question = TextButton(game_states.win, game_states.win.width / 2, game_states.win.height / 2, 1, 1,
                                                      question_text, "Black", None, None, None,
                                                      game_states.the_question_group, 40)

                            game_states.current_open_question_answer = answers[question_theme][points.index(question_points)]
                            game_states.the_question_group = [the_question]
                            game_states.is_open_question = True

                            game_states.question_button_group.remove(i)

        game_states.win.fill("white")

        game_states.update_screen()
        await asyncio.sleep(0)

asyncio.ensure_future(main())