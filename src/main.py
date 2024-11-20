import os
import openai
from dotenv import dotenv_values

# Set up OpenAI credentials

CONFIG = dotenv_values(".env")

OPEN_AI_KEY = CONFIG["KEY"] or os.environ["OPEN_AI_KEY"]
OPEN_AI_ORG = CONFIG["ORG"] or os.environ["OPEN_AI_ORG"]

openai.api_key = OPEN_AI_KEY
openai.organization = OPEN_AI_ORG

def load_file(filename: str) -> str:
    with open(filename, "r") as file:
        return file.read()

# def get_genre() -> str:
#     return input("What genre do you want to write in? ")

def get_user_choice() -> str:
    return input("What do you want to do? ")

def generate_story(prompt: str, user_choice: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a writer for text-based adventure games. Use the user input of {user_choice} to continue the story."},
            # {"role": "user", "content": f"prompt"},
            # {"role": "user", "content": user_choice}
        ],
        temperature=0.7,
        top_p=1,
        max_tokens=1500,
        n=1
    )
    result = response.choices[0].message.content.strip()
    return result

def chat_history():
    result = result
    with open("data/chat_history.md", "a") as file:
        file.write(result + "\n")

def main():
    prompt = load_file("data/prompt.txt")
    while True:
        # print(prompt)
        user_choice = get_user_choice()
        if user_choice.lower() in ["exit", "quit"]:
            break
        prompt = generate_story(prompt, user_choice)
        print(f"prompt = {prompt}")

if __name__ == "__main__":
    main()