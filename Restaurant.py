import json
import os

from queue import Queue
from collections import namedtuple

clear = lambda : os.system('cls')
MENUS = []

class MenuItem():
    def __init__(self, name:str, price:float):
        self.name = name
        self.price = price

    def get_name(self):
        return self.name

    def set_name(self, name:str):
        self.name = name

    def get_price(self):
        return self.price

    def set_price(self, price:float):
        self.price = price
    
    def to_dict(self):
        """Convertir objeto a diccionario para JSON"""
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "price": self.price
        }

class MainCourse(MenuItem):
    def __init__(self, flour:str, protein:str, salad:str, name:str, price:float):
        super().__init__(name, price)
        self.flour = flour
        self.protein = protein
        self.salad = salad
        
    def get_flour(self):
        return self.flour

    def set_flour(self, flour:str):
        self.flour = flour

    def get_protein(self):
        return self.protein

    def set_protein(self, protein:str):
        self.protein = protein

    def get_salad(self):
        return self.salad

    def set_salad(self, salad:str):
        self.salad = salad

    def __str__(self):
        return f"{self.name} ({self.flour}, {self.protein}, {self.salad}) - ${self.price:.2f}"
    
    def to_dict(self):
        """Convertir objeto a diccionario para JSON"""
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "price": self.price,
            "flour": self.flour,
            "protein": self.protein,
            "salad": self.salad
        }
    
    def __str__(self):
        return f"{self.name} ({self.flour}, {self.protein}, {self.salad}) - ${self.price:.2f}"

class Dessert(MenuItem):
    def __init__(self, name:str, price:float, type:str):
        super().__init__(name, price)
        self.type = type

    def get_type(self):
        return self.type

    def set_type(self, type:str):
        self.type = type

    def __str__(self):
        return f"{self.name} ({self.type}) - ${self.price:.2f}"
    
    def to_dict(self):
        """Convertir objeto a diccionario para JSON"""
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "price": self.price,
            "dessert_type": self.type
        }
    
    def __str__(self):
        return f"{self.name} ({self.type}) - ${self.price:.2f}"
    
class Drink(MenuItem):
    def __init__(self, name:str, price:float, size:str, hasSugar:bool):
        super().__init__(name, price)
        self.size = size
        self.hasSugar = hasSugar

    def get_size(self):
        return self.size

    def set_size(self, size:str):
        self.size = size

    def get_hasSugar(self):
        return self.hasSugar

    def set_hasSugar(self, hasSugar:bool):
        self.hasSugar = hasSugar

    def __str__(self):
        return f"{self.name} ({self.size}) - ${self.price:.2f}"
    
    def to_dict(self):
        """Convertir objeto a diccionario para JSON"""
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "price": self.price,
            "size": self.size,
            "hasSugar": self.hasSugar
        }
    
    def __str__(self):
        return f"{self.name} ({self.size}) - ${self.price:.2f}"

class Order():
    def __init__(self, items:list[MenuItem]):
        self.items = items
    
    def get_items(self):
        return self.items

    def set_items(self, items:list[MenuItem]):
        self.items = items

    def add_item(self, item:MenuItem):
        self.items.append(item)
    
    def __calcSubcounts(self, partial):
        dicounts = 0
        if len(self.items) >= 3:
            dicounts += 0.1 * partial
        return dicounts
            
    def getTotalBill(self):
        self.partial = sum(item.price for item in self.items)
        self.discounts = self.__calcSubcounts(self.partial)
        return self.partial - self.discounts

    def get_partial(self):
        return getattr(self, 'partial', 0)

    def get_discounts(self):
        return getattr(self, 'discounts', 0)
    
    def __str__(self):
        return "\n".join(str(item) for item in self.items)
    
class PaymentMethod:
  def __init__(self):
    pass

  def pay(self, monto):
    raise NotImplementedError("Subclases deben implementar pagar()")

