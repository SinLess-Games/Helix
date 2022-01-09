import logging

from discord import Member, Embed, Message, Color, Forbidden
from discord.ext import commands

from Helix import constants
from Helix.api_client import ResponseCodeError
from Helix.utils.checks import check_if_it_is_Sinless_guild, Helix_bot_developer_only
from Helix.utils.converters import DatabaseMember
from Helix.utils.embed_handler import failure, success, goodbye, info, thumbnail

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class HelixAPI(commands.Cog):
    """Commands using Helix API"""

    def __init__(self, client):
        self.client: client = client
        self.system_log_channel = client.get_channel(constants.system_log_channel_id)
        self.user_suggestions_channel = client.get_channel(constants.suggestions_channel_id)

    @commands.command()
    @commands.check(check_if_it_is_Sinless_guild)
    async def is_verified(self, ctx, member: DatabaseMember):
        try:
            response = await self.client.api_client.is_verified(member)
        except ResponseCodeError as e:
            msg = f"Something went wrong, got response status {e.status}.\nDoes the member exist?"
            await ctx.send(embed=failure(msg))
        else:
            await ctx.send(embed=info(f"Verified: {response}", ctx.me, title=f"{member}"))

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def show_data(self, ctx, member: DatabaseMember):
        try:
            data = await self.client.api_client.get_member_data(member)
        except ResponseCodeError as e:
            msg = f"Something went wrong, got response status {e.status}.\nDoes the member exist?"
            await ctx.send(embed=failure(msg))
        else:
            pretty = "\n".join(f"{key}:{value}\n" for key, value in data.items())
            await ctx.send(embed=info(pretty, ctx.me, "Member data"))

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        logger.debug(f"Member {member} left, updating database accordingly.")
        await self.client.api_client.member_left(member)
        await self.system_log_channel.send(embed=goodbye(f"{member} has left the SinLess Games Community."))

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def approve(self, ctx, message_id: int, *, reason: str = "No reason specified"):
        """Approve a suggestion"""
        await self._suggestion_helper(ctx, message_id, reason, constants.SuggestionStatus.approved)
        await ctx.send(embed=success("Suggestion successfully approved."), delete_after=5)

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def deny(self, ctx, message_id: int, *, reason: str = "No reason specified"):
        """Deny a suggestion"""
        await self._suggestion_helper(ctx, message_id, reason, constants.SuggestionStatus.denied)
        await ctx.send(embed=success("Suggestion successfully denied."), delete_after=5)

    async def _suggestion_helper(
            self,
            ctx,
            message_id: int,
            reason: str,
            status: constants.SuggestionStatus
    ):
        """
        Helper for suggestion approve/deny.
        :param ctx: context where approve/deny command was called.
        :param message_id: suggestion message id
        :param reason: reason for approving/denying
        :param status: either constants.SuggestionStatus.approved or constants.SuggestionStatus.denied
        :return:
        """
        msg: Message = await self.user_suggestions_channel.fetch_message(message_id)
        if msg is None:
            return await ctx.send(embed=failure("Suggestion message not found."), delete_after=10)
        elif not msg.embeds or not msg.embeds[0].fields:
            return await ctx.send(embed=failure("Message is not in correct format."), delete_after=10)

        api_data = await self.client.api_client.get_suggestion(message_id)

        msg_embed = msg.embeds[0]
        if status == constants.SuggestionStatus.denied:
            field_title = "Reason"
            state = "denied"
            msg_embed.colour = Color.red()
        else:
            field_title = "Comment"
            state = "approved"
            msg_embed.colour = Color.green()

        dm_embed_msg = (
            f"Your suggestion[[link]]({msg.jump_url}) was **{state}**:\n"
            f"```\"{api_data['brief'][:200]}\"```\n"
            f"\nReason:\n{reason}"
        )
        dm_embed = thumbnail(dm_embed_msg, member=ctx.me, title=f"Suggestion {state}.")

        msg_embed.set_field_at(0, name="Status", value=status.value)

        if len(msg_embed.fields) == 1:
            msg_embed.add_field(name=field_title, value=reason, inline=True)
        else:
            msg_embed.set_field_at(1, name=field_title, value=reason, inline=True)

        await self.client.api_client.edit_suggestion(message_id, status, reason)
        await msg.edit(embed=msg_embed)
        await self._dm_member(api_data["author_id"], dm_embed)

    async def _dm_member(self, user_id, embed: Embed):
        try:
            user = self.client.get_user(user_id)
            await user.send(embed=embed)
        except Forbidden:
            pass

    @commands.command()
    @commands.check(Helix_bot_developer_only)
    async def delete_suggestion(self, ctx, message_id: int):
        """Delete a suggestion"""
        msg: Message = await self.user_suggestions_channel.fetch_message(message_id)
        if msg is not None:
            await msg.delete()

        await self.client.api_client.delete_suggestion(message_id)
        await ctx.send(embed=success("Suggestion successfully deleted."), delete_after=5)


def setup(client):
    client.add_cog(HelixAPI(client))
