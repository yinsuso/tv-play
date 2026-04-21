from sanic_jinja2 import SanicJinja2
from jinja2 import FileSystemLoader

jinja = SanicJinja2(loader=FileSystemLoader('templates'))
