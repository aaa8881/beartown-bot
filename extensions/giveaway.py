import sqlite3
import time
import random
import discord
from discord import slash_command
from discord.ext import commands, tasks
from modules import GiveawayForm
from ast import literal_eval


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lookup.start()

    @staticmethod
    def get_winners(users, amount):
        if len(users) <= amount:
            return users

        winners = []
        for u in range(amount):
            winners.append(random.choice(users))
            del users[users.index(winners[u])]
        return winners

    @tasks.loop(seconds=10)
    async def lookup(self):
        """
        Check whether a giveaway is finished or not every 10 seconds
        """
        await self.bot.wait_until_ready()
        conn = sqlite3.connect('data/event.db')
        cursor = conn.cursor()
        data = cursor.execute('SELECT * FROM giveaway').fetchall()

        now = time.time()
        channel = self.bot.get_channel(1060943947054194708)

        for d in data:
            if d[2] <= now:
                users = literal_eval(d[4])

                msg = await channel.fetch_message(d[3])
                embed = discord.Embed(title="추첨이 완료되었습니다!", color=0x967969)
                embed.add_field(name="당첨 보상", value=d[0], inline=False)
                embed.add_field(name="추첨 인원", value=d[1], inline=False)
                embed.add_field(name="참여자", value=f"{len(users)}명", inline=False)
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text="베어타운", icon_url=self.bot.user.avatar.url)
                if not users:
                    embed.add_field(name="당첨자", value="당첨자가 없습니다.", inline=False)
                    await msg.edit(embed=embed, view=None)
                else:
                    winners = self.get_winners(users, d[1])
                    win = ', '.join([self.bot.get_user(u).mention for u in winners])
                    embed.add_field(name="당첨자", value=win, inline=False)
                    await msg.edit(win, embed=embed, view=None)

                    thread = await msg.create_thread(name="당첨자 전용 스레드", auto_archive_duration=1440)
                    await thread.send(win + "\n24시간 내로 마인크래프트 닉네임을 입력해 주세요.\n"
                                            "스레드가 닫힌 후에는 당첨이 취소됩니다.")

                cursor.execute(f'DELETE FROM giveaway WHERE message = "{d[3]}"')
                conn.commit()
        conn.close()

    @slash_command(name="추첨", description="추첨을 진행합니다.")
    async def giveaway(self, ctx):
        """
        Create a giveaway
        :param ctx: Default param for getting the information of the caller. Nothing to do for this param
        :return
        """
        if not ctx.author.guild_permissions.view_audit_log:
            return await ctx.respond("권한이 없습니다.", ephemeral=True)

        form = GiveawayForm(self.bot)
        return await ctx.interaction.response.send_modal(form)


def setup(bot):
    bot.add_cog(Giveaway(bot))
