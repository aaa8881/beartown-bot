import sqlite3
import discord
from discord.ext import commands
from modules import ServerButton


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ticket')
    async def ticket_create(self, ctx, channel: discord.TextChannel):
        """
        Send create-ticket message
        :param ctx: Default param for getting the information of the caller. Nothing to do for this param
        :param channel: mention a channel to send a create-ticket message
        :return:
        """
        if not ctx.author.guild_permissions.view_audit_log:
            return await ctx.respond("권한이 없습니다.", ephemeral=True)

        embed = discord.Embed(title="도움이 필요하신가요?", color=0x967969,
                              description="다른 유저나 가이드의 도움만으로는 해결하기 힘든 상황일 경우,\n"
                                          "아래의 버튼을 눌러 더 많은 정보를 확인하세요.")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text="베어타운", icon_url=self.bot.user.avatar.url)
        await channel.send(embed=embed, view=ServerButton(self.bot))
        return await ctx.reply(f"생성이 완료되었습니다. {channel.mention}")

    @commands.command(name='clear')
    async def clear_db(self, ctx):
        """
        Delete data from database for those who cannot create a ticket
        :param ctx: Default param for getting the information of the caller. Nothing to do for this param
        :return:
        """
        if not ctx.author.guild_permissions.view_audit_log:
            return await ctx.respond("권한이 없습니다.", ephemeral=True)

        conn = sqlite3.connect('data/tickets.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM opened')
        conn.commit()
        conn.close()
        return await ctx.respond("완료", ephemeral=True)


def setup(bot):
    bot.add_cog(Ticket(bot))
