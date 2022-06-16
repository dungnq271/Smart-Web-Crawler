import json
from json2html import *


def to_json(data, file_name):
    with open(file_name, "w") as outfile:
        json.dump(data, outfile, indent=4)


def to_html(json_file, html_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    out = json2html.convert(json=data)
    with open(html_file, "w", encoding="utf-8") as htmlfile:
        htmlfile.write(str(out))
        print("Json file is converted successfully...")
