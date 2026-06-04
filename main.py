import asyncio

import pygame
from pygame.locals import *

from game_states import game_states
from button import TextButton, TeamButton, QuestionButton


pygame.init()


async def main():
    points = ["100", "200", "300", "400"]
    thema = ["Geschichte\nDefinition", "Vorteile", "Nachteile", "Ausbildung\nHandwerk"]
    questions = {
        thema[0]: [
            "Wann entstanden Zünfte?",
            "Gibt es heute noch Zünfte?",
            "Was ist eine Zunft?",
            "Was ist eine Sammelzunft?",
        ],

        thema[1]: [
            "GRATIS PUNKTE",
            "Nennt ein Vorteil einer Zunft",
            "Was geschah wenn ein Zunftmitglied starb?",
            "Was taten Zünfte das alle Handwerker genug verdienen?",
        ],

        thema[2]: [
            "Wer war (fast) komplett von\neiner Mitgliedschaft ausgeschlossen?",
            "Welche Berufe wurden als ehrlos angesehen?",
            "Warum gab es weniger Innovation?",
            "GRATIS PUNKTE"
        ],

        thema[3]: [
            "Wer durfte Lehrlinge Ausbilden?",
            "Nenne die 3 Ausbildungstufen",
            "GRATIS PUNKTE",
            "Was passierte, wenn man bei\neiner Qualitätskontrolle durchfiel?",
        ]
    }

    answers = {
        thema[0]: [
            "Im 11./12. Jahrhundert",
            "Ja, diese haben aber andere Aufgaben, z.B. die Sozialhilfe.",
            "Zusammenschluss von Handwerkern\nwelche die gleiche Profession haben.",
            "Eine Zunft wo mehrere Professionen in\neiner Zunft zusammengefasst sind.",
        ],

        thema[1]: [
            "GRATIS PUNKTE",
            "Viele Antwortsmöglichkeiten.",
            "Gemeinsamer Trauermarsch durch die Stadt\noder\nUnterstützung der Witwe und Bezahlung der Beerdigung.",
            "Sie regulierten Preise und Herstellungsmethoden.",
        ],

        thema[2]: [
            "Frauen (andere Gruppen auch Möglich)",
            "z.B. Müller/Totengräber/Henker",
            "Weil Produktionsmethoden vorgeschrieben wurden und\nneuer Erfindungen eingeschränkt waren",
            "GRATIS PUNKTE"
        ],

        thema[3]: [
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

            QuestionButton(game_states.win, collum[collum_test_index], row[row_test_index + 1], "???", category_amount_button_active_color, category_amount_button_inactive_color, category, points[row_test_index])

    TextButton(game_states.win, collum[0], row[0], 150, 50, "Punktzahl", "Black", None,
               category_amount_button_active_color, category_amount_button_inactive_color, game_states.ui_render_group)

    for index, current_theme in enumerate(thema, start=1):
        TextButton(game_states.win, collum[index], 100, 200, 50, current_theme, "Black", None, category_amount_button_active_color, category_amount_button_inactive_color, game_states.ui_render_group)

    for index, point in enumerate(points, start=1):
        TextButton(game_states.win, collum[0], row[index], 150, 50, point, "Black", None, category_amount_button_active_color, category_amount_button_inactive_color, game_states.ui_render_group)

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
    german_names = {
        "red": "Rot",
        "blue": "Blau",
        "yellow": "Gelb"
    }

    for index, team_color in enumerate(["red", "blue", "yellow"]):
        TeamButton(game_states.win, 300 + (index * 250), 650, "0", team_color, team_name=german_names[team_color])

    game_states.current_selected_team = game_states.team_button_group[0]

    run = True
    while run:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_BACKSPACE):
                run = False

            if e.type == KEYDOWN:
                if e.key == K_ESCAPE and game_states.current_window == "question":
                    game_states.current_window = "board"

            if e.type == MOUSEBUTTONUP and e.button == 1:

                for i in game_states.team_button_group:
                    i.collidepoint(game_states.mouse_pos)

                if game_states.current_window == "question":
                    if go_back_button.collidepoint(game_states.mouse_pos):
                        game_states.current_window = "board"

                    if to_answer.collidepoint(game_states.mouse_pos):
                        the_answer = TextButton(game_states.win, game_states.win.width / 2, game_states.win.height / 2, 1,
                                                1, game_states.current_open_question_answer, "Black",
                                                None, None, None,
                                                game_states.the_question_group, 40)

                        game_states.the_question_group = [the_answer]

                    if give_points_to.collidepoint(game_states.mouse_pos):
                        if game_states.current_selected_team is not None:
                            game_states.current_selected_team.points += int(game_states.current_question_points)
                            game_states.current_window = "board"

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
                            game_states.current_window = "question"

                            game_states.question_button_group.remove(i)

        if not game_states.question_button_group and game_states.current_window == "board":
            winner_team = ""
            highest_points_amount = 0
            for i in game_states.team_button_group:
                if i.points < highest_points_amount:
                    continue

                elif i.points == highest_points_amount:
                    if isinstance(winner_team, str):
                        winner_team = [winner_team, i.team_name]

                    elif isinstance(winner_team, list):
                        winner_team.append(i.team_name)

                else:
                    winner_team = i.team_name
                highest_points_amount = i.points

            game_states.the_question_group = []

            if isinstance(winner_team, list):
                winner_text = f"Die Teams{", ".join(winner_team).removeprefix(",")} haben mit {highest_points_amount} Punkte gewonnen"

            else:
                winner_text = f"Das Team {winner_team} hat mit {highest_points_amount} Punkte gewonnen"


            winner = TextButton(game_states.win, game_states.win.width / 2, game_states.win.height / 2, 1, 1,
                                winner_text,"Black", None, None,
                                None, game_states.the_question_group, 40)

            game_states.current_window = "winner"


        game_states.win.fill("white")

        game_states.update_screen()

        if game_states.is_web:
            await asyncio.sleep(0)


game_states.is_web = not "__file__" in globals()

if game_states.is_web:
    asyncio.ensure_future(main())
else:
    asyncio.run(main())
