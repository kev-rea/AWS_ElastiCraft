
import subprocess
import ast

# Ruta al entorno virtual y al script Python
venv_path = "/home/kevin/NEW FASE WP2.0/RenPay/Juegos/LearnAws/game/python-packages/renpy_env/bin/python3.10"
script_path = "/home/kevin/NEW FASE WP2.0/RenPay/Juegos/LearnAws/game/python_resources/ai_questions_Aws_Bedrock.py"

# Ejecutar el script y capturar la salida
def generate_question(difficulty, service):
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
                    attempt += 1
                else:
                    return result                        

            except subprocess.CalledProcessError as e:
                # Error al ejecutar el script
                print(f"Error al ejecutar el script: {e}")
                break

    # Si se superan los intentos o ocurre un error, devolver una pregunta predeterminada
    return [
        "Error generating the question.",
        "Option 1", "Option 2", "Option 3", "No answer"
    ]

