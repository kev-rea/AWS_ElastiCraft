
init python:
    from python_resources import conector_with_pyenv as cwp
    
# img and characteres
image bg room =im.Scale( "images/bg cave.jpg", config.screen_width, config.screen_height) # Fondo de la habitación
image personaje = "images/eileen concerned.png"  # Sprite del personaje
image personaje_feliz= 'images/eileen vhappy.png'
image bg explorar= im.Scale( "bg washington.jpg", config.screen_width, config.screen_height)

# global variables
default player_name = ""
default type_game = ""
default level = ""
default correct_answers = 0
default total_questions = 0

# Game start
label start:
    # show backgraound
    scene bg room with fade

    # Mostramos al personaje en el centro
    show personaje at center

    # Mensaje inicial
    "¡Hey! This is a tester about AWS Services."
    "Welcome to the game!"
    "Let's start with your name first!"

    # Pedimos el nombre del jugador
    $ temp_name = renpy.input(_("What is your name? (Type your name and hit Enter.)"), default=_("Kevin"))

    # Aseguramos que el nombre no quede vacío
    $ player_name += temp_name.strip() 

    "¡Nice to meet you, [player_name]!"

    # Ocultamos al personaje
    hide personaje

    # Saltamos al menú principal
    jump main_menu_for_test


# main manu
label main_menu_for_test:
    #limpiar la variable type_game
    $ type_game = ""
    # Preguntamos por la certificación
    "[player_name], which kind of AWS certification do you want to get?"

    menu:
        "Solutions Architect":
            $ type_game += "Solutions_Architect"
            jump Solutions_Architect_parameters

        "Developer":
            $ type_game += "Developer"
            jump Developer_parameters


# Parámetros del curso Solutions Architect
label Solutions_Architect_parameters:
    #limpiar la variable level
    $ level = ""
    scene bg forest with dissolve

    "Welcome to the Solutions Architect course!"
    "In this course, you will practice your knowledge by answering questions about AWS Solutions Architect."
    "Let's start!"
    "What is your level of experience?"

    menu:
        "Beginner":
            $ level += "Beginner"
            "Great! Let's start with Basic Questions!"
            jump Solutions_Architect

        "Intermediate":
            $ level += "Intermediate"
            "Great! Let's start with Intermediate Questions!"
            jump Solutions_Architect

        "Advanced":
            $ level += "Advanced"
            "Great! Let's start with Advanced Questions!"
            jump Solutions_Architect

label Developer_parameters:
    #limpiar la variable level
    $ level = ""
    scene bg forest with dissolve

    "Welcome to the Developer course!"
    "In this course, you will practice your knowledge by answering questions about AWS Developer."
    "Let's start!"
    "What is your level of experience?"
    

    menu:
        "Beginner":
            $ level += "Beginner"
            "Great! Let's start with Basic Questions!"
            jump Developer
        "Intermediate":
            $ level += "Intermediate"
            "Great! Let's start with Intermediate Questions!"
            jump Developer
        "Advanced":
            $ level += "Advanced"
            "Great! Let's start with Advanced Questions!"
            jump Developer    


label Solutions_Architect:
    # Generar pregunta
    $ generated_question = cwp.generate_question(level, type_game)
    "[generate_question]"
    $ total_questions += 1  # Incrementar el total de preguntas

    "Question:\n [generated_question[0]]"
    # timed menu
    $ timeout = 10
    # Set the label that is jumped to if the player doesn't make a decision.
    $ timeout_label = "time_out_cuestions_SA"
    # Mostrar el menú con temporizador
    $ choice = renpy.display_menu([
        (generated_question[1], "A"),
        (generated_question[2], "B"),
        (generated_question[3], "C"),
    ], interact=True)

    if choice is None:
        $ choice_no_response="Solutions_Architect"

    if choice == generated_question[4]:
        $ correct_answers += 1
        "Correct! Option [choice] is the right answer."
    else:
        "Incorrect! The correct answer was [generated_question[4]]."

    $ timeout_label = None
    menu:
        "Next question":
            jump Solutions_Architect
        "Exit":
            jump calculate_score
    

label Developer:
    # Generar pregunta
    $ generated_question = cwp.generate_question(level, type_game)
    $ total_questions += 1  # Incrementar el total de preguntas

    "Question:\n [generated_question[0]]"

    # Configurar la variable de tiempo agotado
    $ timed_out = False

    # Mostrar el menú con temporizador
    $ choice = renpy.display_menu([
        (generated_question[1], "A"),
        (generated_question[2], "B"),
        (generated_question[3], "C"),
    ], interact=True)

    # Agregar un cronómetro con 30 segundos
    $ renpy.pause(5, hard=True)
    if choice is None:  # Si no se seleccionó nada antes del tiempo
        $ timed_out = True

    if timed_out:
        "Time's up! You didn't select an answer."
        "The correct answer was [generated_question[4]]."
    else:
        if choice == generated_question[4]:
            $ correct_answers += 1
            "Correct! Option [choice] is the right answer."
        else:
            "Incorrect! The correct answer was [generated_question[4]]."

    menu:
        "Next question":
            jump Developer
        "Exit":
            jump calculate_score


label time_out_cuestions_SA:
    if choice is None:
        "Time's up! You didn't select an answer."
        "The correct answer was [generated_question[4]]."
    menu:
        "Next question":
            jump Solutions_Architect
        "Exit":
            jump calculate_score
    if choice_no_response == "Solutions_Architect":
        "HELOOOOOOOOOOO"



label calculate_score:
    # Calcular calificación
    $ score = (correct_answers / total_questions) * 10 if total_questions > 0 else 0
    
    # Mostrar calificación
    scene bg room with fade
    "You answered [correct_answers] out of [total_questions] questions correctly."
    "Your final score is: [score] / 10."

    # Reiniciar juego o salir
    menu:
        "Play again":
            $ correct_answers = 0
            $ total_questions = 0
            jump main_menu_for_test
        "Exit":
            return

