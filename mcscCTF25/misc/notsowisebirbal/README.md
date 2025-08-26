## NotSoWiseBirbal

- **Difficulty**: Easy
- **Category**: Miscellaneous
- **Skills Required**: Riddle Solving, Morse Code, Telegram Bot Interaction, Audio Generation

In the grand Mughal court, Emperor Akbar is famed for his wit, but even he admits that Birbal's cleverness is legendary. Yet, lately, Birbal has been stumped by a series of cryptic riddles—each answer hidden not in words, but in something else.

Akbar, ever the prankster, has challenged the kingdom's brightest minds to outsmart Birbal. He's enlisted a mysterious Telegram bot to deliver these puzzles, hoping someone can crack the code and restore Birbal's reputation.

Can you outsmart the royal smartypants and earn imperial bragging rights?

## Files Provided

- Telegram Bot: [@akbars_puzzle_bot](https://t.me/akbars_puzzle_bot)

## Setup and Installation

To run the bot locally for development or testing:

1. **Python Version Requirement**: This bot requires Python 3.10 or lower (not compatible with Python 3.11+)

2. **Install dependencies**:

   ```bash
   pip3 install -r requirements.txt
   ```

3. **Configure the bot**:

   - Create a `.env` file in the project root
   - Add your Telegram bot token: `TELEGRAM_TOKEN=your_bot_token_here`

4. **Run the bot**:
   ```bash
   python3 app.py
   ```

## Hints

Birbal's been tapping his fingers in an unusual rhythm lately. Perhaps he's trying to communicate something that can't be spoken aloud.

## Solution

<details>
<summary>Click to reveal solution</summary>

### Analysis Approach

1. Interact with the Telegram bot to get riddles
2. Solve the riddles to get the answers
3. Convert the answers to Morse code audio
4. Send the audio back to the bot to verify
5. Receive the flag when the correct audio is sent

### Step-by-Step Solution

#### Step 1: Start the Bot

- Search for [@akbars_puzzle_bot](https://t.me/akbars_puzzle_bot) on Telegram
- Send `/start` to begin interaction
- The bot will respond with an introduction and instructions

#### Step 2: Get and Solve a Riddle

Send `/puzzleme` to receive one of these riddles:

| Riddle                                                                                                  | Answer    |
| ------------------------------------------------------------------------------------------------------- | --------- |
| "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?" | echo      |
| "The more you take, the more you leave behind. What am I?"                                              | footsteps |
| "What has keys but no locks, space but no room, and you can enter but not go in?"                       | keyboard  |
| "I'm tall when I'm young, and I'm short when I'm old. What am I?"                                       | candle    |
| "What has many keys but can't open a single lock?"                                                      | piano     |
| "What can travel around the world while staying in a corner?"                                           | stamp     |

#### Step 3: Convert Answer to Morse Code

Use [Morse Code Translator](https://morsecode.world/international/translator.html) to convert the answer.

For example:

- "keyboard" becomes `-.- . -.-- -... --- .- .-. -..`

#### Step 4: Generate and Send Audio

1. On the Morse Code Translator site:
   - Configure audio settings (speed ~15-20 WPM, standard tone ~700 Hz)
   - Click "Play" to verify the sound
   - Click "Download" to save the audio file
2. Send the audio file to the bot as an attachment

#### Step 5: Receive the Flag

Upon correct submission, the bot will decode the Morse code audio and respond with the flag.

```
mcsc{b1rbal_b34ts_th3_b33ps}
```

### Common Issues and Troubleshooting

- If the bot says it's a different puzzle's answer: Double-check that your solution matches the current riddle
- If the bot can't decode the audio: Try generating the Morse code again with slower speed or different tone frequency
- If the bot doesn't recognize your audio: Make sure you're sending an actual audio file, not just text

</details>

## Author

Created by [psychoSherlock](https://github.com/psychoSherlock)
