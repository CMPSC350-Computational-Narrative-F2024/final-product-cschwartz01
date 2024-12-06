import os
import requests
import random
from openai import OpenAI
from dotenv import dotenv_values
import shutil
import json
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
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

SAVE_FILE = "game_save.json" # save game state to this file

def load_file(filename: str) -> str:
    with open(filename, "r") as file:
        return file.read()
    
# def save_game_state(state):
#     '''Saves the game state to a JSON file.'''
#     with open(SAVE_FILE, "w") as file:
#         json.dump(state, file)
#     save_chat_history(state["chat_history"])
#     print("Game saved!")

# def save_chat_history(chat_history):
#     '''Saves the chat history to a markdown file.'''
#     with open("data/chat_history.md", "w") as file:
#         file.writelines(chat_history)

def load_chat_history():
    # if os.path.exists("data/chat_history.md"):
    with open("data/chat_history.md", "r") as file:
        return file.read()
    # else: 
    #     return [] # return empty list if file does not exist

def load_game_state():
    '''Loads the chat history.'''
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            state = json.load(file)
        # load chat history from md file
        state["chat_history"] = load_chat_history()
        print("Game loaded!")
        return state
    else:
        print("No saved game found. Starting a new game.")
        return None

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
    genre = Prompt.ask("Would you like to play a fantasy, sci-fi, or realistic game?", choices=["fantasy", "sci-fi", "realistic"], show_choices=False)
    console.print()
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
    print(f"Appearance: {appearance}")
    img_url = image_generator.data[0].url
    print("Image URL retrieved")
    print(f"\n Here is an image that represents your character: {img_url}")
    return img_url

def save_image(img_url, output_folder):
    '''Saves the image to the output folder.'''
    output_folder = "images"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    img_data = requests.get(img_url).content
    file_name = os.path.join(output_folder, f"character.png") # puts file in output_folder dir
    with open(file_name, "wb") as file:
        file.write(img_data)
        print(f"Saved image to {file_name}")
    return file_name

def character_creation(genre):
    '''Creates a character based on the player's input.'''
    if genre.lower() == "fantasy":
        player_name = input("What is your name? ")
        player_role = Prompt.ask("Would you like to be a wizard, knight, elf, bard, or rogue? ", choices=["wizard", "knight", "elf", "bard", "rogue"], show_choices=False)
    elif genre.lower() == "sci-fi": 
        player_name = input("What is your name? ")
        player_role = Prompt.ask("Would you like to be a space pirate, starship pilot, scientist, rebel leader, cyborg, or engineer? ", choices=["space pirate", "starship pilot", "scientist", "rebel leader", "cyborg", "engineer"], show_choices=False)
    elif genre.lower() == "realistic":          
        player_name = input("What is your name? ")
        player_role = Prompt.ask("Would you like to be a barista, shopkeeper, teacher, librarian, or detective? ", choices=["barista", "shopkeeper", "teacher", "librarian", "detective"], show_choices=False)
    change_appearance = input("Would you like to customize your character? (Yes/No) ")
    if change_appearance.lower() == "yes":
        hair_color = input("What color is your hair? ")
        eye_color = input("What color are your eyes? ")
        gender = input("What is your gender? ")
        age = input("How old are you? ")
        appearance = (f"You are a {age} year old {gender} {player_role} named {player_name} with {hair_color} hair and {eye_color} eyes, existing within a {genre} world.")
    else:
        appearance = get_random_character(player_name, player_role, genre)
        print(f"You are a {appearance}")
    return appearance

def main():
    '''Main function to run the game.'''

    print()
    # title option 1
    # console.rule("[bold green]Welcome to Textfall", align = "center")

    # title option 2
    text = Text("Welcome to Textfall", style="bold green", justify="center")
    console.print(Panel(text))

    if load_chat_history() != "":
        with open("data/chat_history.md", "r") as file:
            chat_history = file.read()  
            story_context = chat_history
    else:
        # start a new game 
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

        player_character = character_creation(genre)
        chat_history = []

        # character_image = generate_character_image(player_character, client)
        # character_image = save_image(character_image, "images")
        with open("data/chat_history.md", "a") as file:
                file.write(f"Character: {player_character} + \n")
                # file.write(f"![Image]({character_image})\n")
        print()
        console.rule("[bold green]You are now ready to begin your adventure!")

    # generate_image(story_context, client)

    while True:
        console.print("\n" + story_context)
        console.print("\n" + get_random_prompt(genre))
        with open("data/chat_history.md", "a") as file:
                file.write(f"Genre: {genre}\n")
                file.write(f"Story context: {story_context}\n")
                file.write(f"Prompt: {get_random_prompt(genre)}\n")
        player_input = input("\nWhat do you want to do? ")

        if player_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            # delete chat history
            with open("data/chat_history.md", "w") as file:
                file.write("")
            # delete images folder
            # shutil.rmtree("images")
            break

        if player_input.lower() == "save":
            print("Game saved!")
            break
            
        story_context = generate_story_response(player_input, story_context, "data/chat_history.md")

        with open("data/chat_history.md", "a") as file:
            file.write(story_context + "\n")

        # chat_history.append(story_context)

if __name__ == "__main__":
    main()