import asyncio

import pygame
from pygame.locals import *

from game_states import game_states
from button import TextButton, TeamButton, QuestionButton


pygame.init()

category_amount_button_active_color = (150, 150, 150)
category_amount_button_inactive_color = (160, 160, 160)

collum = [50, 250, 500, 750, 1000]
row = [100, 200, 300, 400, 500, 600]

points = ["100", "200", "300", "400"]
questions = {
    "Geschichte\nDefinition": {
        "Wann entstanden Zünfte?": {"answer": "Im 11./12. Jahrhundert"},
        # required: answer; optionals: points(=sets a custom amount of points for the question)
        "Gibt es heute noch Zünfte?": {"answer": "Ja, diese haben aber andere Aufgaben, z.B. die Sozialhilfe."},
        "Was ist eine Zunft?": {"answer": "Zusammenschluss von Handwerkern\nwelche die gleiche Profession haben."},
        "Was ist eine Sammelzunft?": {
            "answer": "Eine Zunft wo mehrere Professionen in\neiner Zunft zusammengefasst sind."},
    },
    "Vorteile": {
        "GRATIS PUNKTE": {"answer": "GRATIS PUNKTE"},
        "Nennt ein Vorteil einer Zunft": {"answer": "Viele Antwortsmöglichkeiten"},
        "Was geschah wenn ein Zunftmitglied starb?": {
            "answer": "Gemeinsamer Trauermarsch durch die Stadt\noder\nUnterstützung der Witwe und Bezahlung der Beerdigung."},
        "Was taten Zünfte das alle Handwerker genug verdienen?": {
            "answer": "Sie regulierten Preise und Herstellungsmethoden."},
    },

    "Nachteile": {
        "Wer war (fast) komplett von\neiner Mitgliedschaft ausgeschlossen?": {
            "answer": "Frauen (andere Gruppen auch Möglich)"},
        "Welche Berufe wurden als ehrlos angesehen?": {"answer": "z.B. Müller/Totengräber/Henker"},
        "Warum gab es weniger Innovation?": {
            "answer": "Weil Produktionsmethoden vorgeschrieben wurden und\nneuer Erfindungen eingeschränkt waren"},
        "GRATIS PUNKTE": {"answer": "GRATIS PUNKTE"}
    },

    "Ausbildung\nHandwerk": {
        "Wer durfte Lehrlinge Ausbilden?": {"answer": "Ein Meister"},
        "Nenne die 3 Ausbildungstuffen": {"answer": "Lehrling, Geselle und der Meister"},
        "GRATIS PUNKTE": {"answer": "GRATIS PUNKTE"},
        "Was passierte, wenn man bei\neiner Qualitätskontrolle durchfiel?": {
            "answer": "Das Produkt wurde weggeschmissen und neu gemacht werden"},
    }
}

go_back_button = TextButton(game_states.win, 100, 650, 150, 50, "Zurück", "Black", None,
                            category_amount_button_active_color, category_amount_button_inactive_color,
                            game_states.the_question_button_group)

to_answer = TextButton(game_states.win, 1100, 590, 150, 50, "Antwort", "Black", None,
                       category_amount_button_active_color, category_amount_button_inactive_color,
                       game_states.the_question_button_group)

give_points_to = TextButton(game_states.win, 1020, 650, 250, 50, "Übergebe Punkte", "Black", None,
                            category_amount_button_active_color, category_amount_button_inactive_color,
                            game_states.the_question_button_group)


async def main():
    global points, questions

    for collum_index, category in enumerate(list(questions.keys()), start= 1):
        for row_index, question in enumerate(questions[category], start=1):
            QuestionButton(game_states.win, collum[collum_index], row[row_index], "???", category_amount_button_active_color, category_amount_button_inactive_color, category, question)

    TextButton(game_states.win, collum[0], row[0], 150, 50, "Punktzahl", "Black", None,
               category_amount_button_active_color, category_amount_button_inactive_color, game_states.ui_render_group)

    for index, current_theme in enumerate(questions.keys(), start=1):
        TextButton(game_states.win, collum[index], 100, 200, 50, current_theme, "Black", None, category_amount_button_active_color, category_amount_button_inactive_color, game_states.ui_render_group)

    for index, point in enumerate(points, start=1):
        TextButton(game_states.win, collum[0], row[index], 150, 50, point, "Black", None, category_amount_button_active_color, category_amount_button_inactive_color, game_states.ui_render_group)

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

            if e.type == MOUSEBUTTONUP and e.button == 1:
                for i in game_states.team_button_group:
                    i.collidepoint(game_states.mouse_pos)

                for question_buttons in game_states.question_button_group:
                    if question_buttons.collidepoint(game_states.mouse_pos):
                        await question_loop(question_button=question_buttons, points_table=points)
                        game_states.question_button_group.remove(question_buttons)

        if not game_states.question_button_group and game_states.current_window == "board":
            await winner_loop()

        game_states.win.fill("white")

        game_states.update_screen()

        if game_states.is_web:
            await asyncio.sleep(0)


async def question_loop(question_button: QuestionButton, points_table: list[str]):
    game_states.current_window = "question"

    question_theme = question_button.theme
    question = question_button.question

    question_dict = questions[question_theme][question]

    question_points = question_dict.get("points", None)

    if question_points is None:
                question_points = points_table[list(questions[question_theme].keys()).index(question)]

    game_states.current_question_points = question_points

    the_question = TextButton(game_states.win, game_states.win.width / 2, game_states.win.height / 2, 1, 1,
                              question, "Black", None, None, None,
                              game_states.the_question_group, 40)

    game_states.current_open_question_answer = question_dict["answer"]
    game_states.the_question_group = [the_question]

    # Question Screen
    TextButton(game_states.win, game_states.win.width / 2, game_states.win.height / 2, 1, 1, question,
               "Black", None, None, None, game_states.the_question_group, 40)


    run = True
    while run:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_BACKSPACE):
                run = False

            if e.type == KEYDOWN:
                if e.key == K_ESCAPE and game_states.current_window == "question":
                    game_states.current_window = "board"

            if e.type == MOUSEBUTTONUP and e.button == 1:
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

        if not game_states.current_window == "question":
            return

        game_states.win.fill("white")

        game_states.update_screen()

        if game_states.is_web:
            await asyncio.sleep(0)


async def winner_loop():
    if game_states.question_button_group:
        return

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

    TextButton(game_states.win, game_states.win.width / 2, game_states.win.height / 2, 1, 1, winner_text,
               "Black", None, None,None,
               game_states.the_question_group, 40)

    game_states.current_window = "winner"


    run = True
    while run:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_BACKSPACE):
                run = False

        game_states.win.fill("white")

        game_states.update_screen()

        if game_states.is_web:
            await asyncio.sleep(0)


game_states.is_web = not "__file__" in globals()

if game_states.is_web:
    asyncio.ensure_future(main())
else:
    asyncio.run(main())
