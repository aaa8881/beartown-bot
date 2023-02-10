# beartown-bot

# How to run
1. Open `.env-example` and fill your bot token at `TOKEN`. (To get token, visit https://discord.com/developers/applications)
2. Rename it to `.env`
3. Run `pip install -r requirements.txt` in console.
4. Run `python3 main.py` to start the bot.

# Usage
Channel & Role ids are hard-coded inside the code.
## Slash Commands
- `/추첨`: Create giveaway on event channel.
## Message Commands
- `!verify <@ channel>`: Send get-role message to mentioned channel. Previous message should be deleted manually.
- `!ticket <@ channel>`: Send create-ticket message to mentioned channel. Previous message should be deleted manually.
- `!clear`: Use this to reset the opened ticket data.
- `!del`: Remove every closed ticket.
- `!purge <Integer>`: Delete messages.
