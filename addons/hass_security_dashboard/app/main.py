from flask import Flask, render_template_string, request
import os
import json

app = Flask(__name__, static_folder='web', static_url_path='')

LANG = {
    "en": json.load(open('web/lang/en.json')),
    "nl": json.load(open('web/lang/nl.json'))
}

@app.route('/')
def index():
    lang = os.getenv("LANGUAGE", "en")
    strings = LANG.get(lang, LANG["en"])
    with open('web/index.html', encoding='utf-8') as f:
        template = f.read()
    for key, val in strings.items():
        template = template.replace(f"{{{{ {key} }}}}", val)
    return render_template_string(template)