import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
    # Bind to localhost only unless BIND_ALL_INTERFACES is set
    host = '0.0.0.0' if os.getenv('BIND_ALL_INTERFACES') else '127.0.0.1'
    port = int(os.getenv('PORT', 8080))
    # Explicitly disable debug mode for security
    app.run(host=host, port=port, debug=False, threaded=True)

def keep_alive():
    t = Thread(target=run, daemon=True)
    t.start()