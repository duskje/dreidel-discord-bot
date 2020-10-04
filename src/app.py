from discord.ext import commands
from game import DreidelLogic
import os

from exceptions import (
    InsufficientFundsException,

    AlreadyInGameException,
    NoGameInProgressException,

    NoPlayersException,
    NotPlayersTurnException,
    PlayerNotFoundException,
)

bot = commands.Bot(
    command_prefix='!',
)

dreidel_game = DreidelLogic()


@bot.event
async def on_ready():
    print('Ready to roll!')


@bot.command(aliases=['nr'])
async def new_round(ctx):
    if dreidel_game.is_round_active:
        await ctx.send(f'There is a round already in progress.')
    else:
        await ctx.send(f'Shuffling...')
        dreidel_game.new_round()

        await ctx.send(f'It\'s { dreidel_game.ask_turn() }\'s turn to roll.')


@bot.command(aliases=['r', 'roll_dreidel'])
async def roll(ctx):
    try:
        result = dreidel_game.roll(ctx.author)

        if result == 'nun':
            await ctx.send(f'{result}. You get nothing!')
        elif result == 'gimel':
            await ctx.send(f'{result}. You get eveything in the pot!')
        elif result == 'hei':
            await ctx.send(f'{result}. You get half!')
        elif result == 'shin':
            await ctx.send(f'{result}. You must put one on the pot!')

    except NotPlayersTurnException:
        await ctx.send(f'{ ctx.author }, it\'s not your turn!')
    except NoGameInProgressException:
        await ctx.send('There\'s no game in progress.')


@bot.command(aliases=['jg'])
async def join_game(ctx):
    try:
        dreidel_game.join(ctx.author)
        await ctx.send(f'You\'re in!')
    except AlreadyInGameException:
        await ctx.send(f'{ctx.author}, you\'re already in the game!')


@bot.command(aliases=['lg'])
async def leave_game(ctx):
    try:
        dreidel_game.leave(ctx.author)

        await ctx.send(f'{ctx.author} is not playing anymore.')
    except PlayerNotFoundException:
        await ctx.send(f'You\'re not in the game!')


@bot.command(aliases=['wt'])
async def whose_turn(ctx):
    try:
        await ctx.send(f'It\'s { dreidel_game.ask_turn() }\'s turn.')
    except NoPlayersException:
        await ctx.send(f'No players in queue.')


@bot.command(aliases=['p'])
async def put(ctx, n: int):
    try:
        dreidel_game.put(ctx.author, n)
    except InsufficientFundsException:
        await ctx.send(f'Insufficient funds.')


@bot.command()
async def debug_logic(ctx):
    await ctx.send(
        'Pot: {pot}\n'
        'In queue: {round}\n'
        'Playing: {active_players}'.format(**dreidel_game.__dict__)
    )


@bot.command()
async def debug_user(ctx):
    for player in dreidel_game.active_players:
        await ctx.send(
            'User Object: {user_obj}\n'
            'Session Score: {session_score}\n'
            'User Wallet: {bank}'.format(**player.__dict__)
        )


def main() -> None:
    """
        Your key goes here
    """
    bot.run(os.environ['BOT_TOKEN'])


if __name__ == '__main__':
    main()