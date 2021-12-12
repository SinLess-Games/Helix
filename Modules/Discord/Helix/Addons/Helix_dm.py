import logging
from io import StringIO
from typing import Union
from asyncio import TimeoutError

import discord
from discord.ext import commands

import constants
from utils.cooldown import CoolDown
from utils.message_logger import MessageLogger
from utils.checks import check_if_it_is_Sinless_guild
from utils.embed_handler import authored, failure, success, info, create_suggestion_msg


logger = logging.getLogger(__name__)


class UnsupportedFileExtension(Exception):
    pass


class UnsupportedFileEncoding(ValueError):
    pass


class HelixDM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tortoise_guild = bot.get_guild(constants.SinLess_guild_id)

        self.admin_role = self.tortoise_guild.get_role(constants.admin_role)
        self.moderator_role = self.tortoise_guild.get_role(constants.moderator_role)

        self.cool_down = CoolDown(seconds=120)
        self.bot.loop.create_task(self.cool_down.start())

        # Key is user id value is mod/admin id
        self.active_mod_mails = {}
        self.pending_mod_mails = set()
        self.active_event_submissions = set()
        self.active_bug_reports = set()
        self.active_suggestions = set()

        # Keys are custom emoji IDs, sub-dict message is the message appearing in the bot DM,
        # callable is the method to call when that option is selected and check is callable that returns
        # bool whether that option is disabled or not.
        # TODO if callable errors container will not be properly updated so users will not be able to call it again
        self._options = {
            constants.mod_mail_emoji_id: {
                "message": "Contact staff (mod mail)",
                "callable": self.create_mod_mail,
                "check": lambda: self.bot.tortoise_meta_cache["mod_mail"]
            },
            constants.event_emoji_id: {
                "message": "Event submission",
                "callable": self.create_event_submission,
                "check": lambda: self.bot.tortoise_meta_cache["event_submission"]
            },
            constants.bug_emoji_id: {
                "message": "Bug report",
                "callable": self.create_bug_report,
                "check": lambda: self.bot.tortoise_meta_cache["bug_report"]
            },
            constants.suggestions_emoji_id: {
                "message": "Make a suggestion",
                "callable": self.create_suggestion,
                "check": lambda: self.bot.tortoise_meta_cache["suggestions"]
            }
        }

        # User IDs for which the trigger_typing() is active, so we don't spam the method.
        self._typing_active = set()

        # Server Utility Channels
        self.bug_report_channel = bot.get_channel(constants.bug_reports_channel_id)
        self.user_suggestions_channel = bot.get_channel(constants.suggestions_channel_id)
        self.mod_mail_report_channel = bot.get_channel(constants.mod_mail_report_channel_id)
        self.code_submissions_channel = bot.get_channel(constants.code_submissions_channel_id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id is not None:
            return  # Only allow in DMs
        await self.on_raw_reaction_add_helper(payload)

    async def on_raw_reaction_add_helper(self, payload):
        user_id = payload.user_id
        user = self.bot.get_user(user_id)

        if user is None:
            # Users cannot send messages if they do not share at least one guild with the bot,
            # however they can react to messages they previously sent to bot making it possible
            # that user will be None as they do not share a guild!
            return
        if user_id == self.bot.user.id:
            return  # Ignore the bot

        if self.cool_down.is_on_cool_down(user_id):
            msg = f"You are on cooldown. You can retry after {self.cool_down.retry_after(user_id)}s"
            await user.send(embed=failure(msg))
            return
        else:
            self.cool_down.add_to_cool_down(user_id)

        for emoji_id, sub_dict in self._options.items():
            emoji = self.bot.get_emoji(emoji_id)

            if sub_dict["check"]() and emoji == payload.emoji:
                await sub_dict["callable"](user)
                break

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        elif message.guild is not None:
            return  # Functionality only active in DMs

        if self.is_any_session_active(message.author.id):
            return
        else:
            await self.send_dm_options(output=message.author)

    @commands.Cog.listener()
    async def on_typing(self, channel, user, _when):
        if not isinstance(channel, discord.DMChannel):
            return
        elif not self.is_any_session_active(user.id):
            return
        elif user.id in self._typing_active:
            return

        destination_id = self.active_mod_mails.get(user.id)
        if destination_id is None:
            # If it's None there is no user with that ID that has opened mod mail request.
            # However we can still have the mod/admin that could be attending mod mail
            destination_id = self._get_dict_key_by_value(user.id)

            if destination_id is None:
                # If it's again None then there is no such ID in either user nor mods/admins
                return

        self._typing_active.add(user.id)
        destination_user = self.bot.get_user(destination_id)
        # Per docs: Active for 10s or until first message
        await destination_user.trigger_typing()
        self._typing_active.remove(user.id)

    def _get_dict_key_by_value(self, value: int) -> int:
        for key, v in self.active_mod_mails.items():
            if v == value:
                return key

    async def send_dm_options(self, *, output):
        emoji_map = {
            self.bot.get_emoji(emoji_id): sub_dict['message']
            for emoji_id, sub_dict in self._options.items()
            if sub_dict["check"]()
        }

        if not emoji_map:
            # All DM options are disabled
            return

        msg_options = "\n\n".join(
            f"{emoji} {message}" for emoji, message in emoji_map.items()
        )
        disclaimer = (
            "Note: Abusing any of these options is punishable. Please do not use them just to test.\n"
            "Your Tortoise Community."
        )

        embed = discord.Embed(description=f"{msg_options}\n{constants.embed_space}")
        embed.set_footer(text=disclaimer)
        embed.set_thumbnail(url=str(self.tortoise_guild.icon_url))
        msg = await output.send(embed=embed)

        for emoji in emoji_map.keys():
            if emoji is None:
                logger.warning("Sending DM options failed as emoji is not found.")
                return
            else:
                await msg.add_reaction(emoji)

    def is_any_session_active(self, user_id: int) -> bool:
        # If the mod mail or anything else is active don't clutter the active session
        return any(
            user_id in active for active in (
                self.active_mod_mails.keys(),
                self.active_mod_mails.values(),
                self.active_event_submissions,
                self.active_bug_reports,
                self.active_suggestions
            )
        )

    async def create_mod_mail(self, user: discord.User):
        if user.id in self.pending_mod_mails:
            await user.send(embed=failure("You already have a pending mod mail, please be patient."))
            return

        submission_embed = authored(f"`{user.id}` submitted for mod mail.", author=user)
        # Ping roles so they get notified sooner
        await self.mod_mail_report_channel.send("@here", delete_after=30)
        await self.mod_mail_report_channel.send(embed=submission_embed)

        self.pending_mod_mails.add(user.id)
        await user.send(embed=success("Mod mail was sent to admins, please wait for one of the admins to accept."))

    async def create_event_submission(self, user: discord.User):
        user_reply = await self._get_user_reply(self.active_event_submissions, user)
        if user_reply is None:
            return

        await self.code_submissions_channel.send(
            f"User `{user}` ID:{user.id} submitted code submission: "
            f"{user_reply}"
        )
        await user.send(embed=success("Event submission successfully submitted."))
        self.active_event_submissions.remove(user.id)

    async def create_bug_report(self, user: discord.User):
        user_reply = await self._get_user_reply(self.active_bug_reports, user)
        if user_reply is None:
            return

        await self.bug_report_channel.send(f"User `{user}` ID:{user.id} submitted bug report: {user_reply}")
        await user.send(embed=success("Bug report successfully submitted, thank you."))
        self.active_bug_reports.remove(user.id)

    async def create_suggestion(self, user: discord.User):
        user_reply = await self._get_user_reply(self.active_suggestions, user)
        if user_reply is None:
            return

        msg = await create_suggestion_msg(self.user_suggestions_channel, user, user_reply)
        await self.bot.api_bot.post_suggestion(user, msg, user_reply)
        await user.send(embed=success("Suggestion successfully submitted, thank you."))
        self.active_suggestions.remove(user.id)

    async def _get_user_reply(self, container: set, user: discord.User) -> Union[str, None]:
        """
        Helper method to get user reply, only deals with errors.
        Uses self._wait_for method so it can get both the user message reply and text from attachment file.
        :param container: set, container holding active user sessions by having their IDs in it.
        :param user: Discord user to wait reply from
        :return: Union[str, None] string representing user reply, can be None representing invalid reply.
        """
        user_reply = await self._wait_for(container, user)

        if user_reply is None:
            return None

        try:
            possible_attachment = await self.get_message_txt_attachment(user_reply)
        except (UnsupportedFileExtension, UnsupportedFileEncoding) as e:
            container.remove(user.id)
            await user.send(embed=failure(f"Error: {e} , canceling."))
            return

        user_reply_content = user_reply.content if possible_attachment is None else possible_attachment

        if len(user_reply_content) < 10:
            container.remove(user.id)
            await user.send(embed=failure("Too short - seems invalid, canceling."))
            return None
        else:
            return user_reply_content

    async def _wait_for(self, container: set, user: discord.User) -> Union[discord.Message, None]:
        """
        Simple custom wait_for that waits for user reply for 5 minutes and has ability to cancel the wait,
        deal with errors and deal with containers (which mark users that are currently doing something aka
        event submission/bug report etc).
        :param container: set, container holding active user sessions by having their IDs in it.
        :param user: Discord user to wait reply from
        :return: Union[Message, None] message representing user reply, can be none representing invalid reply.
        """
        def check(msg):
            return msg.guild is None and msg.author == user

        container.add(user.id)
        await user.send(embed=info(
            "Reply with single message, link to paste service or uploading utf-8 `.txt` file.\n"
            "You have 5m, type `cancel` to cancel right away.", user)
        )

        try:
            user_reply = await self.bot.wait_for("message", check=check, timeout=300)
        except TimeoutError:
            container.remove(user.id)
            await user.send(embed=failure("You took too long to reply."))
            return

        if user_reply.content.lower() == "cancel":
            container.remove(user.id)
            await user.send(embed=success("Successfully canceled."))
            return

        return user_reply

    @classmethod
    async def get_message_txt_attachment(cls, message: discord.Message) -> Union[str, None]:
        """
        Only supports .txt file attachments and only utf-8 encoding supported.
        :param message: message object to extract attachment from.
        :return: Union[str, None]
        :raise UnsupportedFileExtension: If file type is other than .txt
        :raise UnicodeDecodeError: If decoding the file fails
        """
        try:
            attachment = message.attachments[0]
        except IndexError:
            return None

        if not attachment.filename.endswith(".txt"):
            raise UnsupportedFileExtension("Only `.txt` files supported")

        try:
            content = (await attachment.read()).decode("utf-8")
        except UnicodeDecodeError:
            raise UnsupportedFileEncoding("Unsupported file encoding, please only use utf-8")

        return content

    @commands.command()
    @commands.check(check_if_it_is_Sinless_guild)
    async def attend(self, ctx, user_id: int):
        if not any(role in ctx.author.roles for role in (self.admin_role, self.moderator_role)):
            await ctx.send(embed=failure("You do not have permission to use this command."))
            return

        # Time to wait for FIRST USER reply. Useful if mod attends but user is away.
        first_timeout = 21_600  # 6 hours
        # Flag for above variable. False means there has been no messages from the user.
        first_timeout_flag = False
        # After the user sends first reply this is the timeout we use.
        regular_timeout = 1800  # 30 min

        user = self.bot.get_user(user_id)
        mod = ctx.author

        if user is None:
            await ctx.send(embed=failure("That user cannot be found or you entered incorrect ID."))
            return
        elif user_id not in self.pending_mod_mails:
            await ctx.send(embed=failure("That user is not registered for mod mail."))
            return
        elif self.is_any_session_active(mod.id):
            await ctx.send(embed=failure("You already have one of active sessions (reports/mod mail etc)."))
            return

        try:
            await mod.send(
                embed=success(
                    f"You have accepted `{user}` mod mail request.\n"
                    "Reply here in DMs to chat with them.\n"
                    "This mod mail will be logged.\n"
                    "Type `close` to close this mod mail."
                )
            )
        except discord.HTTPException:
            await ctx.send(embed=failure("Mod mail failed to initialize due to mod having closed DMs."))
            return

        # Unlike failing for mods due to closed DMs this cannot fail for user since user already did interact
        # with bot in DMs as he needs to in order to even open mod-mail.
        await user.send(
            embed=authored(
                (
                    "has accepted your mod mail request.\n"
                    "Reply here in DMs to chat with them.\n"
                    "This mod mail will be logged, by continuing you agree to that."
                ),
                author=mod
            )
        )

        await ctx.send(embed=success("Mod mail initialized, check your DMs."))
        self.pending_mod_mails.remove(user_id)
        self.active_mod_mails[user_id] = mod.id
        _timeout = first_timeout
        # Keep a log of all messages in mod-mail
        log = MessageLogger(mod.id, user.id)

        def mod_mail_check(msg):
            return msg.guild is None and msg.author.id in (user_id, mod.id)

        while True:
            try:
                mail_msg = await self.bot.wait_for("message", check=mod_mail_check, timeout=_timeout)
                log.add_message(mail_msg)
            except TimeoutError:
                timeout_embed = failure("Mod mail closed due to inactivity.")
                log.add_embed(timeout_embed)
                await mod.send(embed=timeout_embed)
                await user.send(embed=timeout_embed)
                del self.active_mod_mails[user_id]
                await self.mod_mail_report_channel.send(file=discord.File(StringIO(str(log)), filename=log.filename))
                break

            # Deal with attachments. We don't re-upload we just copy paste attachment url.
            attachments = self._get_attachments_as_urls(mail_msg)
            mail_msg.content += attachments

            if len(mail_msg.content) > 1900:
                mail_msg.content = f"{mail_msg.content[:1900]} ...truncated because it was too long."

            # Deal with dynamic timeout.
            if mail_msg.author == user and not first_timeout_flag:
                first_timeout_flag = True
                _timeout = regular_timeout

            # Deal with canceling mod mail
            if mail_msg.content.lower() == "close" and mail_msg.author.id == mod.id:
                close_embed = success(f"Mod mail successfully closed by {mail_msg.author}.")
                log.add_embed(close_embed)
                await mod.send(embed=close_embed)
                await user.send(embed=close_embed)
                del self.active_mod_mails[user_id]
                await self.mod_mail_report_channel.send(file=discord.File(StringIO(str(log)), filename=log.filename))
                break

            # Deal with user-mod communication
            if mail_msg.author == user:
                await mod.send(mail_msg.content)
            elif mail_msg.author == mod:
                await user.send(mail_msg.content)

    @classmethod
    def _get_attachments_as_urls(cls, message: discord.Message) -> str:
        if not message.attachments:
            return ""

        urls = '\n'.join(attachment.url for attachment in message.attachments)
        return f"\nAttachments:\n{urls}"


def setup(bot):
    bot.add_cog(HelixDM(bot))