class Card(PaymentMethod):
  def __init__(self, numero, cvv):
    super().__init__()
    self.__numero = numero
    self.__cvv = cvv
  def set_numero(self, numero):
        self.__numero = numero
  def set_cvv(self, cvv):
        self.__cvv = cvv
  def get_numero(self):
        return self.__numero
  def get_cvv(self):
        return self.__cvv

  def pay(self, monto):
    print(f"Pagando {monto} con tarjeta ...1{self.get_numero()[-4:]}")

class Cash(PaymentMethod):
  def __init__(self, monto_entregado):
    super().__init__()
    self.monto_entregado = monto_entregado

  def pay(self, monto):
    if self.monto_entregado >= monto:
      print(f"Pago realizado en efectivo. Cambio: {self.monto_entregado - monto}")
    else:
      print(f"Fondos insuficientes. Faltan {monto - self.monto_entregado} para completar el pago.")
    
    
def main_menu():
    clear()
    
    print("Bienvenido al restaurante! Por favor, elija una opción: \n\n1. Añadir una nueva orden \n2. Ver ordenes \n3. Cobrar orden \n4. Ver menus \n5. Salir")
    
    try:
        menu_option = int(input("\n\n"))
        if not(1 <= menu_option <= 5):
            raise Exception()
        if False:
            raise NotImplementedError("No hay ningun menu, primero crea uno...\n")
    except NotImplementedError as e:
        input(f"{e} Enter para continuar...\n")
        main_menu()
        return
    except:
        input("El valor debe ser un entero entre el 1 y el 5, intentalo de nuevo, Enter para continuar...\n")
        main_menu()
        return
    
    match menu_option:
        case 1:
            create_order()     
        case 4:
            menus_menu()
            
def create_order():
    clear()
    order = []
    
    while True:
        try:
            menu = int(input("Selecciona el menu del que quieres pedir primero, 0 si no quieres ordenar mas: "))
            if not(True): # Verificar que el indice este dentro de la cantidad de menus
             raise Exception()
        except:
            input("\nEl valor debe ser un entero entre el 1 y el {}, intentalo de nuevo, Enter para continuar\n\n") # cambiar por el numero de menus
            main_menu()
            return
        if menu == 0: break
        partial_order = order_from_menu(menu)
        
    final_order = Order(order)

def order_from_menu(menu_id):
    clear()

def menus_menu():
    clear()
    try:
        selection = int(input("Que deseas hacer? \n1. Crear menu \n2. Borrar Menu \n3. Ver menus disponibles \n0. Para volver\n\n"))
        if not(0 <= selection <= 3):
            raise Exception()
    except:
        input("\nEl valor debe ser un entero entre el 0 y el 3, intentalo de nuevo, Enter para continuar\n\n")
        menus_menu()
        return
    
    match selection:
        case 0:
            main_menu()
            return
        case 1:
            create_menu()
        case 2:
            pass
        case 3:
            clear()
            if MENUS == []:
                input("No hay ningun menu en este momento, por favor, crea uno primero, Enter para continuar\n")
                menus_menu()
                return
            print("Menus disponibles:\n")
            for menu in MENUS:
                print(print_menu(menu))
            input("\n\nPresiona Enter para continuar...\n")
            menus_menu()
            return
            
            
