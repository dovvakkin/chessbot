import telebot
from telebot import types
import string
from . import chess
from .chess import translate
from requests import post
from .localization import set_system_lang
from . import solver
import time

TOKEN = "5505142382:AAEDArd2zRDlygMFYW_PJNWDsb75dZLYfNo"
bot = telebot.TeleBot(TOKEN, parse_mode=None)

current_games = {}
admins = [414173417]
stockfish_solver = solver.Solver()


def make_keyboard():
    markup = types.InlineKeyboardMarkup()
    for number in range(8, 0, -1):
        keyboard_row = []
        for letter in list(string.ascii_lowercase)[:8]:
            keyboard_row.append(types.InlineKeyboardButton(
                f'{letter}{number}', callback_data=f'{letter}{number}'))
        markup.row(*keyboard_row)
    return markup


class Player:
    def __init__(self):
        self.board = []
        self.move_start = ''
        self.move_to = ''
        self.chess = chess.Chess()
        self.prev_state = 0

    def set_move_start(self, cell):
        self.move_start = translate(cell)

    def set_move_to(self, cell):
        self.move_to = translate(cell)

    def clear_accum(self):
        self.move_start = ''
        self.move_to = ''

    def has_piece_under(self, cell):
        start = translate(cell)
        return self.chess.has_piece_under(start)

    def has_prev_cell(self):
        return self.move_start != ''

    def check_move_valid(self):
        return self.chess.move(self.move_start, self.move_to)


@bot.message_handler(commands=['stop'])
def game_start(message):
    del current_games[message.chat.id]
    bot.send_message(message.chat.id, _('Покеда'))


@bot.message_handler(commands=['start'])
def game_start(message):
    current_games[message.chat.id] = Player()
    #chessboard_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/AAA_SVG_Chessboard_and_chess_pieces_02.svg/1024px-AAA_SVG_Chessboard_and_chess_pieces_02.svg.png?20200505220000"
    #bot.send_photo(message.chat.id, photo=chessboard_url, caption='Сделай свой ход', reply_markup=make_keyboard())
    img = open("chessbot/Current_game/initial_board.png", 'rb')
    bot.send_photo(message.chat.id, photo=img,
                   caption=_('Сделай свой ход'), reply_markup=make_keyboard())
    #bot.send_message(message.chat.id, 'Сделай свой ход', reply_markup=make_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    move = call.data
    chat_id = call.message.chat.id
    if current_games[chat_id].has_prev_cell():
        current_games[chat_id].set_move_to(move)
        if current_games[chat_id].check_move_valid():
            # обрабатывать ход
            current_games[chat_id].clear_accum()
            #url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/AAA_SVG_Chessboard_and_chess_pieces_02.svg/1024px-AAA_SVG_Chessboard_and_chess_pieces_02.svg.png?20200505220000"
            img = open("chessbot/Current_game/board.png", 'rb')
            #print(current_games[chat_id].chess.board.board_array)
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
            
            time.sleep(5)
            print(current_games[chat_id].chess.fen)
            move = stockfish_solver.make_step(current_games[chat_id].chess.fen)
            current_games[chat_id].set_move_start(move[0:2])
            current_games[chat_id].set_move_to(move[2:4])

            if current_games[chat_id].check_move_valid():
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
            else:
                print("KEK")
        else:
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
        if current_games[chat_id].has_piece_under(move):
            bot.edit_message_caption(
                chat_id=call.message.chat.id,
                caption=_("Куда поставить фигуру с ") + f"{move}",
                message_id=call.message.message_id,
                reply_markup=make_keyboard()
            )
            current_games[chat_id].prev_state = 0
            current_games[chat_id].set_move_start(move)
        else:
            if current_games[chat_id].prev_state != 2:
                bot.edit_message_caption(
                    chat_id=call.message.chat.id,
                    caption=_("Фигуры не выбрано"),
                    message_id=call.message.message_id,
                    reply_markup=make_keyboard()
                )
            current_games[chat_id].prev_state = 2
            current_games[chat_id].clear_accum()


@bot.message_handler(commands=['kill'])
def create_new_table(message):
    if message.from_user.id not in admins:
        bot.send_message(message.chat.id, _('Не убiй!'))
        return
    print(_('Ня пока(('))
    bot.stop_polling()
    exit()


if __name__ == '__main__':
    set_system_lang()
    print(_('Поехали!'))
    bot.polling()
