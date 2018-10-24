from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/another')
def another():
    return render_template('another.html')

if __name__ == "__main__":
    app.debug = True
    app.run()