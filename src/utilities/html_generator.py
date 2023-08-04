from jinja2 import Environment, FileSystemLoader
import os


class HTMLGenerator:
    def __init__(self):
        os.chdir("..")
        os.chdir("static/template")
        self.env = Environment(loader=FileSystemLoader('./', "utf-8"))
        self.template = self.env.get_template("template.html")
    
    def generate_html(self, data):
        rendered_html = self.template.render(restaurants=data)
        os.chdir("..")
        os.chdir("..")
        return rendered_html
