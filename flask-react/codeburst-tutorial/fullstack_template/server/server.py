import random
import json
from flask import Flask, render_template

app = Flask(__name__, static_folder='../static/dist',
            template_folder='../static')

app.debug = True


@app.route('/')
def index():
    return render_template('index.html')


# take note of this decorator syntax, it's a common pattern
@app.route('/hello')
def hello():
    # It is good practice to only call a function in your route end-point,
    # rather than have actual implementation code here.
    # This allows for easier unit and integration testing of your functions.
    return get_hello()


def get_hello():
    greeting_list = ['Ciao', 'Hei', 'Salut', 'Hola', 'Hallo', 'Hej']
    return json.dumps({'hello': random.choice(greeting_list)})


if __name__ == '__main__':
    app.run()
