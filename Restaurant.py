import json
import os

from queue import Queue
from collections import namedtuple

ProductSummary = namedtuple('ProductSummary', ['name', 'price', 'type'])

clear = lambda : os.system('cls')
MENUS = []
orders_queue = Queue()

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
    
    def pay(self):
        total = self.getTotalBill()
        if total <= 0:
            print("No hay nada que pagar.")
            return
        payment_method = input("Elige el metodo de pago (tarjeta/efectivo): ").strip().lower()
        if payment_method == "tarjeta":
            numero = input("Ingresa el numero de la tarjeta: ")
            cvv = input("Ingresa el CVV de la tarjeta: ")
            card = Card(numero, cvv)
            card.pay(total)
        elif payment_method == "efectivo":
            monto_entregado = float(input("Ingresa el monto entregado: "))
            cash = Cash(monto_entregado)
            cash.pay(total)
        else:
            input("Metodo de pago no reconocido. Intenta de nuevo.\n")
            self.pay()
    
    def __str__(self):
        return f"Order with {len(self.items)} items, Total: ${self.getTotalBill():.2f}, Discounts: ${self.get_discounts():.2f}, Partial: ${self.get_partial():.2f}"
    
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
    
    print("Bienvenido al restaurante! Por favor, elija una opción: \n\n1. Añadir una nueva orden \n2. Ver ordenes \n3. Cobrar orden \n4. Ver menus \n0. Salir")
    
    try:
        menu_option = int(input("\n\n"))
        if not(0 <= menu_option <= 4):
            raise Exception()
        if False:
            raise NotImplementedError("No hay ningun menu, primero crea uno...\n")
    except NotImplementedError as e:
        input(f"{e} Enter para continuar...\n")
        main_menu()
        return
    except:
        input("El valor debe ser un entero entre el 0 y el 4, intentalo de nuevo, Enter para continuar...\n")
        main_menu()
        return
    
    match menu_option:
        case 0:
            clear()
            print("Gracias por visitarnos! Hasta luego!")
            exit(0)
        case 1:
            create_order()  
        case 2:
            clear()   
            print("--- Ordenes pendientes ---")
            if orders_queue.empty():
                print("No hay ordenes pendientes, o somos rapidos o vamos a quebrar :(")
            else:
                for order in orders_queue.queue:
                    print(order)
            input("\n\nPresiona Enter para continuar...\n")
            main_menu()
        case 3:
            clear()
            if orders_queue.empty():
                input("No hay ordenes pendientes, por favor, crea una primero, Enter para continuar\n")
                main_menu()
                return
            print("--- Ordenes pendientes ---")
            for order in orders_queue.queue:
                print(order)
            if input("\nQuieres cobrar la primera orden? (y/n): ").lower() == 'y':
                order = orders_queue.get()
                order.pay()
                input(f"\nOrden cobrada, total: ${order.getTotalBill():.2f}, Enter para continuar\n")
            else:
                input("No se ha cobrado ninguna orden, Enter para continuar\n")
            main_menu()
        case 4:
            menus_menu()
            
def create_order():
    clear()
    order = []
    
    while True:
        clear()
        try:
            print("Menus disponibles:\n")
            for menu in MENUS:
                print(menu['name'], end="\n")
            menu_name = input("Ingresa el nombre del menu del que quieres pedir, 0 si no quieres ordenar mas: ")
            menu = next((menu for menu in MENUS if menu['name'] == menu_name), None)
            if menu_name == "0":
                if not order:
                    input("No has añadido ningun producto, por favor, añade uno primero, Enter para continuar\n")
                    continue
                break
            if not menu:
                raise NameError("Menu no encontrado, intenta de nuevo...")
        except NameError as e:
            input(f"\n{e}, Enter para continuar\n\n")
            main_menu()
            return
        if menu == 0: break
        partial_order = order_from_menu(menu)
        for _ in partial_order:
            order.append(_)
        input(f"\nOrden parcial añadida, tienes {len(order)} productos en la orden, Enter para continuar\n")
    
    final_order = Order(order)
    orders_queue.put(final_order)
    input(f"\nOrden creada con {len(order)} productos, Enter para continuar\n")
    main_menu()

