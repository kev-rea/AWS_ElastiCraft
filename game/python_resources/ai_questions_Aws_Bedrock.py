import os
import boto3
import json
from dotenv import load_dotenv
import re
import sys

class AIQuestions:
    def __init__(self):
        """Initialize the class by loading environment variables."""
        load_dotenv()  # Cargar las variables del archivo .env
        self.region = os.getenv("AWS_REGION", "us-east-1")
        self.model_id = os.getenv("BEDROCK_MODEL_ID", "amazon.titan-text-premier-v1:0")

        # Cargar las credenciales de AWS desde las variables de entorno
        self.aws_access_key_id = os.getenv("AwsAccessKeyId")
        self.aws_secret_access_key = os.getenv("AwsSecretAccessKey")

        # Configurar el cliente AWS con credenciales opcionales
        self.client = self.setup_client()

    def setup_client(self):
        """Set up the Amazon Bedrock client."""
        try:
            if self.aws_access_key_id and self.aws_secret_access_key:
                return boto3.client(
                    service_name="bedrock-runtime",
                    region_name=self.region,
                    aws_access_key_id=self.aws_access_key_id,
                    aws_secret_access_key=self.aws_secret_access_key
                )
            else:
                # Usa las credenciales configuradas por defecto en AWS CLI o IAM
                return boto3.client("bedrock-runtime", region_name=self.region)
        except Exception as e:
            raise ValueError(f"Error al configurar el cliente de Bedrock: {e}")

    @staticmethod
    def instructions_for_the_prompt(service, difficulty):
        """Define the instructions for the prompt."""
        return (
            f"Create a single multiple-choice question about the topic: **{service}**.\n"
            "The question should adhere to the following parameters:\n"
            f"- Difficulty: {difficulty}.\n"
            "- Focus: Only create questions directly related to the specified service, avoiding any unrelated or additional information.\n\n"
            "### Guidelines for the question:\n"
            "1. The question must be clear and concise.\n"
            "2. It should have exactly 3 answer options (labeled A, B, and C).\n"
            "3. Only one option should be correct.\n\n"
            "### Format of Question must be:"
            "Question: <question>, A) <option>, B) <option>, C) <option>, Correct_Answer: <option>"
            "### Example of a well-structured question:\n"
            "Question: What is the capital of France?,A) Madrid,B) Paris,C) London,Correct_Answer: B"
        )

    #change this part if you want to change the model
    def set_settings_of_AI(self, difficulty, service):
        """Set the settings for the AI model and get the response."""
        prompt = self.instructions_for_the_prompt(service, difficulty)

        payload = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 3072,
                "stopSequences": [],
                "temperature": 0.0,
                "topP": 0.9
            }
        }

        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                contentType= "application/json",
                accept="application/json",
                body=json.dumps(payload)
            )
            
            response_body = json.loads(response["body"].read().decode("utf-8"))
            return response_body.get("results", [{}])[0].get("outputText", "")
        except Exception as e:
            raise RuntimeError(f"Error al invocar el modelo: {e}")

    def get_question(self, difficulty, service):
        """Get the question from the response text."""
        response_text = self.set_settings_of_AI(difficulty, service)
        # print("###############################333")
        # print(response_text)
        # Usar regex para extraer el contenido de "content"
        if response_text:
            text_response = response_text
            # Extraer la pregunta directamente
            question_start = text_response.find("ion:")+4 if "Question:" in text_response else 0
            question_end = text_response.find("?") + 1 if "?" in text_response else text_response.find("A)")
            question = text_response[question_start:question_end].strip()
            question = question[:-1] if question.endswith(",") else question
            # Extraer las opciones
            options_start = text_response.find("A)") 
            options_end = text_response.find("Correct_Answer:")
            options = text_response[options_start:options_end].strip()
            options=options[:-1].split(",") if options.endswith(",") else options.split(",")
            # Extraer la respuesta correcta
            correct_answer_start = text_response.find("Correct_Answer:") + len("Correct_Answer:")
            correct_answer = text_response[correct_answer_start:].strip()
            # Crear y retornar la lista con los resultados
            return [question] + options + [correct_answer]
        return [None, None, None, None, None]

def main_get_question(difficulty, service):
    """Get the question from the AI model."""
    try:
        ai = AIQuestions()
        question_data = ai.get_question(difficulty, service)
        return question_data
    except Exception as e:
        return f"Error: {e}"


# result_try=main_get_question("easy", "aws")
# print(result_try)
# print(len(result_try))
# print("----------------------------------------------------------------")

if __name__ == "__main__":
    difficulty = sys.argv[1]
    service = sys.argv[2]
    print(main_get_question(difficulty, service))
