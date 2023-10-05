from threading import Thread

from flask import Flask
import markdown
import markdown.extensions.fenced_code

app = Flask('')

@app.route('/')
def main():
    readme_file = open("Documentation.md", "r")
    md_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )
    return md_string #'Bot is online!'

def run():
    app.run(host="0.0.0.0", port=8080)

def alive():
    server = Thread(target=run)
    server.start()