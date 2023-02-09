import discord
from modules.connection import delete_ticket_data


async def close(interaction: discord.Interaction):
    delete_ticket_data('opened', 'ticket', interaction.channel_id)
    index = interaction.channel.name.split('-')[1]
    unread = discord.PermissionOverwrite(read_messages=False, send_messages=False)
    read = discord.PermissionOverwrite(read_messages=True, send_messages=True)

    overwrites = {
        interaction.guild.default_role: unread,
        interaction.user: read,
        interaction.guild.get_role(1061118127754194954): read,
        interaction.guild.get_role(1061284441672142878): read,
        interaction.guild.get_role(1061118763551957002): read
    }

    await interaction.channel.edit(name=f'closed-{index}', overwrites=overwrites)

    embed = discord.Embed(title="티켓 닫힘", color=0x967969,
                          description=f'{interaction.user.mention} 님께서 티켓을 닫았습니다.')
    return await interaction.response.send_message(embed=embed, view=OpenTicket())


class CloseTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='닫기', style=discord.ButtonStyle.gray,
                       emoji='🔒', custom_id='close')
    async def close_ticket(self, button=None, interaction=None):
        return await close(interaction)


class OpenTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='삭제', style=discord.ButtonStyle.gray,
                       emoji='🚫', custom_id='delete')
    async def delete(self, button=None, interaction: discord.Interaction = None):
        if not interaction.user.guild_permissions.view_audit_log:
            return await interaction.response.send_message("권한이 없습니다.", ephemeral=True)
        return await interaction.channel.delete()
