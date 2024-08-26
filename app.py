from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<beach>')
def beach(beach):
    return render_template('beach.html', beach=beach.capitalize())

if __name__ == '__main__':
    app.run(debug=True)
