import os.path

from aenum import Enum, NoAlias
from discord import Color

AUDIO_CACHE_PATH = os.path.join(os.getcwd(), 'audio_cache')
DISCORD_MSG_CHAR_LIMIT = 4000

SinLess_guild_id = 765715864656936981
website_url = ""
privacy_url = ""
rules_url = ""
verification_url = ""
github_repo_link = "https://github.com/SinLess-Games/Helix/"
Helix_paste_service_link = ""
Helix_paste_endpoint = ""
line_img_url = "https://cdn.discordapp.com/attachments/649868379372388352/723173852796158062/animated-line.gif"
github_repo_stats_endpoint = "https://api.github.com/repos/SinLess-Games/"
project_url = "https://github.com/SinLess-Games/Helix/projects/5"

# Channel IDs
welcome_channel_id = ''
announcements_channel_id = ''
react_for_roles_channel_id = ''

mod_mail_report_channel_id = ''
bug_reports_channel_id = ''
code_submissions_channel_id = ''
suggestions_channel_id = ''

# Log Channel IDs
system_log_channel_id = ""
deterrence_log_channel_id = ""
bot_log_channel_id = ""
successful_verifications_channel_id = ""
verification_channel_id = ""
website_log_channel_id = ""
bot_dev_channel_id = ""
error_log_channel_id = ""
member_count_channel_id = ""
general_channel_id = ""
staff_channel_id = ""

# Roles
muted_role_id = ''
verified_role_id = ''
trusted_role_id = ''
moderator_role = ''
admin_role = ''
new_member_role = ''

self_assignable_roles = {
    915075587972927529: 589128905290547217,  # Python
    915075639558668289: 589129320480636986,  # Javascript
    915075723277008927: 591254311162347561,  # HTML/CSS
    915075796585041951: 589131126619111424,  # SQL
    915075807184031814: 589131022520811523,  # C
    915075858799136778: 589129873809735700,  # C++
    915075894773682197: 589130125208190991,  # C#
    915075923395608608: 589129070609039454,  # Java
    915075953204551740: 589129583375286415,  # R
    915076028332933190: 610834658267103262,  # events
    915076062361296897: 603157798225838101,  # announcements
    915076104149139457: 781210603997757471  # challenges
}

# Badges
partner = "<:partner:753957703155449916>"
staff = "<:staff:753957681336942673>"
nitro = "<:nitro:753957661912989747>"
hs_bal = "<:balance:753957264460873728>"
hs_bril = "<:brilliance:753957311537479750>"
hs_brav = "<:bravery:753957296475996234>"
hs_ev = "<:events:753957640069185637>"
verified_bot_dev = "<:dev:753957609328869384>"
bg_1 = "<:bug1:753957385844031538>"
bg_2 = "<:bug2:753957425664753754>"
ear_supp = "<:early:753957626097696888>"

# Icons
google_icon = "https://www.freepnglogos.com/uploads/google-logo-png/" \
              "google-logo-png-google-icon-logo-png-transparent-svg-vector-bie-supply-14.png"
stack_overflow_icon = "https://cdn2.iconfinder.com/data/icons/social-icons-color/512/stackoverflow-512.png"

# Emotes
idle = "🌙"
game_emoji = "🎮"
online = "<:online:753999406562410536>"
offline = "<:offline:753999424446922782>"
dnd = "<:dnd:753999445728952503>"
spotify_emoji = "<:spotify:754238046123196467>"
tick_yes = "<:tickyes:758291659330420776>"
tick_no = "<:tickno:753974818549923960>"
pin_emoji = "<:pinunread:754233175244537976>"
user_emoji = "<:user:754234411922227250>"
git_start_emoji = "<:git_star:758616139646763064>"
git_fork_emoji = "<:git_fork:758616130780004362>"
git_commit_emoji = "<:git_commit:758616123590574090>"
git_repo_emoji = "<:repo:758616137977561119>"
success_emoji = "<:success:781891698590482442>"
failure_emoji = "<:failure:781891692160090143>"

# Emoji IDs
mod_mail_emoji_id = 706195614857297970
event_emoji_id = 611403448750964746
bug_emoji_id = 723274927968354364
suggestions_emoji_id = 613185393776656384
verified_emoji_id = 610713784268357632
upvote_emoji_id = 741202481090002994
hit_emoji_id = 755715814883196958
stay_emoji_id = 755717238732095562
double_emoji_id = 755715816657518622
blank_card_emoji = "<:card:755715225642336287>"

# Special
Helix_developers = (241693350711787522)

# Embeds are not monospaced so we need to use spaces to make different lines "align"
# But discord doesn't like spaces and strips them down.
# Using a combination of zero width space + regular space solves stripping problem.
embed_space = "\u200b "

# After this is exceeded the link to tortoise paste service should be sent
max_message_length = 1000

# Music Options
# For all options see:
# https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0"  # ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}


class Infraction(Enum):
    _settings_ = NoAlias

    warning = Color.gold()
    kick = Color.gold()
    ban = Color.red()


class SuggestionStatus(Enum):
    under_review = "Under Review"
    denied = "Denied"
    approved = "Approved"


# These are allowed but will get deleted and bot will upload them to pastebin and provide the link to paste
# The message will be deletable by the author by reacting to emoji (wrong code, token leak)
extension_to_pastebin = (
    # Markdown/text based
    "css", "less",
    "csv",
    "htm", "html", "xhtml",
    "ini", "cfg",
    "json", "json5", "yaml", "toml",
    "log",
    "txt", "md", "markdown",
    "xml",
    # Programming languages
    "c", "cpp", "h",
    "cs",
    "go",
    "hs",
    "java",
    "js", "ts", "coffee",
    "kt",
    "lisp",
    "lua",
    "php",
    "pl",
    "py", "pyx",
    "r",
    "rb",
    "rs",
    "swift",
    "vb",
)

# These are allowed and will not get auto-deleted by bot nor will they get a paste link.
allowed_file_extensions = (
    # Audio
    "aif",
    "mid", "midi",
    "mp3",
    "mpa",
    "ogg",
    "wav",
    "wma",

    # Images
    "bmp",
    "gif",
    "jpg", "jpeg",
    "png",
    "svg",
    "tif", "tiff",
    "webp",

    # Video
    "3g2",
    "3gp",
    "avi",
    "h264",
    "mkv",
    "mov", "qt",
    "mp4", "m4v",
    "mpg", "m2v", "mp2", "mpe", "mpeg", "mpv",
    "ogv",
    "webm",
    "wmv",

    # Document/misc
    "doc", "docx",
    "odt",
    "pdf",
    "rtf",
)
