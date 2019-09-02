from client import MyClient
from dotenv import load_dotenv
from env import getVariable

if __name__ == "__main__":
    load_dotenv()

    client = MyClient()
    client.run(getVariable("DISCORD_TOKEN"))