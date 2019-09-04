from bot import FishBot
from dotenv import load_dotenv

if __name__ == "__main__":    
    load_dotenv()      
    bot = FishBot()
    bot.run()