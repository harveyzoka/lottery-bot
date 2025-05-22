import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Lưu dữ liệu người chơi đoán
user_guesses = {}

guess_range = (1, 100)  # Giới hạn số đoán


@bot.event
async def on_ready():
    print(f"🤖 Bot đã sẵn sàng: {bot.user}")


@bot.command()
async def guess(ctx, number: int):
    if ctx.author.id in user_guesses:
        await ctx.send(
            f"{ctx.author.mention} bạn đã đoán rồi: {user_guesses[ctx.author.id]}"
        )
        return

    if not (guess_range[0] <= number <= guess_range[1]):
        await ctx.send(
            f"{ctx.author.mention} số phải nằm trong khoảng {guess_range[0]} đến {guess_range[1]}."
        )
        return

    user_guesses[ctx.author.id] = number
    await ctx.send(f"{ctx.author.mention} đã chọn số {number}. Chúc may mắn! 🎉"
                   )


@bot.command()
@commands.has_permissions(administrator=True)
async def draw(ctx):
    if not user_guesses:
        await ctx.send("Chưa có ai đoán số.")
        return

    winning_number = random.randint(*guess_range)
    await ctx.send(f"🎯 Số trúng là: **{winning_number}**")

    closest_user = None
    closest_diff = None
    for uid, guess in user_guesses.items():
        diff = abs(guess - winning_number)
        if closest_diff is None or diff < closest_diff:
            closest_diff = diff
            closest_user = uid

    winner = await bot.fetch_user(closest_user)
    await ctx.send(
        f"🏆 Người đoán gần nhất: **{winner.name}** với số {user_guesses[closest_user]} (chênh lệch {closest_diff})"
    )


@bot.command()
@commands.has_permissions(administrator=True)
async def list_guesses(ctx):
    if not user_guesses:
        await ctx.send("Chưa có ai đoán số.")
        return

    lines = ["📋 Danh sách người đã đoán:"]
    for uid, number in user_guesses.items():
        user = await bot.fetch_user(uid)
        lines.append(f"• {user.name}: {number}")
    await ctx.send("\n".join(lines))


@bot.command()
@commands.has_permissions(administrator=True)
async def reset_guesses(ctx):
    user_guesses.clear()
    await ctx.send(
        "🔁 Đã bắt đầu vòng chơi mới. Mọi người có thể đoán lại từ đầu!")


# Thêm token bot của bạn ở đây
bot.run(os.getenv("DISCORD_TOKEN"))