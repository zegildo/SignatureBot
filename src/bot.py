#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to generate automatic e-mail signatures.

import logging

from telegram import (ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from conf.settings import (MODE, HEROKU_APP_NAME, PORT, TELEGRAM_TOKEN, PASSWORD)

from conf.messages_pt import (MSG_START, MSG_ORGAO, MSG_ORGAO_NOK, MSG_SENHA,
                              MSG_SENHA_NOK, MSG_TITULO, MSG_CARGO, MSG_DDD,
                              MSG_TEL, MSG_LOG)

import signature_builder as sb

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

ORGAO, SENHA, TITULO, CARGO, DDD, TELEFONE, LOGIN, IMAGEM = range(8) 
EMAIL_SIGNATURE_PARAMS = {}

def start(update, context):
    """
    """
    reply_keyboard = [['CADE', 'UFERSA']]
    update.message.reply_text(MSG_START,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard,
        resize_keyboard=True))

    return ORGAO

def orgao(update, context):
    """
    """
    user = update.message.from_user
    orgao = update.message.text
    logger.info("User %s: %s", user.first_name, update.message.text)

    orgao = orgao.upper()
    if orgao in ['UFERSA', 'CADE']:
        EMAIL_SIGNATURE_PARAMS['ORGAO'] = update.message.text
        update.message.reply_text(MSG_ORGAO, 
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.MARKDOWN_V2)
        return SENHA
    else:
        update.message.reply_text(MSG_ORGAO_NOK, 
            reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    
def senha(update, context):
    """
    """
    user = update.message.from_user
    senha = update.message.text
                       
    if senha != PASSWORD:
        update.message.reply_text(MSG_SENHA_NOK)
        return ConversationHandler.END
    else:
        update.message.reply_text(MSG_SENHA, 
            parse_mode=ParseMode.MARKDOWN_V2)
    
    logger.info("User %s: senha: %s", user.first_name, update.message.text)

    return TITULO

def titulo(update, context):
    """
    """
    user = update.message.from_user
    EMAIL_SIGNATURE_PARAMS['NOME'] = update.message.text
    logger.info("User %s: %s", user.first_name, update.message.text)
    
    reply_keyboard = [['BSc.', 'Esp.', 'MBA.', 'MsC.','Ph.D.']]
    update.message.reply_text(MSG_TITULO,
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, 
            resize_keyboard=True))

    return CARGO

def cargo(update, context):
    """
    """
    user = update.message.from_user
    logger.info("User %s: %s", user.first_name, update.message.text)
    EMAIL_SIGNATURE_PARAMS['TITULO'] = update.message.text

    update.message.reply_text(MSG_CARGO, 
        reply_markup=ReplyKeyboardRemove())

    return DDD

def DDD(update, context):
    """
    """
    user = update.message.from_user
    logger.info("User %s: %s", user.first_name, update.message.text)
    EMAIL_SIGNATURE_PARAMS['CARGO'] = update.message.text

    update.message.reply_text(MSG_DDD, parse_mode=ParseMode.MARKDOWN_V2)

    return TELEFONE

def telefone(update, context):
    """
    """
    user = update.message.from_user
    EMAIL_SIGNATURE_PARAMS['DDD'] = update.message.text

    logger.info("User %s: %s", user.first_name, update.message.text)
    update.message.reply_text(MSG_TEL, parse_mode=ParseMode.MARKDOWN_V2)
    
    return LOGIN

def login(update, context):
    """
    """
    user = update.message.from_user
    EMAIL_SIGNATURE_PARAMS['TELEFONE'] = update.message.text
    logger.info("User %s: %s", user.first_name, update.message.text)
    update.message.reply_text(MSG_LOG,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.MARKDOWN_V2)

    return IMAGEM

def imagem(update, context):
    """
    """
    user = update.message.from_user
    EMAIL_SIGNATURE_PARAMS['LOGIN'] = update.message.text
    logger.info("User %s: %s", user.first_name, update.message.text)

    img = sb.create(EMAIL_SIGNATURE_PARAMS)
    context.bot.send_photo(user.id, photo=img)

    return ConversationHandler.END


def cancel(update, context):
    """
    """
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Este serviço não existe!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def error(update, context):
    """
    """
    logger.warning('Update "%s" erro "%s"', update, context.error)


def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],

        states = {
            ORGAO: [MessageHandler(Filters.text, orgao)],
            SENHA: [MessageHandler(Filters.text, senha)],
            TITULO: [MessageHandler(Filters.text, titulo)],
            CARGO: [MessageHandler(Filters.text, cargo)],
            DDD: [MessageHandler(Filters.text, DDD)],
            TELEFONE: [MessageHandler(Filters.text, telefone)],
            LOGIN: [MessageHandler(Filters.text, login)],
            IMAGEM: [MessageHandler(Filters.text, imagem)]
        },

        fallbacks = [CommandHandler('cancel', cancel)]
    )

    

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    if(MODE == "PROD"):
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TELEGRAM_TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TELEGRAM_TOKEN))
        
    elif(MODE == "DEV"):
        updater.start_polling()
        logger.warning('MODE:DEV - start_polling - OK')

    else:
        logger.error("No MODE specified!")
        sys.exit(1)

    updater.idle()

if __name__ == '__main__':
    main()