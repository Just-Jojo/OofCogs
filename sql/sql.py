from typing import Literal

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config

# MySQL
import mysql.connector


RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class SQL(commands.Cog):
    """
    SQL cog that can be used for interacting with multiple databases.
    """

    __version__ = "1.0.4"

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=572944636209922059,
            force_registration=True,
        )

    async def cog_load(self):
        mysql_cred = await self.bot.get_shared_api_tokens("mysql")
        self.sqql = mysql.connector.connect(
            user=mysql_cred.get("username"),
            password=mysql_cred.get("password"),
            database="",
        )
        self.cursorr = self.sqql.cursor()
        await self.bot.loop.run_in_executor(
            None, self.cursorr.execute, "SET @@wait_timeout = 31536000"
        )

    def format_help_for_context(self, ctx):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        n = "\n" if "\n\n" not in pre_processed else ""
        return f"{pre_processed}{n}\nCog Version: {self.__version__}"

    async def red_delete_data_for_user(
        self, *, requester: RequestType, user_id: int
    ) -> None:
        return

    @commands.is_owner()
    @commands.group()
    async def sql(self, ctx):
        """SQL commands"""
        pass

    @sql.command()
    async def version(self, ctx):
        """Check what version of the SQL cog you have."""
        await ctx.reply(
            f"This cog is on version {self.__version__}.", mention_author=False
        )

    @sql.group()
    async def mysql(self, ctx):
        """MySQL commands"""
        pass

    @mysql.group()
    async def delete(self, ctx):
        """Delete database"""

    @mysql.command()
    async def create(self, ctx, database_name):
        """Create a database with MySQL"""
        await ctx.trigger_typing()
        sql_databases = "show databases"
        await self.bot.loop.run_in_executor(None, self.cursorr.execute, sql_databases)
        dblist = ", ".join(x for (x,) in self.cursorr)
        if len(database_name) > 64:
            await ctx.reply("This name is too long, please choose a shorter name.")
            return
        if database_name in dblist:
            await ctx.reply(
                f'The "{database_name}" database already exists, please use a different name.',
                mention_author=False,
            )
        else:
            await self.bot.loop.run_in_executor(
                None, self.cursorr.execute, f"CREATE DATABASE {database_name}"
            )
            await ctx.reply(f"{database_name} has been created.", mention_author=False)

    @mysql.command()
    async def list(self, ctx):
        """List databases in MySQL"""
        await ctx.trigger_typing()
        databases = "show databases"
        await self.bot.loop.run_in_executor(None, self.cursorr.execute, databases)
        if len(", ".join(x for (x,) in self.cursorr)) > 2000:
            embed = discord.Embed(
                title="MySQL Databases",
                description="Here are the databases that your have on your machine:",
            )
            embed.add_field(
                name="Databases: ",
                value="There are too many characters for your databases to be shown here.",
            )
            embed.set_footer(text="MySQL")
            await ctx.reply(embed=embed, mention_author=False)
        else:
            databases = "show databases"
            await self.bot.loop.run_in_executor(None, self.cursorr.execute, databases)
            mbed = discord.Embed(
                title="MySQL Databases",
                description="Here are the databases that your have on your machine:",
            )
            mbed.add_field(
                name="Databases:",
                value=", ".join(x for (x,) in self.cursorr) or "No databases",
            )
            mbed.set_footer(text="MySQL")
            await ctx.reply(embed=mbed, mention_author=False)

    @delete.command(aliases=["database"])
    async def db(self, ctx, database_name):
        """Remove database"""
        await ctx.trigger_typing()
        sql_databases = "show databases"
        await self.bot.loop.run_in_executor(None, self.cursorr.execute, sql_databases)
        dblist = ", ".join(x for (x,) in self.cursorr)
        if database_name in dblist:
            await self.bot.loop.run_in_executor(
                None, self.cursorr.execute, f"DROP DATABASE {database_name}"
            )
            await ctx.reply(
                f'The database "{database_name}" has been deleted.',
                mention_author=False,
            )
        else:
            await ctx.reply(
                "The database could not be deleted because it does not exist.",
            )
