# CMPSC 350: Project Progress

## Provide a tentative title for the work.

Textfall

## Description

So far, everything has been pretty good, although it did take me a bit to get used to Github Copilot, to be honest. Now that I know a little more about how it works, it's definitely been easier. I've created a character creation portion which allows users to create their character and generate an image of said character which is cool, I just need to figure out a better way to go about it then simply printing the image url which is what I'm doing right now (primarily just to test things). I've also been using Chat GPT to generate starting prompts so that players have something to go ogg og when they first start. As of right now I only have prompts (and character creation) for the fantasy genre, but I'll add to include the other genres I'm thinking of doing (Sci-fi and Realistic). Also, for some reason sometimes the LLM would create the player's choice so I had to specify in the prompt to only follow what the variable `player_input` supplied, which solved the problem.

## Peer Feedback

Questions I have for a peer (Aria)
1. How will you be incorporating Twine into your project? Is there a way to "merge" Twine and an LLM API so that they work together?
2. Will the game be different for each user or will it have the same general storyline with an ending that is effected by the user's choices?
3. How will journaling be incorporated? Will this journaling part be a task that one must do in order to "move on" in the game, or will it simply allow the user a place to record their thoughts and feelings on the game/the experience of living with depression?
4. Will this game focus solely on depression, or will other mental illnesses be included?

### Unstructured peer feedback

From Aria: I think Charlie's game is extremely well developed in terms of technicality. The way that they incorporated the LLM API into their game and actually based their game on the player's input was something I initially wanted to do, but thought too difficult. Therefore, I feel Charlie's successful implementation is quite impressive. I would want to know more about if there is an ending developed into this narrative, as I think this is a game that could go on forever if the player just keeps on making choices, and it could only be up to the player to end the game based on their choices as well.

## Persisting challenges

I've had some problems with streaming the text to the terminal for some reason, but I'm not worried about that and will probably work on that after I get the rest of everything working. Another problem I have is that I can't display images in the terminal (which I knew) so I have to figure out how I'm gonna deal with that. As of right now, I'm thinking of creating a folder for the image(s) and then giving the player the option to open the images at their discretion (kind of like a link they can click to open the photo in a new tab/window). I also don't entirely know how well the chat history works to change the story because I would have to experiment a lot with the exact prompt and get pretty far in to see what a difference it would make. That being said, because of how I have it set up with different starting prompts, each time I start the game there seems to be a relatively unique story (since even if it's the same starting prompt, if I start off doing something different than that will obviously effect the story).
