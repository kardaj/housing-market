import argparse
from app.api import app


class Context(object):

    def __enter__(self):
        self.app = app
        self.context = app.app_context()
        self.context.push()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context.pop()


app_context = Context()
