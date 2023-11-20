import requests


def telegram_bot_sendtext(bot_message):
    bot_token = '5210398447:AAFLSNGn5g-J2UcrkpX9Mx2nOtezEi7lRF8'
    bot_chatID = '-780418515'   #  real otskok '-780418515'
    # -601020332 krip
    #  real otskok '-780418515'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=html&text=' + bot_message
    response = requests.get(send_text)
    return response.json()