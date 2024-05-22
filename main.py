# import libraries
import telebot
from currency_converter import CurrencyConverter
from telebot import types

# connecting to bot using it's token - !ENTER YOUR BOT TOKEN HERE!
bot = telebot.TeleBot('')
# currency object
currency = CurrencyConverter()
# amount of money which will be converted(default - 0)
amount = 0


# function-hanlder that processes start button
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello,Enter Sum:')
    bot.register_next_step_handler(message, sum)


# function that creates convertation Buttons after user entered amount of money
def sum(message):
    global amount
    # checking if user entered sum as int Type
    try:
        # saving amount of money which user entered into variable
        amount = int(message.text.strip())
    except ValueError:
        # if user entered amount in wrong format he will get message from bot
        bot.send_message(message.chat.id, 'Wrong Format, Enter sum')
        # register to restart this function as next step
        bot.register_next_step_handler(message, sum)
        return
    # checking is user entered positive amount of money(it can't be 0 or negative)
    if amount > 0:
        # creating inlineButtons for different convertations
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('else', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        # sending message to user to choose pair of currency to convert
        bot.send_message(
            message.chat.id, 'Choose pair of currency', reply_markup=markup)
    else:
        # if user doesn't enter positive number he will get message from bot
        bot.send_message(
            message.chat.id, 'Please, enter amount that is bigger that 0')
        bot.register_next_step_handler(message, sum)


# function that processes callback-data(function that calls after pressing on conversation button)
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    # if user doesn't choose else button
    if call.data != 'else':
        # saving two currencies in variable
        values = call.data.upper().split('/')
        # saving result of converting into variable
        res = currency.convert(amount, values[0], values[1])
        # sending converted sum to a user
        bot.send_message(call.message.chat.id, f'You will get {round(res, 2)} {
            values[1]}.You can write another sum: ')
        # register function that will make user to enter another sum if he wants
        bot.register_next_step_handler(call.message, sum)
    # if user wants to enter his own currencies
    else:
        # bot asks user to enter his own pair of currencies
        bot.send_message(call.message.chat.id,
                         'Enter pair of currencies to convert')
        # register next step function mycurrency after user entered his pair of currencies
        bot.register_next_step_handler(call.message, my_currency)


# function that converts user's pair of currencies
def my_currency(message):
    # checking is user entered pair of currencies corectly
    try:
        values = message.text.upper().split('/')
        # saving result of converting into variable
        res = currency.convert(amount, values[0], values[1])
        # sending converted sum to a user
        bot.send_message(message.chat.id, f'You will get {round(res, 2)} {
            values[1]}.You can write another sum: ')
        # register function that will make user to enter another sum if he wants
        bot.register_next_step_handler(message, sum)
    # if user entered pair of currencies incorrect
    except Exception:
        # he will get message from bot
        bot.send_message(
            message.chat.id, 'Something wrong.Please enter currency values again:')
        # restarting my_currency function as next step after user's message
        bot.register_next_step_handler(message, my_currency)


        # non stop mode for bot
bot.polling(non_stop=True)
