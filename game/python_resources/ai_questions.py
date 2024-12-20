import os 
import subprocess
from openai import AzureOpenAI
from dotenv import load_dotenv
import re
import sys


class AIQuestions:
    def __init__(self):
        """Initialize the class by loading environment variables."""
        load_dotenv()
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment = os.getenv("DEPLOYMENT_NAME")
        self.subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        self.client = self.setup_client()

    def setup_client(self):
        """Set up the AzureOpenAI client."""
        return AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.subscription_key,
            api_version=self.azure_api_version,
        )

    @staticmethod
    def instructions_for_the_prompt(service, difficulty):
        """Define the instructions for the prompt."""

        ""
        return (
            f"Create a single multiple-choice question about the topic: **{service}**.\n"
            "The question should adhere to the following parameters:\n"
            f"- Difficulty: {difficulty}.\n"
            "- Focus: Only create questions directly related to the specified service, avoiding any unrelated or additional information.\n\n"
            "### Guidelines for the question:\n"
            "1. The question must be clear and concise.\n"
            "2. It should have exactly 3 answer options (labeled A, B, and C).\n"
            "3. Only one option should be correct.\n\n"
            "### Example of a well-structured question:\n"
            "### Format of Question must be:"
            "Question: <question>, A) <option>, B) <option>, C) <option>, Correct_Answer: <option>"
            "### Example of a well-structured question:\n"
            "Question: What is the capital of France?,A) Madrid,B) Paris,C) London,Correct_Answer: B"
        )

    def set_settings_of_AI(self,dificulty, service):
        """Set the settings for the AI model and get the rating score.
        :param plugin_name: The name of the plugin.
        :return: The rating score."""
        prompt = self.instructions_for_the_prompt(dificulty, service)
        chat_prompt = [{"role": "user", "content": prompt}]
    
        completion = self.client.chat.completions.create(
            model=self.deployment,
            messages=chat_prompt,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
        )
        response_text = completion.to_json()
        return response_text
    
    def get_question(self,dificulty, service):
        """Get the question from the response text."""
        response_text = self.set_settings_of_AI(dificulty, service)
        regex = r'"content":\s*"(.*?)",'
        match_response = re.search(regex, response_text)
        text_response=match_response.group(1)  
        if match_response:
            pattern =r"Question:\s*(.*?),\s*A\)\s*(.*?),\s*B\)\s*(.*?),\s*C\)\s*(.*?),\s*Correct Answer:\s*(\w)"
            match=re.search(pattern,text_response)
            if match:
                results=match.groups()
                return results
            else:
                None, None, None, None, None
        else:
            None, None, None, None, None

def main_get_question(dificulty, service):
    """Get the question from the AI model."""
    ai = AIQuestions()
    questions_text= ai.get_question(dificulty, service)
    return questions_text

if __name__ == "__main__":
    difficulty = sys.argv[1]
    service = sys.argv[2]
    print(main_get_question(difficulty, service))


