import sys

sys.path.append('..')

from server import app
from os import environ

if __name__ == "__main__":
    path = environ["PATH"]
    print(path)
    app.run(debug=True)
