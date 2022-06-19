"""Module with Telegram bot's logic and program's mainloop"""

import time
import string
import telebot
from telebot import types
from . import chess
from .chess import translate
from .localization import set_system_lang
from . import solver


TOKEN = "5505142382:AAEDArd2zRDlygMFYW_PJNWDsb75dZLYfNo"
bot = telebot.TeleBot(TOKEN, parse_mode=None)

current_games = {}
admins = [414173417]
stockfish_solver = solver.Solver()


def make_keyboard():
    """Generate virtual keyboard."""
    markup = types.InlineKeyboardMarkup()
    for number in range(8, 0, -1):
        keyboard_row = []
        for letter in list(string.ascii_lowercase)[:8]:
            keyboard_row.append(types.InlineKeyboardButton(
                f'{letter}{number}', callback_data=f'{letter}{number}'))
        markup.row(*keyboard_row)
    return markup


class Player:
    """
    Class to store game information.

    ...
    Attributes:
    ---------------
    move_start : str
        First picked key on keyboard
    move_to : str
        Second picked key on keyboard
    chess : chess.Chess
        Game logic
    prev_state : int
        state of a game, -1 - loss, 0 - wrong move, 1 - possible move
    """

    def __init__(self):
        """Initialise player state."""
        self.move_start = ''
        self.move_to = ''
        self.chess = chess.Chess()
        self.prev_state = 0

    def set_move_start(self, cell):
        """Check start move."""
        self.move_start = translate(cell)

    def set_move_to(self, cell):
        """Set next move."""
        self.move_to = translate(cell)

    def clear_accum(self):
        """Clear state between turns."""
        self.move_start = ''
        self.move_to = ''

    def has_piece_under(self, cell):
        """Detect piece for kb location."""
        start = translate(cell)
        return self.chess.has_piece_under(start)

    def has_prev_cell(self):
        """Check buffer."""
        return self.move_start != ''

    def check_move_valid(self):
        """Check move validity."""
        return self.chess.move(self.move_start, self.move_to)


@bot.message_handler(commands=['stop'])
def game_stop(message):
    """End game."""
    del current_games[message.chat.id]
    bot.send_message(message.chat.id, _('Покеда'))


@bot.message_handler(commands=['start'])
def game_start(message):
    """Initialise game."""
    current_games[message.chat.id] = Player()
    img = open("chessbot/Current_game/initial_board.png", 'rb')
    bot.send_photo(message.chat.id, photo=img,
                   caption=_('Сделай свой ход'), reply_markup=make_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    """Mainloop. Take turn from player and solver."""
    move = call.data
    chat_id = call.message.chat.id
    if current_games[chat_id].has_prev_cell():
        current_games[chat_id].set_move_to(move)
        move_check = current_games[chat_id].check_move_valid()
        print(move_check)
        if move_check == 1:
            # обрабатывать ход
            current_games[chat_id].clear_accum()
            img = open("chessbot/Current_game/board.png", 'rb')
            bot.edit_message_media(
                chat_id=call.message.chat.id,
                media=types.InputMediaPhoto(media=img),
                message_id=call.message.message_id,
                reply_markup=make_keyboard()
            )
            bot.edit_message_caption(
                chat_id=call.message.chat.id,
                caption=_("Ход робота"),
                message_id=call.message.message_id,
                reply_markup=make_keyboard()
            )
            time.sleep(5) # to give player time to
            #print(current_games[chat_id].chess.fen)
            move = stockfish_solver.make_step(current_games[chat_id].chess.fen)
            if move is None:
                bot.edit_message_caption(
                    chat_id=call.message.chat.id,
                    caption=_("Победа!!!!!!"),
                    message_id=call.message.message_id
                )
            else:
                current_games[chat_id].set_move_start(move[0:2])
                current_games[chat_id].set_move_to(move[2:4])

                bot_move_check = current_games[chat_id].check_move_valid()
                if bot_move_check == 1:
                    current_games[chat_id].clear_accum()
                    img = open("chessbot/Current_game/board.png", 'rb')
                    bot.edit_message_media(
                        chat_id=call.message.chat.id,
                        media=types.InputMediaPhoto(media=img),
                        message_id=call.message.message_id,
                        reply_markup=make_keyboard()
                    )
                    bot.edit_message_caption(
                        chat_id=call.message.chat.id,
                        caption=_("Сделай следующий ход"),
                        message_id=call.message.message_id,
                        reply_markup=make_keyboard()
                    )
                    current_games[chat_id].prev_state = 0
                elif bot_move_check == 0:
                    bot.edit_message_caption(
                        chat_id=call.message.chat.id,
                        caption=_("Победа!!!!!!"),
                        message_id=call.message.message_id
                    )
                else:
                    bot.edit_message_caption(
                        chat_id=call.message.chat.id,
                        caption=_("Поражение((("),
                        message_id=call.message.message_id
                    )
                    current_games[chat_id].clear_accum()
        elif move_check == 0:
            if current_games[chat_id].prev_state != 1:
                bot.edit_message_caption(
                    chat_id=call.message.chat.id,
                    caption=_("Невозможный ход"),
                    message_id=call.message.message_id,
                    reply_markup=make_keyboard()
                )
            current_games[chat_id].prev_state = 1
            current_games[chat_id].clear_accum()
        else:
            bot.edit_message_caption(
                chat_id=call.message.chat.id,
                caption=_("Победа!!!!!!"),
                message_id=call.message.message_id
            )
            current_games[chat_id].clear_accum()
    else:
        if current_games[chat_id].has_piece_under(move):
            bot.edit_message_caption(
                chat_id=call.message.chat.id,
                caption=_("Выберите ход для фигуры с поля ") + f"{move}",
                message_id=call.message.message_id,
                reply_markup=make_keyboard()
            )
            current_games[chat_id].prev_state = 0
            current_games[chat_id].set_move_start(move)
        else:
            if current_games[chat_id].prev_state != 2:
                bot.edit_message_caption(
                    chat_id=call.message.chat.id,
                    caption=_("Фигура не выбрана"),
                    message_id=call.message.message_id,
                    reply_markup=make_keyboard()
                )
            current_games[chat_id].prev_state = 2
            current_games[chat_id].clear_accum()


@bot.message_handler(commands=['kill'])
def delete_table(message):
    """Kills current game."""
    if message.from_user.id not in admins:
        bot.send_message(message.chat.id, _('Нет доступа: возобновление работы.'))
        return
    print(_('Остановка работы приложения.'))
    bot.stop_polling()
    exit()


if __name__ == '__main__':
    set_system_lang()
    print(_('Запуск приложения.'))
    bot.polling()
