import asyncio
import os
import time
import aiohttp
from aiohttp import web
import discord
from discord.ext import commands

# ==============================================================================
# 🎓 WELCOME TO PYTHON DISCORD BOT DEVELOPMENT! (FOR COMPLETE BEGINNERS)
# ==============================================================================
# Read the green comments (#) from top to bottom! Every section explains:
#   1. WHAT the Python code is doing
#   2. WHY we write it that way
#   3. HOW you can edit it yourself
#
# HOW TO ACTIVATE THIS BOT IN DISCORD:
#   • Type `/learn` or `!learn` -> Opens the Interactive 5-Lesson Academy Panel!
#   • Type `/trainee`           -> Opens your customizable practice sandbox!
#   • Type `!ping`              -> Tests the bot's response speed!
#   • Type `!say Hello World`   -> Makes the bot repeat your message!
#   • Type `!userinfo`          -> Shows your Discord account info on an Embed!
# ==============================================================================


# ==============================================================================
# 📘 STEP 1: VARIABLES & CONFIGURATION
# In Python, a "variable" is like a labeled box that stores information.
#   • Text (Strings) goes inside quotes: "Hello"
#   • Numbers (Integers) have no quotes: 12345
#   • Lists hold multiple items inside square brackets: [1, 2, 3]
# ==============================================================================

# `os.getenv("BOT_TOKEN")` safely reads your secret Bot Token from Render
# so nobody can steal your bot password from your code file.
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# A Python list holding your server's Staff Role ID
STAFF_ROLE_IDS = [1567026563369664590]

# Tracks when the bot started so we can calculate uptime
START_TIME = time.time()
BOT_STATUS = "Starting..."


# ==============================================================================
# 📘 STEP 2: 24/7 KEEP-ALIVE WEB SERVER (FOR RENDER HOSTING)
# Why is this here?
# Free cloud hosts like Render shut down your bot if it doesn't have a web port
# or if nobody visits it for 15 minutes.
# This code creates a tiny webpage and visits itself every 4 minutes (240s)!
# ==============================================================================

async def handle_ping(request):
    uptime_minutes = int((time.time() - START_TIME) // 60)
    return web.Response(text=f"Trainee Learning Bot 24/7 | Uptime: {uptime_minutes}m | Status: {BOT_STATUS}")

async def run_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    await web.TCPSite(runner, "0.0.0.0", port).start()

async def self_ping_loop():
    await asyncio.sleep(20)
    url = os.environ.get("RENDER_EXTERNAL_URL") or f"http://127.0.0.1:{os.environ.get('PORT', 10000)}/"
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url, timeout=10):
                    pass
            except Exception:
                pass
            await asyncio.sleep(240)  # Waits 240 seconds (4 minutes), then pings again


# ==============================================================================
# 📘 STEP 3: POPUP FORMS (`discord.ui.Modal`)
# What is a Modal?
# A Modal is a popup window with text boxes that appears when a user clicks a
# button or runs a slash command.
# ==============================================================================

class PracticeModal(discord.ui.Modal, title="📝 Lesson 4: Popup Modal Form"):
    def __init__(self):
        super().__init__()

        # TextInput creates a typing box inside the popup window
        self.user_name = discord.ui.TextInput(
            label="What is your name or nickname?",
            placeholder="Type your name here...",
            required=True,
            max_length=50,
        )
        self.learned_today = discord.ui.TextInput(
            label="Write 1 thing you learned about Python today:",
            style=discord.TextStyle.paragraph,  # .paragraph makes a big multi-line box
            placeholder="e.g. I learned that 'await' lets the bot talk to Discord without freezing!",
            required=True,
            max_length=300,
        )

        # Attach both text boxes to the popup window
        self.add_item(self.user_name)
        self.add_item(self.learned_today)

    # `on_submit` runs automatically the moment the user clicks the blue "Submit" button!
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎉 Modal Form Submitted Successfully!",
            description=(
                "You just used a **`discord.ui.Modal`** class! Here is what your Python code received:\n\n"
                f"👤 **Name Input (`self.user_name.value`):** `{self.user_name.value}`\n"
                f"📘 **What You Learned (`self.learned_today.value`):**\n> {self.learned_today.value}\n\n"
                "**🔍 How this worked in Python:**\n"
                "```python\n"
                "async def on_submit(self, interaction: discord.Interaction):\n"
                "    await interaction.response.send_message(embed=embed, ephemeral=True)\n"
                "```"
            ),
            color=discord.Color.green(),
        )
        # `ephemeral=True` makes the reply private so ONLY the person who clicked can see it!
        await interaction.response.send_message(embed=embed, ephemeral=True)


