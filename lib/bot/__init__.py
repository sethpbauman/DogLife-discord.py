from datetime import datetime
from sys import exc_info

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed, File
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

PREFIX = "+"
OWNER_IDS = [146426946048229377]

class Bot(BotBase):
    def __init__(self):
        # adding prefix as attribute for convenience
        self.PREFIX = PREFIX
        # so we know whether bot has started or not
        self.ready = False  
        # to set the guild (for later)
        self.guild = None
        # scheduler
        self.scheduler = AsyncIOScheduler()

        # create the bot
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)
        
    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()
        
        print("running bot...")
        super().run(self.TOKEN, reconnect=True)
    
    async def on_connect(self):
        print("bot connected")
    
    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        # 
        if err == "on_command_error":
            await args[0].send("Something went wrong.")
        channel = self.get_channel(730922987246846066)
        await channel.send("error occured")
        # re-raises the error explicitly by using sys.exc_info to get the exception instance
        ## sys.exc_info returns (type, value, traceback), where value is the exception instance
        raise exc_info(1)

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass
        
        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc


    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(730922987246846063)
            print("bot ready")
            
            # creates channel object
            channel = self.get_channel(730922987246846066)
            
            # sends a message to the channel
            await channel.send("Now online!")

            # makes one of those little boxes with text in it (called an embed)
            embed = Embed(title="This is my title", description="DogBot has a description",
                          colour=0xFF0000, timestamp=datetime.utcnow())
            
            # adds the main contents to embed (inline = false puts that field in a new row)
            fields = [("Name", "Value", True),
                      ("Another field", "This field is next to the other one", True),
                      ("A non-inline field", "This field will appear on it's own row", False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            # sets an author (with an icon picture, currently using the guild picture), footer, thumbnail, and image
            embed.set_author(name="Seth", icon_url=self.guild.icon_url)
            embed.set_footer(text="This is a footer!")
            embed.set_thumbnail(url=self.guild.icon_url)
            embed.set_image(url=self.guild.icon_url)

            # sends embed message
            await channel.send(embed=embed)

            # sends a picture message (uses file)
            await channel.send(file=File("./data/images/profilepic.jpg"))


        else:
            print("bot reconnected")

    async def on_message(self, message):
        pass


bot = Bot()