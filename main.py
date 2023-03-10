import check
import login
import logout
import neko
import submit
import setting
import help
from common import *


@client.event
async def on_ready():
    logging.info("BOT launched!")
    await tree.sync()
    client.auto_healthcheck.start()

client.run(secret.TOKEN, log_handler=handler)