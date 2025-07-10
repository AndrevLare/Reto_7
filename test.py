try:
        with open('menus.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            MENUS = {}
except FileNotFoundError:
    print("no archivo")