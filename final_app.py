import os
import logging
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, abort

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "tlc-business-solutions-secret")

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.context_processor
def inject_now():
    return {'now': datetime.datetime.now()}

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logging.exception("Failed to render index.html")
        abort(500)

@app.errorhandler(404)
def page_not_found(e):
    return "Page not found.", 404

@app.errorhandler(500)
def internal_error(e):
    return "Internal server error. Please check your template and route setup.", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
