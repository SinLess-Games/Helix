import logging
import math
import sys
import traceback

import discord
from discord.ext import commands

from Helix.utils.embed_handler import failure

logger = logging.getLogger(__name__)


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error_):
        # Get the original exception
        error = getattr(error_, "original", error_)

        # If command has local error handler, ignore
        if hasattr(ctx.command, "on_error"):
            pass

        # TODO Here it should ignore if cog has local handler (cog_command_error) to prevent duplicate messages

        elif isinstance(error, commands.CommandNotFound):
            pass

        elif isinstance(error, commands.BotMissingPermissions):
            missing_perms = self._get_missing_permission(error)
            message = f"I need the **{missing_perms}** permission(s) to run this command."
            await ctx.send(embed=failure(message))

        elif isinstance(error, commands.MissingPermissions):
            missing_perms = self._get_missing_permission(error)
            message = f"You need the **{missing_perms}** permission(s) to use this command."
            await ctx.send(embed=failure(message))

        elif isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown, please retry in {math.ceil(error.retry_after)}s."
            await ctx.send(embed=failure(message))

        elif isinstance(error, commands.UserInputError):
            await ctx.send(embed=failure(f"Invalid command input: {error}"))

        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(embed=failure("This command cannot be used in direct messages."))
            except discord.Forbidden:
                pass

        elif isinstance(error, commands.CheckFailure):
            # All arguments including error message are eaten and pushed to .args
            if error.args:
                await ctx.send(embed=failure(". ".join(error.args)))
            else:
                await ctx.send(embed=failure("You do not have permission to use this command."))

        elif isinstance(error, discord.Forbidden):
            if error.code == 50007:
                # code 50007: Cannot send messages to this user.
                # Ignore this error if it's because user closed DMs
                pass
            else:
                await ctx.send(embed=failure(f"{error}"))

        elif isinstance(error, commands.CommandInvokeError):
            print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
            traceback.print_tb(error.original.__traceback__)
            print(
                f'{error.original.__class__.__name__}: {error.original}', file=sys.stderr)

        else:
            error_type = type(error)
            feedback_message = f"Uncaught {error_type} exception in command '{ctx.command}'"
            traceback_message = traceback.format_exception(etype=error_type, value=error, tb=error.__traceback__)
            log_message = f"{feedback_message} {traceback_message}"
            logger.critical(log_message)
            await self.bot.log_error(log_message)

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound,)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

        # if command has local error handler, return
        if hasattr(ctx.command, 'on_error'):
            return

        # get the original exception
        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'I need the **{}** permission(s) to run this command.'.format(fmt)
            await ctx.send(_message)
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send('This command has been disabled.')
            return

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("This command is on cool down, please retry in {}s.".format(math.ceil(error.retry_after)))
            return

        if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
            await ctx.send(_message)
            return

        if isinstance(error, commands.UserInputError):
            await ctx.send("Invalid input.")
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send('This command cannot be used in direct messages.')
            except discord.Forbidden:
                pass
            return

        if isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permission to use this command.")
            return

        # ignore all other exception types, but print them to stderr
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)

        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @classmethod
    def _get_missing_permission(cls, error) -> str:
        missing_perms = [perm.replace("_", " ").replace("guild", "server").title() for perm in error.missing_perms]

        if len(missing_perms) > 2:
            message = f"{'**, **'.join(missing_perms[:-1])}, and {missing_perms[-1]}"
        else:
            message = " and ".join(missing_perms)

        return message


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
