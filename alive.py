from threading import Thread

from flask import Flask

app = Flask('')

@app.route('/')
def main():
    return 'Bot is online!'

def run():
    app.run(host="0.0.0.0", port=8080)

def alive():
    server = Thread(target=run)
    server.start()