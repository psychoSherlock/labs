from flask import Flask, render_template, request, make_response

app = Flask(__name__)


@app.after_request
def add_csp_header(response):
    response.headers['Content-Security-Policy'] = "script-src 'self' https://accounts.google.com object-src 'none'"
    return response


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/profile')
def profile():
    username = request.args.get('username')
    return render_template('profile.html', username=username)


if __name__ == '__main__':
    app.run(debug=True)
