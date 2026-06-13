import os, threading, websocket, telebot, time
from flask import Flask

app = Flask(__name__)
TOKEN = os.getenv('TOKEN')
BOT = telebot.TeleBot(os.getenv('BOT_TOKEN'))
CHAT_ID = os.getenv('CHAT_ID')

@app.route('/')
def home(): return "البوت يعمل!"

def run_bot():
    while True:
        try:
            ws = websocket.WebSocketApp("wss://ws2.qxbroker.com/socket.io/?EIO=3&transport=websocket",
                on_open=lambda ws: ws.send(f'42["auth",{{"token":"{TOKEN}"}}]'),
                on_message=lambda ws, msg: BOT.send_message(CHAT_ID, f"إشارة: {msg}") if "candles" in msg else None)
            ws.run_forever()
        except: time.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
