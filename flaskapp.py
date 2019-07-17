from flask import Flask, Response
flask_app = Flask('flaskapp')


@flask_app.route('/hello')
def hello_world():
    return Response(
        'Suuuup from Flask world ayeeeee!\n',
        mimetype='text/plain'
    )

app = flask_app.wsgi_app
