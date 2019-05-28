# -*- coding: utf-8 -*-
"""
Created on Tue May 28 01:04:09 2019

@author: Pablo Carrera Flórez de Quiñones y José Llanes Jurado

En este script desarrollamos un chatbot en Telegram.
"""

#############
# Librerias #
#############

# Telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, RegexHandler

# Others
import logging
import config





###############
# Preparación #
###############

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)





#######################
# Sección de registro #
#######################

NOMBRE, APELLIDOS, FOTO, AFICIONES = range(4)

def start(bot, update):
    update.message.reply_text(
         "¡Hola soy Helper, el bot ayudante! "
         "Si en cualquier momento quieres dejar de hablar conmigo escribe /salir \n \n"
         "Por cierto, veo que no estás registrado en nuestra aplicación, "
         "eso hay que arreglarlo, ¿cómo te llamas?"
         )
    return NOMBRE

def nombre(bot, update):
    user = update.message.from_user
    logger.info("Nombre de %s: %s", user.first_name, update.message.text)
    update.message.reply_text("¡Bonito nombre!, ¿y tus apellidos?")
    return APELLIDOS

def apellidos(bot, update):
    user = update.message.from_user
    logger.info("Apellidos de %s: %s", user.first_name, update.message.text)
    update.message.reply_text("Tampoco están nada mal. ¿Me puedes enseñar una foto tuya?")
    return FOTO
    
def foto(bot, update):
    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download('user_photo.jpg')
    logger.info("Foto de %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text("Guau, ¡sales genial!, ¿Y que haces en tu tiempo libre?")
    return AFICIONES

def aficiones(bot, update):
    user = update.message.from_user
    logger.info("Aficiones de %s: %s", user.first_name, update.message.text)
    update.message.reply_text("¡Que vida más interesante!")
    update.message.reply_text("¡Ya estas registrado y puedes acceder a nuestro /menu "
                              "para disfrutar de todas nuestras funcionalidades!")
    return MENU



    
    
###################
# Sección de menú #
###################
    
MENU, ELEGIR, PEDIR, CONCEDER, AYUDA, SALIR = range(4,10)
    
def menu(bot, update):
    user = update.message.from_user
    reply_keyboard = [["Pedir favor", "Conceder favor", "Ayuda", "/salir"]]
    update.message.reply_text(
         "¡Ahora ya puedes usar la aplicación! \n \n"
         "¿Que quieres hacer?",
         reply_markup = ReplyKeyboardMarkup(reply_keyboard, 
                                            one_time_keyboard = True,
                                            resize_keyboard = True)
         )
    logger.info("%s ha entrado en el %s", user.first_name, update.message.text)
         
    return ELEGIR

def elegir(bot, update):
    user = update.message.from_user
    logger.info("%s ha elegido %s", user.first_name, update.message.text)
    if update.message.text == "Pedir favor" :
        update.message.reply_text("¿Qué necesitas?")
        return PEDIR
    if update.message.text == "Conceder favor" : 
        return CONCEDER
    if update.message.text == "Ayuda" : 
        update.message.reply_text("¿Qué problema tienes?")
        return AYUDA
    if update.message.text == "Salir" : 
        return SALIR
    
def pedir(bot, update):
    user = update.message.from_user
    logger.info("%s ha pedido %s.", user.first_name, update.message.text)
    update.message.reply_text("Buena idea, vamos a volver al /menu mientras esperamos")
    return MENU

def conceder(bot, update):
    user = update.message.from_user
    logger.info("Denegado a %s: %s.", user.first_name, "Conceder favor")
    update.message.reply_text("No hay tareas pendientes ahora, ¡Que suerte!")
    update.message.reply_text("Mejor volvemos al /menu.")
    return MENU

def ayuda(bot, update):
    user = update.message.from_user
    logger.info("%s ha pedido %s.", user.first_name, update.message.text)
    update.message.reply_text("Aún estamos desarrollando esta opción, ¡mientras "
                              "tanto puedes visitar nuestra página web!")
    update.message.reply_text("Mejor volvemos al /menu.")
    return MENU




####################
# Sección de otros #
####################

def salir(bot, update):
    user = update.message.from_user
    logger.info("%s ha salido de la conversación.", user.first_name)
    update.message.reply_text("Adiós, ¡espero que podamos hablar en otra ocasión!",
                              reply_markup = ReplyKeyboardRemove()
                              )
    return ConversationHandler.END


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)





##################
# Implementación #
##################

        
def main():
    # Cremos las instancias necesarias
    updater = Updater(token = config.TOKEN)
    dispatcher = updater.dispatcher

    # Sección de conversación para realizar el registro
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],

        states = {
            # Sección de conversación para realizar el registro
            NOMBRE:     [MessageHandler(Filters.text, nombre)],
            APELLIDOS:  [MessageHandler(Filters.text, apellidos)],
            FOTO:       [MessageHandler(Filters.photo, foto)],
            AFICIONES:  [MessageHandler(Filters.text, aficiones)],

            # Sección de conversación para realizar el registro
            MENU:     [CommandHandler("menu", menu)],
            ELEGIR:   [RegexHandler("^(Pedir favor|Conceder favor|Ayuda|Salir)", elegir)],
            PEDIR:    [MessageHandler(Filters.text, pedir)],
            CONCEDER: [MessageHandler(Filters.text, conceder)],
            AYUDA:    [MessageHandler(Filters.text, ayuda)]
        },

        fallbacks=[CommandHandler('salir', salir)]
    )
    
    dispatcher.add_handler(conv_handler)

    # Muestra los errores
    dispatcher.add_error_handler(error)

    # Iniciar el bot
    updater.start_polling()

    # Mantener el bot hasta pulsar Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()