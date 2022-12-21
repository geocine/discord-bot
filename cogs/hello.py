import discord
import config
from discord import app_commands
from discord.ext import commands

class Hello(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Hello cog loaded.')

    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
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
        await interaction.response.send_message(f'Hey {interaction.user.name} you chose color {colors.name}')

async def setup(bot):
    await bot.add_cog(Hello(bot), guilds=[discord.Object(id=config.GUILD)])