def order_from_menu(menu):
    clear()
    order = []
    print("Menu seleccionado: ", menu['name'], "\n")
    if not menu['products']:
        input("No hay ningun producto en este menu, por favor, añade uno primero, Enter para continuar\n")
        menus_menu()
        return
    print("Productos del menu:")
    for product in menu['products']:
        print(product, end="\n")
    try:
        product_name = input("\nIngresa el nombre del producto que quieres añadir a la orden: ")
        product = next((p for p in menu['products'] if p.name == product_name), None)
        if not product:
            raise NameError("Producto no encontrado, intenta de nuevo...")
        quantity = int(input("\nIngresa la cantidad de este producto que quieres añadir a la orden: "))
        if not(0 < quantity <= 20):
            raise NameError("Cantidad invalida, debe ser un entero entre 1 y 20, intenta de nuevo...")
        for _ in range(quantity):
            order.append(product)
    except NameError as e:
        input(f"\n{e}, Enter para continuar\n\n")
        return order_from_menu(menu)
    return order

def menus_menu():
    clear()
    try:
        selection = int(input("Que deseas hacer? \n1. Crear menu \n2. Borrar Menu \n3. Ver menus disponibles \n4. Editar Menus \n0. Para volver\n\n"))
        if not(0 <= selection <= 4):
            raise Exception()
    except:
        input("\nEl valor debe ser un entero entre el 0 y el 4, intentalo de nuevo, Enter para continuar\n\n")
        menus_menu()
        return
    
    match selection:
        case 0:
            main_menu()
            return
        case 1:
            create_menu()
        case 2:
            delete_menu()
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
        case 4:
            update_menu()
            
def update_menu():
    clear()
    print("Menus disponibles:\n")
    for menu in MENUS:
        print(menu['name'], end="\n")
    name = input("Inserta el nombre del menu que quieres editar: ")
    menu = next((menu for menu in MENUS if menu['name'] == name), None)
    if not menu:
        input("Menu no encontrado, intenta de nuevo...\n")
        menus_menu()
        return
    clear()
    try:
        selection = int(input(f"\nMenu seleccionado: {menu['name']}, que deseas hacer?\n\n1. Editar nombre del menu \n2. Añadir producto \n3. Eliminar producto \n4. Ver productos del menu \n0. Para volver\n"))
        if not(0 <= selection <= 4):
            raise NameError("El valor debe ser un entero entre el 0 y el 4,")
        match selection:
            case 0:
                menus_menu()
                return
            case 1:
                clear()
                print("Menu seleccionado: ", menu['name'], "\n")
                new_name = input("Inserta el nuevo nombre del menu: ")
                if not(0 < len(new_name) <= 20) or any(menu['name'] == new_name for menu in MENUS):
                    raise NameError("\nLongitud de nombre invalida o el nombre ya está en uso, empieza de nuevo...")
                menu['name'] = new_name
            case 2:
                clear()
                print("Menu seleccionado: ", menu['name'], "\n")
                product_name = input("\nIngresa el nombre del producto.\n")
                if not(0 < len(product_name) <= 20):
                    raise NameError("\nLongitud de nombre invalida, empieza de nuevo...")
                price = float(input("\nIngresa el precio del producto: "))
                if not(0 <= price):
                    raise NameError("\nIngresa un precio valido, empieza de nuevo...")
                type = int(input("\nIngresa el tipo de producto: \n1. Plato principal \n2. Postre \n3. Bebida\n"))
                if not(1 <= type <= 3):
                    raise NameError("\nTipo de procucto invalido, empieza de nuevo...")
                match type:
                    case 1:
                        flour = input("\nIntroduce la harina: ")
                        protein = input("\nIntroduce la proteina: ")
                        salad = input("\nIntroduce la ensalada: ")
                        product = MainCourse(flour, protein, salad, product_name, price)
                    case 2:
                        dessert_type = input("\nIntroduce el tipo de postre (pastel, galleta, etc...): ")
                        product = Dessert(product_name, price, dessert_type)
                    case 3:
                        size = input("\nIntroduce el tamaño: ")
                        hasSugar = True if input("\nTiene azucar? (y/n): ").lower() == 'y' else False
                        if not(hasSugar == 0 or hasSugar == 1):
                            raise NameError("\nIngresa un valor valido, empieza de nuevo...")
                        product = Drink(product_name, price, size, hasSugar)
                menu['products'].append(product)
            case 3:
                clear()
                print("Menu seleccionado: ", menu['name'], "\n")
                product_name = input("\nIngresa el nombre del producto que quieres eliminar.\n")
                product = next((p for p in menu['products'] if p.name == product_name), None)
                if not product:
                    raise NameError("\nProducto no encontrado, empieza de nuevo...")
                menu['products'].remove(product)
            case 4:
                clear()
                print("Menu seleccionado: ", menu['name'], "\n")
                if not menu['products']:
                    input("No hay ningun producto en este menu, por favor, añade uno primero, Enter para continuar\n")
                    update_menu()
                    return
                print("Productos del menu:")
                for product in menu['products']:
                    print(product, end="\n")
                input("\n\nPresiona Enter para continuar...\n")
                update_menu()
                return
        with open("menus.json", "w", encoding="utf-8") as file:
            json.dump([menu_to_dict(m) for m in MENUS], file, indent=4, ensure_ascii=False)
        input(f"\nMenu actualizado. Enter para continuar\n")
        update_menu()
                    
    except NameError as e:
        input(f"{e} Enter para continuar\n")
        menus_menu()
        return
    
    
