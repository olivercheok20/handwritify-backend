from flask import Flask, request
from flask_cors import CORS, cross_origin
import unidecode
import json

from demo import Hand

app = Flask(__name__)
cors = CORS(app)

@app.route("/", methods=['POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
def hello_world():
    jsonResponse = json.loads(request.data.decode('utf-8'))

    lines = jsonResponse["lines"]

    processed_lines = []

    # all_chars = ''

    for line in lines:
        line = line.replace("&", "and")
        line = line.replace("$", "S")
        line = line.replace("*", "")
        line = line.replace("Q", "q")
        line = line.replace("X", "x")
        line = line.replace("Z", "z")
        processed_lines.append(unidecode.unidecode(line))
        # if len(line) > 70:
        #     print(line)
        # for char in line:
        #     if char not in all_chars:
        #         all_chars += char

    lines = processed_lines
    # print(all_chars)

    for line in lines:
        for char in line:
            if char not in "\u0000 !\"#'(),-.0123456789:;?ABCDEFGHIJKLMNOPRSTUVWYabcdefghijklmnopqrstuvwxyz":
                print(char)


    biases = [float(jsonResponse["bias"]) for i in lines]
    styles = [9 for i in lines]
    stroke_colors = [jsonResponse["font_color"] for i in lines]
    stroke_widths = [float(jsonResponse["width"]) for i in lines]

    filename = 'dummy.svg'

    hand = Hand()

    return hand.write(
        filename=filename,
        lines=lines,
        biases=biases,
        styles=styles,
        stroke_colors=stroke_colors,
        stroke_widths=stroke_widths,
        bg_color=jsonResponse["bg_color"]
    )

if __name__ == "__main__":
    app.run()