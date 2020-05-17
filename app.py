from flask import Flask, render_template

app = Flask('PythonBI')

@app.route('/')
def index():
    return render_template('login.html')

from views.page import simple_page
app.register_blueprint(simple_page)
from views.api import api
app.register_blueprint(api)


if __name__ == "__main__":
    app.run(debug=True)