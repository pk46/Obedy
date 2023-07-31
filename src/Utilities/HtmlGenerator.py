    #    restaurant_data = []
for restaurant_name, menu in results:
    restaurant_data.append({
        'name': restaurant_name,
        'menu': menu
    })


    with open("output.html", "w", encoding="utf-8") as file:
        template = Template(open("template.html").read())
        file.write(template.render(results=results))