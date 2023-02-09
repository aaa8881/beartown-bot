import discord
from discord.ext import commands


class VerifyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='역할받기', style=discord.ButtonStyle.primary, custom_id='verify-role')
    async def role(self, button, interaction):
        role = interaction.guild.get_role(1061120395639529562)
        await interaction.user.add_roles(role)
        return await interaction.response.send_message('역할이 지급되었습니다.', ephemeral=True)


class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Member join event handler
        :param member: Default param for getting the joined member. Nothing to do for this param
        :return
        """
        if member.guild.id != 860930425811894313:
            return None

        channel = self.bot.get_channel(860930425811894316)
        rule = self.bot.get_channel(1061090011220545547)
        embed = discord.Embed(title="환영합니다!", color=0x967969,
                              description=f"안녕하세요 {member.mention}님, "
                                          f"베어타운에 오신 것을 환영합니다!\n"
                                          f"{rule.mention} 채널에서 서버 규칙을 확인하신 후,\n"
                                          f"채널 하단의 메시지에 버튼을 눌러 역할을 획득해 주세요.")
        embed.set_author(name=member, icon_url=getattr(member.avatar, 'url', self.bot.user.avatar.url))
        embed.set_thumbnail(url=member.guild.icon.url)
        embed.set_footer(text="베어타운", icon_url=self.bot.user.avatar.url)
        return await channel.send(member.mention, embed=embed)

    @commands.command(name='verify')
    async def verify_create(self, ctx, channel: discord.TextChannel):
        """
        Create get-role message
        :param ctx: Default param for getting the information of the caller. Nothing to do for this param
        :param channel: mention a channel to send a get-role message
        :return:
        """
        if not ctx.author.guild_permissions.view_audit_log:
            return await ctx.respond("권한이 없습니다.", ephemeral=True)

        embed = discord.Embed(title="역할받기", color=0x967969,
                              description="규칙을 숙지하셨다면 아래의 버튼을 눌러 역할을 받아주세요.")
        embed.set_footer(text="베어타운", icon_url=self.bot.user.avatar.url)
        await channel.send(embed=embed, view=VerifyButton())

        return await ctx.reply(f"생성이 완료되었습니다. {channel.mention}")


def setup(bot):
    bot.add_cog(Join(bot))
