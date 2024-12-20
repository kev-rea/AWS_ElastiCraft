

# Declaramos las imágenes de fondo y personajes
image bg room =im.Scale( "images/bg cave.jpg", config.screen_width, config.screen_height) # Fondo de la habitación
image personaje = "images/eileen concerned.png"  # Sprite del personaje
image personaje_feliz= 'images/eileen vhappy.png'
image bg explorar= im.Scale( "bg washington.jpg", config.screen_width, config.screen_height)

# Declaramos variables globales vacías
default player_name = ""
default type_game = ""
default level = ""

# Inicia el juego
label start:
    # Mostramos el fondo
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


# Menú principal
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



label Solutions_Architect:
    "Here is the question"
    python:
        import subprocess
        import ast
        difficulty = level  # Usamos la variable 'level' definida anteriormente
        service = type_game  # Ejemplo de servicio

        # Ruta al entorno virtual y al script Python
        venv_path = "/home/kevin/NEW FASE WP2.0/RenPay/Juegos/LearnAws/game/python-packages/renpy_env/bin/python3.10"
        script_path = "/home/kevin/NEW FASE WP2.0/RenPay/Juegos/LearnAws/game/python_resources/ai_questions_Aws_Bedrock.py"

        # Comando para activar el entorno virtual y ejecutar el script
        # Ejecutar el script y capturar la salida
        def generate_question(venv_path, script_path, difficulty, service):
            attempt = 0
            max_attempts = 3  # Número máximo de intentos
            while attempt < max_attempts:
                    try:
                        # Ejecutar el script y capturar la salida
                        result = subprocess.check_output(
                            [venv_path, script_path, difficulty, service],
                            text=True
                        )
                        
                        # Convertir la cadena de texto en una tupla de Python
                        result = ast.literal_eval(result)
                        
                        # Verificar si la pregunta se ha generado correctamente
                        question = result[0]
                        if question is None:
                            renpy.say("Sorry, could not generate a valid question. Retrying...")
                            attempt += 1
                        else:
                            return result                        

                    except subprocess.CalledProcessError as e:
                        # Error al ejecutar el script
                        renpy.say(f"Error generating the question: {e}")
                        break

            # Si se superan los intentos o ocurre un error, devolver una pregunta predeterminada
            return [
                "Error generating the question.",
                "Option 1", "Option 2", "Option 3", "No answer"
            ]

        # Llamada a la función y almacenamiento de la pregunta generada
        generated_question = generate_question(venv_path, script_path, difficulty, service)


    "Aqui vemos lo que se obtuvo de la pregunta generada [generated_question]"
    "Question: [generated_question[0]]"  # La pregunta generada
    menu:
        "A) [generated_question[1]]":
            if generated_question[4] == "A":
                "Correct! Option A is the right answer."
            else:
                "Incorrect! The correct answer was [generated_question[4]]."

        "B) [generated_question[2]]":
            if generated_question[4] == "B":
                "Correct! Option B is the right answer."
            else:
                "Incorrect! The correct answer was [generated_question[4]]."

        "C) [generated_question[3]]":
            if generated_question[4] == "C":
                "Correct! Option C is the right answer."
            else:
                "Incorrect! The correct answer was [generated_question[4]]."

    menu:
        "Next question":
            jump Solutions_Architect
        "Exit":
            jump main_menu_for_test



    


    

#     #endpoint, deployment, subscription_key, azure_api_version
#     $ endpoint=renpy.input("Please enter the endpoint")
#     $ deployment=renpy.input("Please enter the deployment")
#     $ subscription_key=renpy.input("Please enter the subscription_key")
#     $ azure_api_version=renpy.input("Please enter the azure_api_version")

#     $  questio_3_answer = aq.main_get_question(level, type_game, endpoint, deployment, subscription_key, azure_api_version)
#     "Question: [questio_3_answer[0]]"
#     menu:
#         "[questio_3_answer[1]]":
#             pass
#         "[questio_3_answer[2]]":
#             pass
#         "[questio_3_answer[3]]":
#             pass
#     "Correct answer: [questio_3_answer[4]]"

#     return

# label Developer:
#     scene bg room with dissolve
#     "Decides quedarte en casa a estudiar."
#     "¡Vamos a estudiar!"
#     return

