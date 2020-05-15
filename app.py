from flask import Flask, render_template

app = Flask('PythonBI')

@app.route('/')
def index():
    return render_template('page/main.html')

from views.page import simple_page
app.register_blueprint(simple_page)


if __name__ == "__main__":
    app.run(debug=True)