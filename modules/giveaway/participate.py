import discord
import sqlite3
from ast import literal_eval


class GiveawayButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="추첨 참여", style=discord.ButtonStyle.primary, custom_id='participate')
    async def participate(self, button=None, interaction=None):
        conn = sqlite3.connect('data/event.db')
        cursor = conn.cursor()
        data = cursor.execute(f'SELECT * FROM giveaway WHERE message = "{interaction.message.id}"').fetchone()
        users = literal_eval(data[4])

        if interaction.user.id in users:
            return await interaction.response.send_message("이미 추첨에 참여하셨습니다!", ephemeral=True)
        users.append(interaction.user.id)
        cursor.execute('UPDATE giveaway SET users = ? WHERE message = ?', (str(users), interaction.message.id))
        conn.commit()
        conn.close()
        await interaction.response.send_message("추첨에 참여하셨습니다!", ephemeral=True)

        embed = interaction.message.embeds[0]
        try:
            embed.set_field_at(3, name="참여자", value=f"{len(users)}명", inline=False)
        except IndexError:
            embed.add_field(name="참여자", value=f"{len(users)}명", inline=False)

        return await interaction.message.edit(embed=embed)
