from dotenv import load_dotenv

from bot import FishBot

if __name__ == "__main__":
    load_dotenv()
    bot = FishBot()
    bot.run()
