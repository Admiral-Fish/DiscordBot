from client import MyClient
import env

if __name__ == "__main__":
    client = MyClient()
    client.run(env.DISCORD_TOKEN)
