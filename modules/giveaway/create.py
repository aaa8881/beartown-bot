import time
import sqlite3
import discord
from datetime import datetime
from .participate import GiveawayButton


def convert_time(t):
    if len(str(t)) == 1:
        return f"0{t}"
    return t


class GiveawayForm(discord.ui.Modal):
    def __init__(self, bot):
        super().__init__(title='추첨 생성', custom_id="giveaway_form")
        self.bot = bot
        self.add_item(discord.ui.InputText(placeholder="당첨자에게 지급할 재화와 그 양을 입력해주세요",
                                           label="당첨 보상", style=discord.InputTextStyle.short))
        self.add_item(discord.ui.InputText(placeholder="추첨할 인원을 입력해주세요", label="인원",
                                           style=discord.InputTextStyle.short))

        now = datetime.now()
        self.add_item(discord.ui.InputText(placeholder="마감 시각을 입력해주세요", label="마감 시각",
                                           value=f"{now.year}-{convert_time(now.month)}-{convert_time(now.day + 1)} "
                                                 f"{convert_time(now.hour)}:{convert_time(now.minute)}",
                                           style=discord.InputTextStyle.short))

    async def callback(self, interaction: discord.Interaction):
        try:
            int(self.children[1].value)
        except ValueError:
            return await interaction.response.send_message("숫자만 입력해주세요.")

        conn = sqlite3.connect('data/event.db')
        cursor = conn.cursor()

        target = self.children[2].value
        convert = datetime.strptime(target, "%Y-%m-%d %H:%M")
        timestamp = int(convert.timestamp())

        if time.time() >= timestamp:
            return await interaction.response.send_message("이미 마감 시각이 지났습니다.", ephemeral=True)

        channel = self.bot.get_channel(1060943947054194708)
        embed = discord.Embed(title="추첨", color=0x967969)
        embed.add_field(name="당첨 보상", value=self.children[0].value, inline=False)
        embed.add_field(name="추첨 인원", value=self.children[1].value, inline=False)
        embed.add_field(name="남은 시간", value=f"<t:{timestamp}:R>", inline=False)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text="베어타운", icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        msg = await channel.send(embed=embed, view=GiveawayButton())

        cursor.execute(f'INSERT INTO giveaway VALUES ("{self.children[0].value}", '
                       f'"{self.children[1].value}", "{timestamp}", "{msg.id}", "[]")')
        conn.commit()
        conn.close()
        return await interaction.response.send_message("추첨이 생성되었습니다.", ephemeral=True)
