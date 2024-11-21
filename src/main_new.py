import os
import requests
import random
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

def get_genre() -> str:
    genre = input("Would you like to play a fantasy, sci-fi, or realistic game? ")
    return genre

def get_random_prompt():
    prompts_file = open("data/prompts.txt", "r")
    data = prompts_file.read()
    prompts_list = data.split("\n")
    random_prompt = random.choice(prompts_list)
    return random_prompt

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

    genre = get_genre()
    if genre.lower() == "fantasy":
        story_context = ''' You live in the kingdom of Eldravia, a lush and mountainous realm where the mists of 
            of the peaks are said to carry the whispers of ancient gods, and the valleys are alive with bioluminescent 
            flora that glow brighter under the gaze of the twin moons. Eldravia's heart lies in Veilspire, a city carved into a 
            towering cliff, where the crystalline palace of the Crescent Throne houses a ruler whose mysterious lineage grants 
            them the power to command the elements.
            '''
    elif genre.lower() == "sci-fi":
        story_context = '''In the galaxy of Kyntara, a coalition of alien species inhabits colossal space stations built around 
            dying stars, harvesting their energy for survival. Among the stars, fleets of sentient ships wander aimlessly, their memories of 
            ancient wars locked in cryptic data archives, waiting for the right mind to unlock their secrets.
            '''
    elif genre.lower() == "realistic":
        story_context = ''' The town of Maplebrook is a quiet suburban haven where every street feels like a scene from a postcard, 
            lined with neatly trimmed hedges and mailboxes painted with personal touches. Its heart is the old-fashioned downtown, where a 
            family-run diner, a cozy bookstore, and a quirky antique shop form the backdrop of everyday routines. Life here is slow and 
            predictable, yet the bonds between neighbors and the small, heartfelt dramas of daily life give Maplebrook its charm and meaning.
            '''
    
    # player_character = character_creation()
    print("You are now ready to begin your adventure!")

    while True:
        print("\n" + story_context)
        print("\n" + get_random_prompt())
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