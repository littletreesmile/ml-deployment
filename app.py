
from flask import Flask, render_template, request
# from transformers import MarianMTModel, MarianTokenizer

app = Flask(__name__)

def translate(input_text):
    # model_name = "Helsinki-NLP/opus-mt-zh-en"
    # tokenizer = MarianTokenizer.from_pretrained(model_name)
    # model = MarianMTModel.from_pretrained(model_name)
    # translated = model.generate(**tokenizer(input_text, return_tensors="pt", padding=True))
    # res = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
    return input_text + "  -- xiaofat_LN"


@app.route("/", methods=["GET", "POST"])
def index():
    translated_text = ""
    input_text = ""
    if request.method == "POST":
        input_text = request.form["text"]
        translated_text = translate(input_text)
    return render_template("index.html", input_text=input_text, translated_text=translated_text)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)  # for deployment
    # app.run(debug=False, port=8080)  # for local run