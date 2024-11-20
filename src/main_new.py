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

def generate_story_response(player_input, story_context):
    prompt = f'''
        The following is a text-based adventure game. Continue the story based on the player's choice. 
        Stort context: {story_context}
        Player's choice: {player_input}
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
        stream=True
    )
    result = response.choices[0].message.content.strip()
    return result 

def generate_image(appearance, client):
    image_generator = client.images.generate(
        model = "dall-e-3",
        prompt = f"Generate an imaage that represents the following character: {appearance}",
        size = "1024x1024",
        n = 1
    )
    img_url = image_generator.data[0].url
    print(f"Here is an image that represents you: {img_url}")

def character_creation():
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

def main():
    print("Welcome to the game!")
    print("Type your actions and see how the story unfolds. Type quit to exit. \n")

    player_character = character_creation()
    print("You are now ready to begin your adventure!")

    # while True:
    #     print("\n" + story_context)
    #     player_input = input("What do you want to do? ")

    #     if player_input.lower() in ["quit", "exit"]:
    #         print("Goodbye!")
    #         break
            
    #     story_context = generate_story_response(player_input, story_context)

if __name__ == "__main__":
    main()