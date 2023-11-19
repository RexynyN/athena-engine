from actions import summarize, tooltip
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/')
def index ():
    return jsonify({ "data": "Poggggers" })

@app.route('/tooltip', methods=["POST"])
def tooltip_text():
    content = request.json
    tooltips = tooltip.classify_from_text(content["data"])

    return jsonify({ "data": tooltips })


@app.route('/tooltip/list', methods=["POST"])
def tooltip_concepts():
    content = request.json
    tooltips = tooltip.classify_from_concept(content["data"])

    return jsonify({ "data": tooltips})


@app.route("/summarize/", methods=["POST"])
def poppers():
    data = request.json
    summ = summarize.summarize_text(data.get("data"))
    print(summ)

    return jsonify({ "data": summ })

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
