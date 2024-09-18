import discord
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.members = True  # Enable member-related events

bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = 'ODgwMjE5NzY0MTM0NDA4MjMy.GyPyfw.5u5ouqWgLvgNGDwYTwShGzPVDU56eK6GXFguZM'
GUILD_ID = 1278446879801212999  # Replace with your guild ID
ROLE_NAME = 'Member'  # Replace with the name of the role you want to assign
CHANNEL_ID = 1285923139477573723  # The ID of the channel to send the message to

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=ROLE_NAME)

    if role:
        try:
            await member.add_roles(role)
            print(f'Added role to {member.name}')
        except discord.Forbidden:
            print(f'Failed to add role to {member.name}. Missing permissions.')
        except discord.HTTPException as e:
            print(f'HTTP exception occurred: {e}')




# Define role names with emojis
ROLE_NAMES = {
    "პირველ კურსელი": "1️⃣",
    "მეორე კურსელი": "2️⃣",
    "მესამე კურსელი": "3️⃣",
    "მეოთხე კურსელი": "4️⃣"
}


class EmojiRoleButton(Button):
    def __init__(self, emoji, role_name):
        super().__init__(emoji=emoji, style=discord.ButtonStyle.primary)
        self.role_name = role_name

    async def callback(self, interaction: discord.Interaction):
        try:
            role = discord.utils.get(interaction.guild.roles, name=self.role_name)
            if role is None:
                await interaction.response.send_message(f"Role '{self.role_name}' not found.", ephemeral=True)
                return

            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"'{self.role_name}'✅",
                                                    ephemeral=True)

        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to assign this role.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"Failed to assign role due to an HTTP exception: {e}",
                                                    ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An unexpected error occurred: {e}", ephemeral=True)
            print(f"Error in callback: {e}")  # Log unexpected errors to console

class RoleSelectionView(View):
    def __init__(self, timeout=180):
        super().__init__(timeout=timeout)
        # Add emoji buttons dynamically for each role
        for role_name, emoji in ROLE_NAMES.items():
            self.add_item(EmojiRoleButton(emoji, role_name))


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}.')
    channel = bot.get_channel(CHANNEL_ID)

    if channel is None:
        print(f"Channel with ID {CHANNEL_ID} not found.")
        return

    # Check if the message has already been sent
    async for message in channel.history(limit=100):
        if message.author == bot.user and message.embeds:
            embed = message.embeds[0]
            if embed.title == "👋 აირჩიე აკადემიური წელი":
                print(f"Role selection message already exists in channel {channel.name}.")
                # Update the view if needed
                if message.components:
                    await message.edit(view=RoleSelectionView())
                return

    # Upload the local image to Discord
    with open("headers/giusha.png", "rb") as img_file:
        image_message = await channel.send(file=discord.File(img_file, "giusha.png"))

    # Get the image URL
    image_url = image_message.attachments[0].url

    # Create the view and send the role selection message
    view = RoleSelectionView()
    embed = discord.Embed(
        title="👋 აირჩიე აკადემიური წელი",
        description=(
            "დააჭირე ქვემოთ ღილაკს რომელიც შეესაბამება შენს აკადემიურ წელს!\n\n"
        ),
        color=0x1383C3
    )
    embed.set_footer(text="TSU CS Roles")

    await channel.send(embed=embed, view=view)
    print(f"Role selection message sent to channel {channel.name}")


bot.run(TOKEN)
