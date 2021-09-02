## SCRIPT PARA GESTIONAR UN BOT PARA CALENDARIO DE EVENTOS Y RECORDATORIOS

from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
import Token
import datetime
import logging

token = Token.token

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
    )
logger = logging.getLogger()

print('Token:', token)
print('Bot iniciado...')

def start(update: Update, context: CallbackContext) -> None:    # devuelve None

    """ Método para contestar cuando el usuario escriba el comando /start """

    # info del usuario y del chat
    user_id = update.message.from_user.id
    print('user ID:', user_id)
    user_name = update.message.from_user.username
    print('user name:', user_name)
    first_name = update.message.from_user.first_name
    print('first_name:', first_name)
    chat_id = update.message.chat_id
    print('chat ID:', chat_id)

    update.message.reply_text(
        text=f'¡Hola, <b>{user_name}!</b>\n\n'
             f'Puedes escribir los siguientes comandos:\n\n'
             f'<i>/comando1</i> para acción 1\n'
             f'<i>/comando2</i> para acción 2\n'
             f'<i>/comando3</i> para acción 3\n\n'
             f'¡Un saludo!',
        parse_mode='HTML'
    )

def daily_docs(update: Update, context: CallbackContext) -> None:

    """ Método callback del jobqueue para enviar los documentos diarios """

    logger.info('Callback de los docs diarios')

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Aquí están los documentos diarios'
    )

def daily(update: Update, context: CallbackContext) -> None:

    """ Método para implementar jobqueues para eventos diarios """

    logger.info('Comando daily recibido')

    week_days = (0, 1, 2, 3, 4)     # de lunes a viernes
    post_time = datetime.time(
        hour=9,
        minute=00
    )                               # hora del día a la que se postearán los documentos diarios

    # Diariamente se ejecutará la función daily_schedule para enviar los documentos diarios
    context.job_queue.run_daily(
        callback=daily_docs,
        time=post_time,
        days=week_days
    )

    update.message.reply_text(text=f'Hola, te voy a enviar un reminder cada {context.args[0]} segundos')

def error(update: Update, context: CallbackContext) -> None:

    """ Método de error """

    print(f'Update {update} caused error {context.error}')

def main ():

    updater = Updater(token)
    print('updater creado')
    dp = updater.dispatcher
    print('dispatcher creado')

    # handler de comando para repetir un recordatorio
    dp.add_handler(CommandHandler(
            command='daily',
            callback=daily
        ))

    # handler de error

    dp.add_error_handler(error)

    updater.start_polling(5)    # listo para escuchar cada 5 segundos
    updater.idle()              # el bot se queda escuchando

main()