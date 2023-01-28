from common import *
import neko, login

@client.event
async def on_ready():
    logging.info("BOT launched!")
    print("起動完了！")
    await tree.sync()

client.run(secret.TOKEN, log_handler=handler)