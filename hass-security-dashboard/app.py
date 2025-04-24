from flask import Flask, render_template, request
import os, json

app = Flask(__name__, static_folder='web/static', template_folder='web/templates')

CONFIG = {
    'port': int(os.getenv('PORT', 8099)),
    'lang': os.getenv('LANG', 'en')
}

@app.route('/')
def index():
    lang = CONFIG['lang']
    with open(f'data/translations/{lang}.json', 'r') as f:
        labels = json.load(f)
    return render_template('index.html', labels=labels)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=CONFIG['port'])