def create_menu():
    clear()
    try:
        menu_name = input("Inserta el nombre del nuevo menu: ")
        if not(0 < len(menu_name) <= 20):
            raise NameError("\nLongitud de nombre invalida, empieza de nuevo...")
    except NameError as e:
        input(f"{e} Enter para continuar\n")
        create_menu()
        return
    
    print("\nAhora, añade los prouctos.\n")

    products = []

    while True:
        clear()
        try:
            name = input("Ingrese el nombre del producto, \"0\" si no quieres añadir mas:")
            if name == "0": 
                print("\nNo se añadiran mas productos...\n")
                break
            if not(0 < len(name) <= 20):
                raise NameError("longitud de nombre invalida, empieza de nuevo...")
            price = float(input("\nIngrese el precio del producto: "))
            if not(0 <= price):
                raise NameError("Ingresa un precio valido, empieza de nuevo...")
            type = int(input("\nIngresa el tipo de producto: \n1. Plato principal \n2. Postre \n3. Bebida\n"))
            if not(1 <= type <= 3):
                raise NameError("Tipo de procucto invalido, empieza de nuevo...")
            match type:
                case 1:
                    protein = input("\nIntroduce la proteina: ")
                    salad = input("\nIntroduce la ensalada: ")
                    flour = input("\nIntroduce la harina: ")
                    product = MainCourse(flour, protein, salad, name, price)
                case 2:
                    type = input("\nIntroduce el tipo de postre (pastel, galleta, etc...): ")
                    product = Dessert(name, price, type)
                case 3:
                    size = input("\nIntroduce el tamaño: ")
                    hasSugar = True if input("\nTiene azucar? (y/n): ").lower() == 'y' else False
                    if not(hasSugar == 0 or hasSugar == 1):
                        raise NameError("\nIngresa un precio valido, empieza de nuevo...")
                    product = Drink(name, price, size, hasSugar)
                case default:
                    raise NameError("\nTipo de producto invalido, empieza de nuevo...")
        except NameError as e:
            input(f"{e} Enter para continuar\n")
            continue
        except:
            input("\nHa habido un error inesperado, intenta de nuevo, Enter para continuar\n")
            continue
        products.append(product)
        
    # Convertir objetos a diccionarios para JSON
    products_dict = [product.to_dict() for product in products]
    
    menu = {
        "name": menu_name,
        "products": products
    }
    MENUS.append(menu)
    save_menu(menu_name, products_dict)
    
def save_menu(name, products):
    try:
        with open("menus.json", "w", encoding="utf-8") as file:
            new_json = json.load(file)
            new_menu = {
                "name": name,
                "products": products
            }
            new_json.append(new_menu)
            json.dump(new_json, file, indent=4, ensure_ascii=False)    
        print("\nMenu guardado exitosamente\n")
        main_menu()
    except FileNotFoundError:
        input("\nNo se pudo crear el archivo, intenta de nuevo, Enter para continuar\n")
        create_menu()
    except PermissionError:
        input("\nNo tienes permisos para escribir, intenta de nuevo, Enter para continuar\n")
        create_menu()
    except Exception as e:
        input(f"\nError inesperado: {e}, intenta de nuevo, Enter para continuar\n")
        create_menu()
def load_menus():
    global MENUS
    try:
        with open('menus.json', 'r', encoding='utf-8') as file:
            if os.path.getsize('menus.json') == 0:
                 with open('default.json', 'r', encoding='utf-8') as default_file:
                    data = json.load(default_file)
            else:
                data = json.load(file)
            for menu in data:
                products = []
                for product in menu["products"]:
                    category = product["type"].lower()
                    match category:
                        case "drink":
                            products.append(Drink(product["name"],
                                                  product["price"],
                                                  product["size"],
                                                  product["hasSugar"]))
                        case "dessert":
                            products.append(Dessert(product["name"],
                                                    product["price"],
                                                    product["dessert_type"]))
                        case "maincourse":
                            products.append(MainCourse(product["flour"],
                                                      product["protein"],
                                                      product["salad"],
                                                      product["name"],
                                                      product["price"]))
                menu = {
                    "name": menu["name"],
                    "products": products
                }
                MENUS.append(menu)
    except FileNotFoundError:
        return
    
def print_menu(menu):
    output = (f"{menu["name"]}: \n")
    for product in menu["products"]:
        output += f"\t{product.__str__()}\n"
    return (output + "\n")
        
if __name__ == "__main__":
    clear()
    load_menus()
    main_menu()