# ==============================================================================
# 📘 STEP 4: INTERACTIVE LEARNING ACADEMY BUTTONS (`discord.ui.View`)
# What is a View?
# A `View` is a container that holds clickable buttons under a message.
#
# CRITICAL 24/7 RULE:
# Always set `super().__init__(timeout=None)` and give every button a unique
# `custom_id="..."` so buttons never stop working!
# ==============================================================================

class AcademyLessonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # ---------------- LESSON 1 BUTTON: PYTHON BASICS ----------------
    @discord.ui.button(label="Lesson 1: async & await", style=discord.ButtonStyle.primary, emoji="🐍", custom_id="acad:l1", row=0)
    async def lesson_1_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🐍 Lesson 1: Why Do Bots Use `async def` and `await`?",
            description=(
                "In normal Python, code runs one line at a time and freezes while waiting. "
                "In Discord, 100 people might click buttons at the exact same second!\n\n"
                "### 🔑 The 2 Magic Keywords:\n"
                "1️⃣ **`async def`** — Defines an *asynchronous function* (a task that can run without freezing the bot).\n"
                "2️⃣ **`await`** — Used whenever the bot sends or fetches data from Discord over the internet.\n\n"
                "### 💻 Example Code:\n"
                "```python\n"
                "# Whenever we talk to Discord, we put 'await' in front:\n"
                "async def greet_user(ctx):\n"
                "    await ctx.send('Hello from Python!')\n"
                "```\n"
                "💡 **Rule of Thumb:** If an action sends a message, edits an embed, kicks a user, or waits on Discord, put **`await`** in front of it!"
            ),
            color=discord.Color.blurple(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # ---------------- LESSON 2 BUTTON: DISCORD EMBEDS ----------------
    @discord.ui.button(label="Lesson 2: Embeds", style=discord.ButtonStyle.primary, emoji="🎨", custom_id="acad:l2", row=0)
    async def lesson_2_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🎨 Lesson 2: How to Build a Discord Embed",
            description=(
                "An **Embed** is this colored card box you are reading right now! "
                "Here is the exact Python code used to create an Embed:\n\n"
                "```python\n"
                "embed = discord.Embed(\n"
                "    title='My First Embed',\n"
                "    description='This is the main text!',\n"
                "    color=discord.Color.gold()\n"
                ")\n"
                "embed.add_field(name='Field 1', value='Hello!', inline=True)\n"
                "embed.set_footer(text='Bottom footer text')\n"
                "await ctx.send(embed=embed)\n"
                "```"
            ),
            color=discord.Color.gold(),
        )
        embed.add_field(name="📌 Inline Field 1", value="Created with `add_field()`", inline=True)
        embed.add_field(name="📌 Inline Field 2", value="Sits side-by-side!", inline=True)
        embed.set_footer(text="This is the footer created with embed.set_footer()!")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # ---------------- LESSON 3 BUTTON: CLICKABLE BUTTONS ----------------
    @discord.ui.button(label="Lesson 3: Buttons", style=discord.ButtonStyle.success, emoji="🔘", custom_id="acad:l3", row=0)
    async def lesson_3_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🔘 Lesson 3: How Clickable Buttons Work",
            description=(
                f"You just clicked a button, and Discord sent an **`interaction`** object from {interaction.user.mention} to Python!\n\n"
                "### 💻 How This Exact Button Is Coded:\n"
                "```python\n"
                "class MyView(discord.ui.View):\n"
                "    def __init__(self):\n"
                "        super().__init__(timeout=None) # Keeps button active 24/7!\n\n"
                "    @discord.ui.button(\n"
                "        label='Click Me',\n"
                "        style=discord.ButtonStyle.success,\n"
                "        emoji='🔘',\n"
                "        custom_id='my_unique_id'\n"
                "    )\n"
                "    async def my_btn(self, interaction: discord.Interaction, button: discord.ui.Button):\n"
                "        await interaction.response.send_message('You clicked me!', ephemeral=True)\n"
                "```\n"
                "### 🎨 Button Styles (Colors):\n"
                "• `ButtonStyle.primary` -> 🟦 Blurple (Blue)\n"
                "• `ButtonStyle.success` -> 🟩 Green\n"
                "• `ButtonStyle.danger`  -> 🟥 Red\n"
                "• `ButtonStyle.secondary` -> ⬛ Grey"
            ),
            color=discord.Color.green(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # ---------------- LESSON 4 BUTTON: POPUP MODAL ----------------
    @discord.ui.button(label="Lesson 4: Test Popup Form", style=discord.ButtonStyle.secondary, emoji="📝", custom_id="acad:l4", row=1)
    async def lesson_4_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Opens the popup form we created in STEP 3!
        await interaction.response.send_modal(PracticeModal())

    # ---------------- LESSON 5 BUTTON: GRADUATION CHALLENGE ----------------
    @discord.ui.button(label="Lesson 5: Your First Coding Tasks", style=discord.ButtonStyle.danger, emoji="🏆", custom_id="acad:l5", row=1)
    async def lesson_5_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🏆 Lesson 5: Trainee Hands-On Coding Challenge!",
            description=(
                "Ready to write your own Python code? Open **`trainee_starter_bot.py`** and complete these 3 beginner tasks:\n\n"
                "### ✅ Task 1: Change an Embed Color\n"
                "Find the `/trainee` command near the bottom of `trainee_starter_bot.py` and change `discord.Color.blurple()` to `discord.Color.green()`.\n\n"
                "### ✅ Task 2: Add Your Own Button\n"
                "Inside `TraineeSandboxView`, copy the example button and add a new button labeled `'👋 Say Hi'` that replies with `'Hello from my first custom button!'`.\n\n"
                "### ✅ Task 3: Create Your Own Command\n"
                "Copy the `!ping` command and create a new command called `!hello` that makes the bot reply with your name!"
            ),
            color=discord.Color.orange(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


# ==============================================================================
# 📘 STEP 5: TRAINEE SANDBOX VIEW (EDIT THIS CLASS FOR YOUR PRACTICE!)
# ==============================================================================

class TraineeSandboxView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Test Sandbox Button", style=discord.ButtonStyle.success, emoji="⚡", custom_id="sandbox:click")
    async def test_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        # 🛠️ TRAINEE TASK: Try changing the message inside send_message below!
        await interaction.response.send_message(
            f"✅ Awesome job {interaction.user.mention}! You triggered `test_btn` inside `TraineeSandboxView`!",
            ephemeral=True,
        )

    @discord.ui.button(label="Open Practice Form", style=discord.ButtonStyle.primary, emoji="📝", custom_id="sandbox:modal")
    async def modal_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PracticeModal())


# ==============================================================================
# 📘 STEP 6: THE BOT CLASS & EVENTS (`setup_hook`, `on_ready`, `on_message`)
# What is an Event?
# Events are functions that Discord triggers automatically when something happens:
#   • `setup_hook` -> Runs when the bot is booting up (registers buttons & slash commands)
#   • `on_ready`   -> Runs as soon as the bot is logged in and online
#   • `on_message` -> Runs every time someone sends a message in any channel
# ==============================================================================

class TraineeBot(commands.Bot):
    def __init__(self, msg_intent: bool = True):
        intents = discord.Intents.default()
        intents.message_content = msg_intent  # Allows the bot to read "!commands"
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def setup_hook(self):
        # Register our Views so buttons work 24/7 even after a restart
        self.add_view(AcademyLessonView())
        self.add_view(TraineeSandboxView())
        # Sync all `/slash` commands with Discord
        await self.tree.sync()

    async def on_ready(self):
        global BOT_STATUS
        BOT_STATUS = f"ONLINE as {self.user}"
        print(f"✅ Trainee Learning Bot is ONLINE as {self.user}")

    async def on_message(self, message: discord.Message):
        # ⚠️ IMPORTANT RULE: Always ignore messages from bots so the bot never loops forever!
        if message.author.bot:
            return

        # Required so "!ping", "!learn", etc. continue to work when using on_message
        await self.process_commands(message)


# ==============================================================================
# 📘 STEP 7: COMMANDS (`!prefix` AND `/slash` COMMANDS)
# Here is where we create the commands you type in Discord!
# ==============================================================================

def make_academy_embed() -> discord.Embed:
    return discord.Embed(
        title="🎓 Python & Discord Bot Development Academy",
        description=(
            "Welcome, Trainee! Click each lesson button below in order to learn how Python Discord bots work from scratch:\n\n"
            "🐍 **Lesson 1: `async` & `await`** — Understand non-blocking Python functions\n"
            "🎨 **Lesson 2: Discord Embeds** — Learn how colored Embed cards are built\n"
            "🔘 **Lesson 3: Interactive Buttons** — See how `discord.ui.View` handles clicks\n"
            "📝 **Lesson 4: Popup Forms (Modals)** — Test a real popup form & see the code\n"
            "🏆 **Lesson 5: Your First Coding Tasks** — 3 easy challenges to try in `trainee_starter_bot.py`!"
        ),
        color=discord.Color.blurple(),
    )

def register_commands(bot: TraineeBot):
    # -------------------- 1. /learn & !learn (Academy Panel) --------------------
    @bot.command(name="learn", aliases=["academy", "lessons"])
    async def learn_prefix(ctx: commands.Context):
        await ctx.send(embed=make_academy_embed(), view=AcademyLessonView())

    @bot.tree.command(name="learn", description="Open the interactive 5-Lesson Python & Discord Bot Academy")
    async def learn_slash(interaction: discord.Interaction):
        await interaction.response.send_message(embed=make_academy_embed(), view=AcademyLessonView())

    # -------------------- 2. /trainee & !trainee (Practice Sandbox) --------------------
    @bot.command(name="trainee")
    async def trainee_prefix(ctx: commands.Context):
        # 🛠️ TRAINEE TASK 1: Try changing discord.Color.blurple() to discord.Color.green()!
        embed = discord.Embed(
            title="🧪 Trainee Practice Sandbox",
            description="Edit this embed inside `trainee_starter_bot.py` to test your own changes!",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="👤 Opened By", value=ctx.author.mention, inline=True)
        embed.add_field(name="🟢 Bot Status", value="24/7 Active", inline=True)
        await ctx.send(embed=embed, view=TraineeSandboxView())

    @bot.tree.command(name="trainee", description="Open your customizable Trainee Practice Sandbox")
    async def trainee_slash(interaction: discord.Interaction):
        embed = discord.Embed(
            title="🧪 Trainee Practice Sandbox",
            description="Edit this embed inside `trainee_starter_bot.py` to test your own changes!",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="👤 Opened By", value=interaction.user.mention, inline=True)
        embed.add_field(name="🟢 Bot Status", value="24/7 Active", inline=True)
        await interaction.response.send_message(embed=embed, view=TraineeSandboxView())

    # -------------------- 3. !ping (Simple Prefix Command) --------------------
    @bot.command(name="ping")
    async def ping_cmd(ctx: commands.Context):
        latency_ms = round(bot.latency * 1000)
        await ctx.send(f"🏓 **Pong!** Bot latency is `{latency_ms}ms`.")

    # -------------------- 4. !say <text> (Command with Arguments) --------------------
    @bot.command(name="say")
    async def say_cmd(ctx: commands.Context, *, text: str = "You forgot to type a message! Example: `!say Hello`"):
        await ctx.send(f"🗣️ **{ctx.author.display_name} says:** {text}")

    # -------------------- 5. !userinfo [@member] (Reading Discord Member Data) --------------------
    @bot.command(name="userinfo", aliases=["whois"])
    async def userinfo_cmd(ctx: commands.Context, member: discord.Member = None):
        target = member or ctx.author
        created_date = target.created_at.strftime("%B %d, %Y")
        emb = discord.Embed(title=f"👤 User Info: {target.display_name}", color=discord.Color.teal())
        emb.set_thumbnail(url=target.display_avatar.url)
        emb.add_field(name="🆔 User ID", value=f"`{target.id}`", inline=True)
        emb.add_field(name="📅 Account Created", value=created_date, inline=True)
        emb.add_field(name="🎭 Roles Count", value=f"`{len(target.roles) - 1}` roles", inline=True)
        await ctx.send(embed=emb)


# ==============================================================================
# 📘 STEP 8: STARTING THE BOT (`main()`)
# ==============================================================================

async def main():
    await run_web_server()
    asyncio.create_task(self_ping_loop())
    if not BOT_TOKEN:
        print("❌ ERROR: BOT_TOKEN environment variable is missing!")
        while True:
            await asyncio.sleep(3600)

    bot = TraineeBot(True)
    register_commands(bot)
    try:
        await bot.start(BOT_TOKEN)
    except discord.PrivilegedIntentsRequired:
        await bot.close()
        bot = TraineeBot(False)
        register_commands(bot)
        await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
