import discord
from .menu import TypeSelect


class ServerButton(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label='문의하기', style=discord.ButtonStyle.primary, custom_id='create-ticket')
    async def create_ticket(self, button, interaction):
        return await self.create_button(interaction)

    async def create_button(self, interaction: discord.Interaction):
        embed = discord.Embed(title="문의 내용을 선택해 주세요", color=0x967969,
                              description="어떤 부분에서 문제가 발생하였는지 선택해 주세요.\n")
        embed.add_field(name="주의사항", value="당장 고치지 않으면 서버 경제, 운영에 막대한 지장이 생길 수 있는 버그, "
                                           "서버 다운 등의 치명적인 문제가 아닐 경우, 관리자를 멘션하지 말아주세요.")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text="베어타운", icon_url=self.bot.user.avatar.url)
        view = discord.ui.View(timeout=None)
        view.add_item(TypeSelect(self.bot))
        return await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
