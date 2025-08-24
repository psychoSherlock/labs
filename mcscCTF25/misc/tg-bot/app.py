import telebot
import random
import os
import logging
import dotenv
import tempfile
from morse_audio_decoder.morse import MorseCode

dotenv.load_dotenv()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Dictionary of puzzles with their solutions
PUZZLES = {
    "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?": "echo",
    "The more you take, the more you leave behind. What am I?": "footsteps",
    "I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?": "map",
    "What has keys but no locks, space but no room, and you can enter but not go in?": "keyboard",
    "I'm tall when I'm young, and I'm short when I'm old. What am I?": "candle",
    "What is always in front of you but can't be seen?": "future",
    "What has many keys but can't open a single lock?": "piano",
    "What can travel around the world while staying in a corner?": "stamp"
}

# Morse code translations for answers
MORSE_CODE = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 
    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 
    's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-', 
    'y': '-.--', 'z': '--..', '0': '-----', '1': '.----', '2': '..---', 
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', 
    '8': '---..', '9': '----.'
}

# User session data
user_data = {}

# Get the bot token from environment variable
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not BOT_TOKEN:
    logger.error("No TELEGRAM_TOKEN environment variable found!")
    exit(1)

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Send a welcome message when the command /start is issued."""
    bot.reply_to(message,
        f"Hello, {message.from_user.first_name}! I'm Akbar, and this is my supposedly 'wise' friend Birbal!\n\n"
        f"Between us, Birbal's been struggling with these puzzles lately. His brain might be on vacation! 😂\n\n"
        f"Use /puzzleme to get a riddle that has Birbal scratching his head. Maybe YOU can show this so-called genius how it's done!\n\n"
        f"*Birbal glares while Akbar chuckles mischievously*"
        f"\n\n"
        "Type /help for instructions on how to play this game. Birbal keeps forgetting them, so I had to write them down for him!\n\n"
        "Let's see if you can outsmart Birbal! 🧠\n\n"
    )

@bot.message_handler(commands=['help'])
def send_help(message):
    """Send a message when the command /help is issued."""
    bot.reply_to(message,
        "🧠 *BIRBAL'S STRUGGLING GUIDE TO PUZZLES* 🧠\n\n"
        "How to survive our puzzle game (even Birbal needs this guide):\n\n"
        "/start - Hear Akbar mock Birbal's recent puzzle failures\n"
        "/puzzleme - Get a riddle that made Birbal's brain hurt\n"
        "/help - See these instructions that Birbal keeps in his pocket\n\n"
        "*Birbal frowns* \"I don't need help, Akbar just gives impossible puzzles!\""
    )

@bot.message_handler(commands=['puzzleme'])
def send_puzzle(message):
    """Send a random puzzle when the command /puzzleme is issued."""
    user_id = message.from_user.id
    
    # Select a random puzzle
    puzzle_text, answer = random.choice(list(PUZZLES.items()))
    
    # Store the current puzzle and answer for this user
    user_data[user_id] = {
        'puzzle': puzzle_text,
        'answer': answer.lower(),
        'morse_answer': ''.join(MORSE_CODE.get(char, '') for char in answer.lower() if char in MORSE_CODE)
    }
    
    bot.send_message(message.chat.id,
        f"🧩 *BIRBAL'S NIGHTMARE PUZZLE* 🧩\n\n"
        f"Hey {message.from_user.first_name}! Akbar here with a riddle that made Birbal hide under his turban:\n\n"
        f"{puzzle_text}\n\n"
        f"Birbal's been stuck on this one for days! *whispers* Between us, I'm starting to think he's not the genius everyone claims he is... Can YOU solve it?\n\n"
        f"*Birbal mumbles something about 'unfair riddles' in the background*"
    )

@bot.message_handler(content_types=['voice', 'audio', 'document'])
def handle_voice(message):
    """Handle voice messages, audio files and documents (which could be audio files)."""
    user_id = message.from_user.id
    
    # Check if user has an active puzzle
    if user_id not in user_data:
        bot.reply_to(message,
            "🤔 *BIRBAL'S CONFUSION* 🤔\n\n"
            "An audio without a puzzle? Even I'm not THAT confused!\n\n"
            "Get a puzzle first with /puzzleme before sending mysterious sounds.\n\n"
            "*Birbal looks relieved that someone else is confused for once*"
        )
        return
    
    # Get user's current puzzle data
    puzzle_data = user_data[user_id]
    
    # Download the audio file
    try:
        if message.voice:
            file_info = bot.get_file(message.voice.file_id)
        elif message.audio:
            file_info = bot.get_file(message.audio.file_id)
        elif message.document:
            file_info = bot.get_file(message.document.file_id)
        else:
            raise Exception("No audio content found")
            
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            file_path = temp_file.name
        
        # Download the file
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_path, 'wb') as audio_file:
            audio_file.write(downloaded_file)
            
        # Decode the Morse code from the audio file
        try:
            morse_code = MorseCode.from_wavfile(file_path)
            decoded_text = morse_code.decode().lower()
            
            # Log the decoded text for debugging
            logger.info(f"Decoded Morse: {decoded_text}")
            
            # Check if the decoded text matches the current puzzle answer
            if decoded_text == puzzle_data['answer']:
                bot.reply_to(message,
                    "🎉 *AKBAR IS IMPRESSED* 🎉\n\n"
                    "By the heavens! You solved it with Morse code! Birbal has been trying for WEEKS!\n\n"
                    f"I knew I'd find someone smarter than Birbal eventually! Here's your reward:\n\n 🔥 mcsc{{b1rbal_b34ts_th3_b33ps}} 🔥 \n\n"
                    f"Want another puzzle? Birbal needs all the help he can get these days!\n\n"
                    f"*Birbal mutters* \"I was just about to solve it...\""
                )
                # Reset user data
                del user_data[user_id]
                return
                
            # Check if it matches any OTHER puzzle answer
            for puzzle_text, answer in PUZZLES.items():
                if decoded_text == answer.lower() and puzzle_text != puzzle_data['puzzle']:
                    bot.reply_to(message,
                        "🤨 *AKBAR LISTENS CAREFULLY* 🤨\n\n"
                        "Hmm... I can hear the code clearly, but that's the answer to a different riddle!\n\n"
                        "It seems you're sending the solution to another puzzle. This one needs a different answer.\n\n"
                        f"*Birbal cups his ear* \"They're solving the wrong puzzle!\""
                    )
                    return
            
            # If it's valid Morse but doesn't match any answer
            bot.reply_to(message,
                "🤔 *BIRBAL AND AKBAR LISTEN INTENTLY* 🤔\n\n"
                f"We can hear your audio code saying '{decoded_text}', but that's not the answer to this puzzle.\n\n"
                "Try again with the correct solution\n\n"
                "*Birbal smirks* \"Even I know that's not right.\""
            )
            
        except Exception as e:
            logger.error(f"Error decoding Morse: {str(e)}")
            # If we can't decode the Morse code
            bot.reply_to(message,
                "😕 *AKBAR SCRATCHES HIS HEAD* 😕\n\n"
                "We're having trouble hearing clear code in this audio.\n\n"
                "Make sure your audio contains clear dots and dashes for the answer!\n\n"
                "*Birbal covers* \"I definitely heard something... I think.\""
            )
            
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        bot.reply_to(message,
            "😅 *TECHNICAL DIFFICULTIES* 😅\n\n"
            "Birbal seems to have dropped the audio while trying to listen to it!\n\n"
            "Could you please try sending it again? Make sure it's a clear audio file with code.\n\n"
            "*Akbar sighs* \"This is why we can't have nice things, Birbal.\""
        )
    finally:
        try:
            if 'file_path' in locals():
                os.unlink(file_path)
        except:
            pass

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Handle text messages."""
    user_id = message.from_user.id
    # Check if user has an active puzzle
    if user_id not in user_data:
        bot.reply_to(message,
            "🤨 *AKBAR'S PUZZLED LOOK* 🤨\n\n"
            "You're answering a puzzle I haven't even given yet? Wow, you might actually be smarter than Birbal!\n\n"
            "Type /puzzleme to get a riddle that's been making Birbal cry at night.\n\n"
            "*Birbal protests* 'I do NOT cry over puzzles... much.'"
        )
        return
    puzzle_data = user_data[user_id]
    user_message = message.text.lower()
    # Check if the answer matches any OTHER puzzle than the current one
    for puzzle_text, answer in PUZZLES.items():
        if user_message == answer.lower() and puzzle_text != puzzle_data['puzzle']:
            bot.reply_to(message,
                "😵 *AKBAR LOOKS CONFUSED* 😵\n\n"
                "That seems like an answer to a different riddle! Are you solving puzzles from the future?\n\n"
                "Birbal and I are still waiting for you to solve THIS puzzle:\n\n"
                f"{puzzle_data['puzzle']}\n\n"
                "*Birbal smirks* 'At least I'm solving the RIGHT puzzle...'"
            )
            return
    # Check if message matches morse code
    if user_message.replace(' ', '') == puzzle_data['morse_answer'].replace(' ', ''):
        bot.reply_to(message,
            "👂 *ROYAL CONFUSION* 👂\n\n"
            "What are these strange symbols? Birbal's been trying to decipher them for days!\n\n"
            "I can't see them clearly? But my ears are not aged yet\n\n"
            "*Birbal pretends to understand* 'Yes, yes, I was just about to suggest that...'"
        )
        return
    # Check if message matches answer directly
    if user_message == puzzle_data['answer']:
        bot.reply_to(message,
            "🤔 *BIRBAL LOOKS PERPLEXED* 🤔\n\n"
            "Hmm, your answer seems... familiar somehow, but we speak a different language in the court!\n\n"
            "Perhaps this hint might help you??? 👇\n\n"
            "*Birbal absentmindedly taps his fingers on the table in an unusual rhythm*"
        )
        return
    # Handle other cases
    bot.reply_to(message,
        "😁 *BIRBAL FINALLY FEELS SMART* 😁\n\n"
        "Ha! That's not right! For once, Birbal knows something you don't!\n\n"
        "*Birbal grins smugly* 'See Akbar? Not so easy, is it?'\n\n"
        "*Akbar whispers* 'Don't worry, he doesn't know the answer either. Try again!'"
    )

def main():
    logger.info("Akbar is ready to find someone smarter than Birbal!")
    bot.infinity_polling()

if __name__ == "__main__":
    main()