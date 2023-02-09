import discord
from modules.connection import get_ticket_data
from .create import TicketCreate


class TypeSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        self.select_options = get_ticket_data('options')
        select_options = [discord.SelectOption(label=o[1], description=o[2],
                                               emoji=o[3], value=o[0]) for o in self.select_options]
        super().__init__(placeholder="문의할 내용을 선택해 주세요.", min_values=1, max_values=1, options=select_options)

    async def callback(self, interaction: discord.Interaction):
        value = [o for o in self.select_options if o[0] == self.values[0]][0]

        if self.values[0] == 'urgent':
            embed = discord.Embed(title=f"{value[3]} {value[1]}", color=0x967969, description=value[4])
            embed.set_footer(text="베어타운", icon_url=self.bot.user.avatar.url)
            return await interaction.response.send_message(embed=embed, view=UrgentButton(self.bot), ephemeral=True)

        return await TicketCreate(self.bot, interaction, self.values[0]).create_ticket()


class UrgentButton(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label='동의합니다', style=discord.ButtonStyle.green,
                       emoji='✅', custom_id='confirm')
    async def confirm(self, button, interaction):
        return await TicketCreate(self.bot, interaction).create_urgent_ticket()
