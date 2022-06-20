## Постановка задачи

### Телеграмм-бот, с которым можно сыграть в шахматы. 

## Фичи:

- User Interface, реализованный через Telegramm-бота <br>
- Вывод текущего состояния шахматной доски <br>
- Соперник в виде искуственного интеллекта <br>

## Список сторонних модулей:

- PIL для работы с изображением <br>
- numpy для работы с модулем PIL <br>
- pytelegramAPI, telebot для генерации UI и запуска бота в Telegram <br>
- stockfish для обертки над Stockfish Engine <br>

## Макет интерфейса, описание элементов:
- Изображение отображающее текущее состояние доски
- Строка подсказывающая игроку что ему нужно сделать (совершить свой ход или ожидать ход соперника)
- Ввод команд используя клавиатуру

![макет игры](images/prototype.png)

# Пользовательская документация

## Хостинг бота
- Бот может быть запущен только единожды в одной машине
- Для запуска модуля `python -m chessbot`
- Тесты отрабатывают при запуске `pytest` из корня

## Взаимодействие с ботом
- Необходимо написать боту с ником `@PD22_chessbot`
- Для старта игры нужно отправить ему `/start`
- Игра закончится при победе\поражении или по команде `/stop`
- Завершить исполнение бота можно с помощью `/kill`

![вид игры](images/game.png)

