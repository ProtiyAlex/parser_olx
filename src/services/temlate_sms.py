from services.telegram_sms import telegram_bot_sendtext

class TelegrammSms:
    def __init__(self,card):
        self.card=card
        self.template()
        pass
    def template(self):
        txt = f"✅ {self.card.img_link} \n" \
              f"💵 price: {self.card.price} \n" \


        telegram_bot_sendtext(txt)

        # txt = f"✅ {self.card.link} \n" \
        #       f"🧩 Strategy: {self.coin.strategy}\n" \
        #       f"📝 Side: {self.coin.side}\n" \
        #       f"🧮 Amount: {round(self.coin.qty_buy * self.coin.price_end, 2)} USDT, ({self.coin.qty_buy})\n" \
        #       f"📈 Price start: {self.coin.price_start_real} USDT\n" \
        #       f"📉 Price end: {self.coin.price_end} USDT\n" \
        #       f"💵 price: {self.card.price} \n" \
        #       f"💎 Profit: {round(self.coin.profit, 2)} USDT\n" \
        #       f"⏰ Time: {self.duration()}\n" \
        #       f"_________________________\n" \
        #       f"💵 Profit per day: {self.balans} USDT"

