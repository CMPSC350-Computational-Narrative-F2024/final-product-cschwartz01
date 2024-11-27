import os
import requests
import random
from openai import OpenAI
from dotenv import dotenv_values
import rich
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import Box

# Set up rich console
console = Console()

# Set up OpenAI credentials
client = OpenAI()

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

def get_genre() -> str:
    genre = input("Would you like to play a fantasy, sci-fi, or realistic game? ")
    return genre

def get_random_character(player_name, player_role, genre):
    hair = ["black", "brown", "blonde", "red", "gray", "white", "blue", "green", "purple", "pink", "orange", "rainbow"]
    random_hair = random.choice(hair)
    eye = ["brown", "blue", "green", "hazel", "gray", "black", "amber", "red", "pink", "purple", "yellow", "orange", "rainbow"]
    random_eye = random.choice(eye)
    gender = ["male", "female", "non-binary", "genderfluid", "agender"]
    random_gender = random.choice(gender)
    age = random.randint(15, 85)
    random_character = f"{age} year old {random_gender} {player_role} named {player_name} with {random_hair} hair and {random_eye} eyes, existing within a {genre} world."
    return random_character

def get_random_prompt(genre):
    if genre.lower() == "fantasy":
        prompts_file = open("data/fantasy_prompts.txt", "r")
    elif genre.lower() == "sci-fi":
        prompts_file = open("data/scifi_prompts.txt", "r")
    elif genre.lower() == "realistic":
        prompts_file = open("data/realistic_prompts.txt", "r")
    # prompts_file = open("data/prompts.txt", "r")
    data = prompts_file.read()
    prompts_list = data.split("\n")
    random_prompt = random.choice(prompts_list)
    return random_prompt

def generate_image(description, client):
    '''Generates an image based on the given description.'''
    image_generator = client.images.generate(
        model = "dall-e-3",
        prompt = f"Generate an image to accompany the following description: {description}",
        size = "1024x1024",
        n = 1
    )
    img_url = image_generator.data[0].url
    print(f"\n Here is an image: {img_url}")

def generate_character_image(appearance, client):
    '''Generates an image based on the given character appearance.'''
    image_generator = client.images.generate(
        model = "dall-e-3",
        prompt = f"Generate an image for a character design without any letters or words. The character is a {appearance}. The image should be a portrait and in a style that is similar to that of Dungeons and Dragons handbooks.",
        size = "1024x1024",
        n = 1
    )
    img_url = image_generator.data[0].url
    print(f"\n Here is an image that represents your character: {img_url}")

def character_creation(genre):
    '''Creates a character based on the player's input.'''
    if genre.lower() == "fantasy":
        player_name = input("What is your name? ")
        player_role = input("Would you like to be a wizard, knight, elf, bard, or rogue? ")
    elif genre.lower() == "sci-fi": 
        player_name = input("What is your name? ")
        player_role = input("Would you like to be a space pirate, starship pilot, scientist, rebel leader, cyborg, or engineer? ")
    elif genre.lower() == "realistic":          
        player_name = input("What is your name? ")
        player_role = input("Would you like to be a barista, shopkeeper, teacher, librarian, or detective? ")
    change_appearance = input("Would you like to customize your appearance? (Yes/No) ")
    if change_appearance.lower() == "yes":
        hair_color = input("What color is your hair? ")
        eye_color = input("What color are your eyes? ")
        gender = input("What is your gender? ")
        age = input("How old are you? ")
        appearance = (f"{age} year old {gender} {player_role} named {player_name} with {hair_color} hair and {eye_color} eyes, existing within a {genre} world.")
        generate_character_image(appearance, client)
    else:
        appearance = get_random_character(player_name, player_role, genre)
        print(appearance)
        generate_character_image(appearance, client)
    return appearance

def main():
    '''Main function to run the game.'''

    print()
    # title option 1
    console.rule("[bold green]Welcome to Textfall", align = "center")

    # title option 2
    text = Text("Welcome to Textfall", style="bold green", justify="center")
    console.print(Panel(text))

    print("Type your actions and see how the story unfolds. Type quit to exit. \n")
    
    genre = get_genre()
    if genre.lower() == "fantasy":
        story_context = "You live in the kingdom of Eldravia, a lush and mountainous realm where the mists of of the peaks are said to carry the whispers of ancient gods, and the valleys are alive with bioluminescent flora that glow brighter under the gaze of the twin moons. Eldravia's heart lies in Veilspire, a city carved into a towering cliff, where the crystalline palace of the Crescent Throne houses a ruler whose mysterious lineage grants them the power to command the elements"
    elif genre.lower() == "sci-fi":
        story_context = "In the galaxy of Kyntara, a coalition of alien species inhabits colossal space stations built around dying stars, harvesting their energy for survival. Among the stars, fleets of sentient ships wander aimlessly, their memories of ancient wars locked in cryptic data archives, waiting for the right mind to unlock their secrets."
    elif genre.lower() == "realistic":
        story_context = "The town of Maplebrook is a quiet suburban haven where every street feels like a scene from a postcard, lined with neatly trimmed hedges and mailboxes painted with personal touches. Its heart is the old-fashioned downtown, where a family-run diner, a cozy bookstore, and a quirky antique shop form the backdrop of everyday routines. Life here is slow and predictable, yet the bonds between neighbors and the small, heartfelt dramas of daily life give Maplebrook its charm and meaning."
    elif genre.lower() == "quit":
        print("Goodbye!")
        return

    # player_character = character_creation(genre)
    # with open("data/chat_history.md", "a") as file:
    #         file.write(player_character + "\n")
    print("You are now ready to begin your adventure!")

    # generate_image(story_context, client)

    while True:
        console.print("\n" + story_context)
        console.print("\n" + get_random_prompt(genre))
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