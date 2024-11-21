import os
import requests
from openai import OpenAI
from dotenv import dotenv_values

client = OpenAI()
# Set up OpenAI credentials

CONFIG = dotenv_values(".env")

OPEN_AI_KEY = CONFIG["KEY"] or os.environ["OPEN_AI_KEY"]
OPEN_AI_ORG = CONFIG["ORG"] or os.environ["OPEN_AI_ORG"]

client.api_key = OPEN_AI_KEY
client.organization = OPEN_AI_ORG

def load_file(filename: str) -> str:
    with open(filename, "r") as file:
        return file.read()

def generate_story_response(player_input, story_context, chat_history):
    '''Generates a response to the player's input based on the current story context and chat history.'''

    prompt = f'''
        The following is a text-based adventure game. Continue the story based on the player's choice. 
        Story context: {story_context}
        Player's choice: {player_input}
        Do not generate the player's choice, only follow what {player_input} leads to.
        You will be given the chat history to help you continue the story and allow for the story to change based on the player's previous choices
        and actions. This chat history is {chat_history}.
        '''
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a writer for text-based adventure games."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        top_p=1,
        max_tokens=1500,
        n=1,
        # stream=True I'll figure this out later
    )
    result = response.choices[0].message.content.strip()
    return result

def generate_image(appearance, client):
    '''Generates an image based on the player's appearance.'''
    image_generator = client.images.generate(
        model = "dall-e-3",
        prompt = f"Generate an imaage that represents the following character: {appearance}",
        size = "1024x1024",
        n = 1
    )
    img_url = image_generator.data[0].url
    print(f"Here is an image that represents you: {img_url}")

def character_creation():
    '''Creates a character based on the player's input.'''
    player_name = input("What is your name? ")
    player_role = input("WOuld you like to be a wizard, knight, elf, bard, or rogue? ")
    change_appearance = input("Would you like to customize your appearance? (Yes/No) ")
    if change_appearance.lower() == "yes":
        hair_color = input("What color is your hair? ")
        eye_color = input("What color are your eyes? ")
        gender = input("What is your gender? ")
        age = input("How old are you? ")
        appearance = (f"You are a {age} year old {player_role} named {player_name} with {hair_color} hair and {eye_color} eyes.")
        print(appearance)
        generate_image(appearance, client)
    else:
        print(f"You are a {player_role} named {player_name}.")
        appearance = (f"You are a {player_role}.Your age, hair and eye color are all random.")
        generate_image(appearance, client)
    return appearance

def main():
    '''Main function to run the game.'''
    
    print("Welcome to the game!")
    print("Type your actions and see how the story unfolds. Type quit to exit. \n")

    # player_character = character_creation()
    print("You are now ready to begin your adventure!")

    story_context = """You live in the vast and ancient world of Middle-earth, lands of unmatched beauty and peril stretch across mountains,forests, and plains, each harboring its own legends and mysteries. From the rolling hills of the Shire, where peace and simplicity reign, to the fiery chasms 
        of Mount Doom, where evil stirs in shadow, the world is shaped by the constant struggle between light and darkness. Amid these landscapes, 
        dwarven halls glitter beneath towering peaks, elven realms shimmer with timeless magic, and human cities rise as bastions of hope against 
        the creeping forces of despair. Every stone and tree bears the weight of history, waiting for new heroes to carve their stories into the 
        tapestry of the world."""

    while True:
        print("\n" + story_context)
        player_input = input("\n What do you want to do? ")

        if player_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            with open("data/chat_history.md", "w") as file:
                file.write("")
            break
            
        story_context = generate_story_response(player_input, story_context, "data/chat_history.md")

        with open("data/chat_history.md", "a") as file:
            file.write(story_context + "\n")

if __name__ == "__main__":
    main()