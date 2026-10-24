import discord
from discord.ext import commands

from config import TOKEN, DATABASE
from logic import DatabaseManager

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix='!', intents=intents,
    allowed_mentions=discord.AllowedMentions.none()
)
manager = DatabaseManager(DATABASE)

@bot.command()
async def start(ctx, *, name: str):
    """Contoh: !start Budi Santoso"""
    if manager.add_owner(ctx.author.id, name):
        await ctx.send('Registrasi berhasil! Coba !add Belajar Python.')
    else:
        await ctx.send('Kamu sudah terdaftar.')


@bot.command(name='list')
async def list_tasks(ctx):
    """Lihat ID, nama, dan status semua task milikmu."""
    tasks = manager.get_tasks(ctx.author.id)
    message = 'ID | Nama | Status\n'

    if len(tasks) == 0:
        await ctx.send('Task masih kosong, coba !add dulu')
        return

    for task_id, name, status in tasks:
        message += f'{task_id} | {name} | {status}\n'

    await ctx.send(message)


@bot.command()
async def add(ctx, *, name: str):
    """Contoh: !add Belajar Python"""
    name = name.strip()
    if manager.add_task(ctx.author.id, name):
        await ctx.send('Task ditambahkan dengan status todo')
    else:
        await ctx.send('Task gagal ditambahkan. Daftar dengan !register Nama Kamu.')


@bot.command()
async def update(ctx, task_id: int, *, status: str):
    """Contoh: !update 1 on progress"""
    status = status.strip().lower()
    if manager.update_task(ctx.author.id, task_id, status):
        await ctx.send('Status task berhasil diubah.')
    else:
        await ctx.send('Task tidak ditemukan dalam daftar milikmu. Periksa !list.')


@bot.command()
async def delete(ctx, task_id: int):
    """Contoh: !delete 1"""
    if manager.delete_task(ctx.author.id, task_id):
        await ctx.send('Task berhasil dihapus.')
    else:
        await ctx.send('Task tidak ditemukan dalam daftar milikmu. Periksa !list.')

if __name__ == '__main__':
    bot.run(TOKEN)
