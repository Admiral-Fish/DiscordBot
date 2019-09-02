from dotenv import load_dotenv

from client import MyClient
from env import getVariable


if __name__ == "__main__":
    load_dotenv()

    client = MyClient()
    client.run(getVariable("DISCORD_TOKEN"))
