import json
from pathlib import Path

from redbot.core.bot import Red

from .invitetracker import InviteTracker

with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


async def setup(bot: Red) -> None:
    await bot.add_cog(InviteTracker(bot))
