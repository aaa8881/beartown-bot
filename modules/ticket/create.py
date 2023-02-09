import discord
from modules.connection import *
from .close import CloseTicket


class TicketCreate:
    def __init__(self, bot, interaction: discord.Interaction, opt='urgent'):
        self.bot = bot
        self.interaction = interaction
        self.opt = opt

    @staticmethod
    def indexing(num: int):
        return f"{'0' * (4 - len(str(num)))}{num}"

    async def create(self):
        read = discord.PermissionOverwrite(read_messages=True)

        overwrites = {
            self.interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            self.interaction.guild.get_role(860930902149693470): read,
            self.interaction.guild.get_role(1061118763551957002): read,
            self.interaction.guild.get_role(1061284441672142878): read,
            self.interaction.guild.get_role(1061118127754194954): read,
            self.interaction.user: read
        }

        index = get_index() + 1
        user = [u for u in get_ticket_data('opened') if u[1] == self.interaction.user.id]

        if user:
            return await self.interaction.response.send_message("이미 생성된 티켓이 존재합니다. "
                                                                "생성된 티켓을 닫은 뒤 새로 티켓을 생성해 주세요.", ephemeral=True)

        category = self.bot.get_channel(1060950171833335838)
        option = [o for o in get_ticket_data('options') if o[0] == self.opt][0]

        channel = await category.create_text_channel(name=f'{option[0]}-{self.indexing(index)}', overwrites=overwrites)
        save_index(index, channel.id, self.interaction.user.id)

        await self.interaction.response.send_message(f"티켓이 생성되었습니다. {channel.mention}", ephemeral=True)
        return channel, option

    async def create_ticket(self):
        channel, option = await self.create()
        embed = discord.Embed(title=f"{option[3]} {option[1]}", description=option[4], color=0x967969)
        embed.set_footer(text="베어타운", icon_url=self.bot.user.avatar.url)
        return await channel.send(self.interaction.user.mention, embed=embed, view=CloseTicket())

    async def create_urgent_ticket(self):
        channel, option = await self.create()

        embed = discord.Embed(title="티켓 열림", color=0x967969,
                              description='긴급 문의 티켓이 생성되었습니다. 문의하실 내용을 입력해주세요.')
        embed.set_footer(text="베어타운", icon_url=self.bot.user.avatar.url)
        return await channel.send('<@244070533241634816> <@259350454452879362>', embed=embed, view=CloseTicket())
