from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

simple_page = Blueprint('simple_page', __name__,  template_folder='templates')

@simple_page.route('/views/', defaults={'page': 'main'})
@simple_page.route('/views/<page>')
def show(page='main'):
    try:
        return render_template(f'page/{page}.html')
    except TemplateNotFound:
        abort(404)