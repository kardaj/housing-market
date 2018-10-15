from app.model import db


def make_app():
    from flask import Flask
    import flask_restful
    from flask_cors import CORS
    app = Flask(__name__)

    app.config.from_object(app_conf)
    api = flask_restful.Api(app)
    CORS(
        app,
        allow_headers=['authorization', 'content-type', 'if-modified-since'],
        expose_headers=['last-modified']
    )
    db.init_app(app)
    return app, api


app, api = make_app()


def main():
    app.run(host='127.0.0.1', port=9999, debug=False)


if __name__ == "__main__":
    main()
