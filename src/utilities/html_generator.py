from jinja2 import Environment, FileSystemLoader
import os


class HTMLGenerator:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader("C:/Users/motor/PycharmProjects/Obedy/src/template", "utf-8"))
        self.template = self.env.get_template("template.html")
    
    def generate_html(self, data):
        rendered_html = self.template.render(restaurants=data)
        return rendered_html
