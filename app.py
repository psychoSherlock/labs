from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/profile')
def profile():
    username = request.args.get('username')
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)
