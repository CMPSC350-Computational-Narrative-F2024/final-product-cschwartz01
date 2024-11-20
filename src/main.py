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

def get_genre() -> str:
    genre = input("Puzzle, Horror, Fantasy, or Sci Fi? ")
    if genre.lower in ["puzzle"]:
        print("You have chosen the puzzle genre.")
        prompt = load_file("data/puzzle_prompt.txt")
    elif input == "Horror":
        prompt = load_file("data/horror_prompt.txt")
    elif input == "Fantasy":
        prompt = load_file("data/fantasy_prompt.txt")
    elif input == "Sci Fi":
        prompt = load_file("data/scifi_prompt.txt")
    else:
        print("Invalid input. Please try again.")
        get_genre()
    return prompt

def start_game() -> str:
    return input("Type 'start' to begin the game: ")

def get_user_choice() -> str:
    return input("What do you want to do? ")

def generate_story(prompt: str, user_choice: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a writer for text-based adventure games."},
            # {"role": "user", "content": f"prompt"},
            # {"role": "user", "content": user_choice}
        ],
        temperature=0.7,
        top_p=1,
        max_tokens=1500,
        n=1,
    )
    result = response.choices[0].message.content.strip()
    with open("data/chat_history.md", "a") as file:
        file.write(result + "\n")
    return result

def main():
    prompt = load_file("data/prompt.txt")
    print("Welcome to [insert game name here]! Type 'exit' or 'quit' to leave the game.")
    while True:
        # genre = get_genre()
        # if genre() != None:
        #     prompt = generate_story(genre(), user_choice)
        print()
        user_choice = get_user_choice()
        if user_choice.lower() in ["exit", "quit"]:
            with open("data/chat_history.md", "w") as file:
                file.write("")
            break
        prompt = generate_story(prompt, user_choice)
        print(prompt)

if __name__ == "__main__":
    main()