def delete_menu():
    clear()
    name = input("Inserta el nombre del menu que quieres eliminar: ")
    new_menus = []
    try:
        menu = next((menu for menu in MENUS if menu['name'] == name), None)
        if not menu:
            raise NameError("Menu no encontrado, intenta de nuevo...")
        MENUS.remove(menu)
        with open("menus.json", "r", encoding="utf-8") as file:
            try:
                new_menus = json.load(file)
            except json.JSONDecodeError:
                pass # Si el archivo está vacío o corrupto, no hacemos nada
        with open("menus.json", "w", encoding="utf-8") as file:
            # Filtrar los menús que no coinciden con el nombre a eliminar
            new_menus = [m for m in new_menus if m['name'] != name]
            json.dump(new_menus, file, indent=4, ensure_ascii=False)
        input(f"\nMenu '{name}' eliminado exitosamente. Enter para conitnuar\n")
        menus_menu()
    except NameError as e:
        input(f"{e} Enter para continuar\n")
        menus_menu()
            
def create_menu():
    clear()
    try:
        menu_name = input("Inserta el nombre del nuevo menu: ")
        if not(0 < len(menu_name) <= 20) or any(menu['name'] == menu_name for menu in MENUS) or menu_name == "0":
            raise NameError("\nLongitud de nombre invalida o el nombre ya está en uso, empieza de nuevo...")
    except NameError as e:
        input(f"{e} Enter para continuar\n")
        menus_menu()
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
        # 1. Prepara una lista para guardar todos los menús.
        all_menus = []
        
        # 2. Intenta leer el archivo JSON existente.
        try:
            with open("menus.json", "r", encoding="utf-8") as file:
                # Si el archivo no está vacío, carga su contenido (la lista de menús).
                if os.path.getsize("menus.json") > 0:
                    all_menus = json.load(file)
        except FileNotFoundError:
            # Si el archivo no existe, no hay problema. Se creará más adelante.
            pass
        except json.JSONDecodeError:
            # Si el archivo está corrupto o vacío, empezamos con una lista vacía.
            pass

        # 3. Crea el nuevo menú como un diccionario.
        new_menu = {
            "name": name,
            "products": products
        }
        
        # 4. Añade el nuevo menú a la lista que leímos (o a la lista vacía si el archivo no existía).
        all_menus.append(new_menu)
        
        # 5. Escribe la lista completa y actualizada de vuelta en el archivo.
        #    El modo "w" borrará el contenido anterior y escribirá el nuevo.
        with open("menus.json", "w", encoding="utf-8") as file:
            json.dump(all_menus, file, indent=4, ensure_ascii=False)
            
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
                    with open('menus.json', 'w', encoding='utf-8') as new_file:
                        json.dump(data, new_file, indent=4, ensure_ascii=False)
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
    
def menu_to_dict(menu):
    return {
        "name": menu["name"],
        "products": [product.to_dict() for product in menu["products"]]
    }
    
def print_menu(menu):
    output = (f"{menu["name"]}: \n")
    for product in menu["products"]:
        output += f"\t{product.__str__()}\n"
    return (output + "\n")
        
if __name__ == "__main__":
    clear()
    load_menus()
    main_menu()
