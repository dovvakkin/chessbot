import telebot
from telebot import types
import string

TOKEN = ""
bot = telebot.TeleBot(TOKEN, parse_mode=None)

current_games = {}
admins = [414173417]


def make_keyboard():
    markup = types.InlineKeyboardMarkup()
    for number in range(8,0,-1):
        keyboard_row = []
        for letter in list(string.ascii_lowercase)[:8]:
            keyboard_row.append(types.InlineKeyboardButton(f'{letter}{number}', callback_data=f'{letter}{number}'))
        markup.row(*keyboard_row)
    return markup


class GameBoard:
    def __init__(self):
        self.board = []
        self.move_acc = ''

    def accumulate_move(self, cell):
        self.move_acc += cell

    def clear_accum(self):
        self.move_acc = ''

    def has_piece_under(self, cell):
        return True

    def has_prev_cell(self):
        return len(self.move_acc) == 2

    def check_move_valid(self):
        return True

    def apply_move(move):
        pass


@bot.message_handler(commands=['stop'])
def game_start(message):
    del current_games[message.chat.id]
    bot.send_message(message.chat.id, 'Покеда')


@bot.message_handler(commands=['start'])
def game_start(message):
    current_games[message.chat.id] = GameBoard()
    chessboard_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/AAA_SVG_Chessboard_and_chess_pieces_02.svg/1024px-AAA_SVG_Chessboard_and_chess_pieces_02.svg.png?20200505220000"
    bot.send_photo(message.chat.id, photo=chessboard_url, caption='Сделай свой ход', reply_markup=make_keyboard())
    #bot.send_message(message.chat.id, 'Сделай свой ход', reply_markup=make_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    move = call.data
    chat_id = call.message.chat.id
    if current_games[chat_id].has_prev_cell():
        current_games[chat_id].accumulate_move(move)
        if current_games[chat_id].check_move_valid():
            # обрабатывать ход
            current_games[chat_id].clear_accum()
            url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/AAA_SVG_Chessboard_and_chess_pieces_02.svg/1024px-AAA_SVG_Chessboard_and_chess_pieces_02.svg.png?20200505220000"
            bot.edit_message_media(
                chat_id=call.message.chat.id,
                media=types.InputMediaPhoto(media=url),
                message_id=call.message.message_id,
                reply_markup=make_keyboard()
            )
            bot.edit_message_caption(
                chat_id=call.message.chat.id,
                caption=f"Сделай следующий ход",
                message_id=call.message.message_id,
                reply_markup=make_keyboard()
            )
        else:
            bot.edit_message_caption(
                chat_id=call.message.chat.id,
                caption="Невозможный ход",
                message_id=call.message.message_id,
                reply_markup=make_keyboard()
            )
            current_games[chat_id].clear_accum()
    else:
        if current_games[chat_id].has_piece_under(move):
            bot.edit_message_caption(
                chat_id=call.message.chat.id,
                caption=f"Куда поставить фигуру с {move}",
                message_id=call.message.message_id,
                reply_markup=make_keyboard()
            )
            current_games[chat_id].accumulate_move(move)
        else:
            bot.edit_message_caption(
                chat_id=call.message.chat.id,
                caption=f"Фигуры не выбрано",
                message_id=call.message.message_id,
                reply_markup=make_keyboard()
            )
            current_games[chat_id].clear_accum()



@bot.message_handler(commands=['kill'])
def create_new_table(message):
    if message.from_user.id not in admins:
        bot.send_message(message.chat.id, 'Не убий!')
        return
    print('Ня пока((')
    bot.stop_polling()
    exit()


if __name__ == '__main__':
    print('Поехали!')
    bot.polling() 