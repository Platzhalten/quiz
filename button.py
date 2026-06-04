import pygame

from game_states import game_states


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


        self.rect = pygame.Rect(position_x, position_y, width, height)

        self.enable_background = enable_background

        if active_background_color is None:
            self.active_background_color = ""
            self.enable_background = False

        else:
            self.active_background_color = active_background_color

        if inactive_background_color is None:
            self.inactive_background_color = ""
            self.enable_background = False

        else:
            self.inactive_background_color = inactive_background_color

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
                 inactive_background_color: list[int] | tuple[int, int, int], theme: str, question: str):
        super().__init__(source, position_x, position_y, 200, 50, text, "Black", None,
                         active_background_color, inactive_background_color, render_group=game_states.question_button_group)

        self.theme = theme
        self.question = question



class TeamButton(TextButton):
    def __init__(self, source: pygame.Surface, position_x: float | int, position_y: float | int,  text: str,
                 team_color: str | tuple[int, int, int], team_name: str):
        super().__init__(source, position_x, position_y, 200, 50, text, "Black", None,
                         None,None, render_group=game_states.team_button_group)

        self.points = 0
        self.team_color = team_color
        self.team_name = team_name

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
