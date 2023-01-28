from common import *
import neko, login, submit

@client.event
async def on_ready():
    logging.info("BOT launched!")
    await tree.sync()

client.run(secret.TOKEN, log_handler=handler)