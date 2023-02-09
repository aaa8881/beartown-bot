import discord
from discord.ext import commands, tasks
from modules import *


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status_loop.start()

    @tasks.loop(minutes=10)
    async def status_loop(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(1061614195063394374)
        try:
            return await channel.edit(name=f"👥 | 멤버수: {channel.guild.member_count}")
        except discord.HTTPException:
            pass

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        try:
            custom_id = interaction.data['custom_id']
            if custom_id == 'create-ticket':
                return await ServerButton(self.bot).create_button(interaction)
            elif custom_id == 'close':
                return await CloseTicket().close(interaction=interaction)
            elif custom_id == 'delete':
                return await interaction.channel.delete()
            elif custom_id == 'participate':
                return await GiveawayButton().participate(interaction=interaction)
            elif custom_id == 'verify-role':
                role = interaction.guild.get_role(1061120395639529562)
                await interaction.user.add_roles(role)
                return await interaction.response.send_message('역할이 지급되었습니다.', ephemeral=True)
        except (discord.HTTPException, discord.InteractionResponded, KeyError, TypeError):
            return None


def setup(bot):
    bot.add_cog(Event(bot))
