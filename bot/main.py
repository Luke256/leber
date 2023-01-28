from common import *
import neko

@client.event
async def on_ready():
    print("起動完了")
    await tree.sync()#スラッシュコマンドを同期

client.run(secret.TOKEN, log_handler=handler)