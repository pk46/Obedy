from jinja2 import Environment, FileSystemLoader


class HTMLGenerator:
    def __init__(self, name):
        self.name = name
        self.env = Environment(loader=FileSystemLoader("C:/Users/motor/PycharmProjects/Obedy/src/template", "utf-8"))
        self.template = self.env.get_template("template.html")
    
    def generate_html(self, data):
        rendererd_html = self.template.render(
            title=self.name,
            data=data[0]
        )
        return rendererd_html
