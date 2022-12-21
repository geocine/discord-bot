import datetime
import os
import discord
import config
from discord import app_commands
from discord.ext import commands
from PIL import Image, PngImagePlugin

class Hello(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Hello cog loaded.')

    # watch on_message event
    @commands.Cog.listener()
    async def on_message(self, message):
        # check if the message is from the bot
        if message.author == self.bot.user:
            return
        print(f"Message from {message.author}: {message.content}")
        # check if the message contains any attachments
        if message.attachments:
            # get the first attachment
            attachment = message.attachments[0]
            print(f"Attachment: {attachment.filename}")
            # check if the attachment is a PNG image
            if attachment.filename.endswith(".png"):
                print("Image is a PNG file.")
                # create the images folder if it does not exist
                if not os.path.exists("images"):
                    os.makedirs("images")

                # generate a unique filename for the image
                timestamp = datetime.datetime.now().timestamp()
                image_name = f"image{timestamp}.png"
                image_path = f"images/{image_name}"

                print(f"Saving image as {image_name}")

                # save the image to the images folder
                await attachment.save(image_path)

                print(f"Image saved as {image_name}")

                # open the image and get the metadata
                with Image.open(image_path) as im:
                    metadata = im.info

                print(f"Image metadata: {metadata}")
                
                # delete the image
                os.remove(image_path)

                # send the metadata back to the server
                await message.channel.send(f"Image metadata: {metadata}", reference=message)
            else:
                await message.channel.send("Image is not a PNG file.")

    @commands.command()
    async def sync(self, ctx) -> None:
        # check if the user is the owner of the bot
        if ctx.author.id == ctx.bot.owner_id:
            # send a message to the channel
            print("You are not allowed!")
            return
        # fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        fmt = await ctx.bot.tree.sync()
        await ctx.send(
          f"Synced {len(fmt)} commands to the current guild."
        )
        # channel = await ctx.message.author.create_dm()
        # await channel.send('hey buddy')
        return

    @commands.command()
    async def respond(self, ctx):
        """
        This commands response with Hello {user.name}
        """
        # check if the user is the owner of the bot
        if ctx.author.id == ctx.bot.owner_id:
            # send a message to the channel
            await ctx.send(f'Hello master!')
            return
        # log the user who tried to use the command and the owner of the bot
        print(f'{ctx.author.id} tried to use the command respond')
        print(f'Owner of the bot is {ctx.bot.owner_id}')
        # get the user who sent the message
        user = ctx.author
        # send a message to the channel
        await ctx.send(f'Hello {user.name}!')

    @commands.command()
    async def hello(self, ctx):
        """
        This commands response with Hello {user.name}
        """
        # get the user who sent the message
        user = ctx.author
        # send a message to the channel
        await ctx.send(f'Hello {user.name}!')

    @app_commands.command(name="choosecolor", description="color selector")
    #new code
    @app_commands.describe(colors='Colors to choose from')
    @app_commands.choices(colors=[
        discord.app_commands.Choice(name='Red', value=1),
        discord.app_commands.Choice(name='Blue', value=2),
        discord.app_commands.Choice(name='Green', value=3),
    ])
    #end new code
    async def choosecolor(self, interaction: discord.Interaction, colors: discord.app_commands.Choice[int]):
        print("in choosecolor")
        await interaction.response.send_message(f'Hey {interaction.user.name} you chose color {colors.name}')

async def setup(bot):
    # await bot.add_cog(Hello(bot), guilds=[discord.Object(id=config.GUILD)])
    await bot.add_cog(Hello(bot))
