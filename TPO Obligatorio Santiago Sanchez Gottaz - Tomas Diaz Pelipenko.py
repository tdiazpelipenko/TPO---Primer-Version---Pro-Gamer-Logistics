
# TRABAJO PRÁCTICO OBLIGATORIO: SEGUNDO PARCIAL
# grupo: Santiago Sanchez Gottas -  TOMAS IVO DIAZ PELIPENKO

import random 


# FUNCIONES DE VALIDACIÓN
# Estas funciones garantizan la integridad de los datos de entrada
# según las reglas del negocio antes de guardarlos en las listas


def validar_id_producto(id_prod):
    # Valida que el ID tenga entre 4 y 10 caracteres
    # y que solo use letras, numeros o "_".
    largo = 0
    for caracter in id_prod:
        largo += 1
        
    if largo < 4 or largo > 10: # Restricción de longitud (4 a 10 caracteres) 
        return False
        
    es_valido = True
    i = 0
    # Usamos ciclo condicional controlado lógicamente (sin break ni flags) 
    while i < largo and es_valido:
        caracter = id_prod[i]
        # Validación por rangos de caracteres de la tabla ASCII
        es_alfa = ('A' <= caracter <= 'Z') or ('a' <= caracter <= 'z')
        es_num = ('0' <= caracter <= '9')
        es_guion = (caracter == '_')
        
        if not (es_alfa or es_num or es_guion):
            es_valido = False # El ciclo ttermina en la próxima iteración al volverse falso
        i += 1
        
    return es_valido

def validar_descripcion(desc):
    # Verifica que la descripción empiece con una letra
    # y que la cadena de texto no esté vacía.
    largo = 0
    for caracter in desc:
        largo += 1
        
    if largo == 0:
        return False
        
    primera_letra = desc[0]
    es_letra = ('A' <= primera_letra <= 'Z') or ('a' <= primera_letra <= 'z')
    return es_letra

def validar_categoria():
    # Controla que la categoría ingresada esté dentro del grupo permitido.
    # Si el usuario presiona Enter (vacio), por regla del negocio se asigna a 'Varios'.
    print("\nCategorías disponibles: Monitores, Sillas, Periféricos, Hardware, Accesorios, Varios")
    cat = input("Ingrese la categoría: ")
    
    if cat == "":
        return "Varios" 
        
    while cat not in ["Monitores", "Sillas", "Periféricos", "Hardware", "Accesorios", "Varios"]:
        print("Categoría no válida. Intente nuevamente.")
        cat = input("Ingrese la categoría: ")
        if cat == "":
            cat = "Varios"
            
    return cat

def validar_marca(marca):
    # Cuenta cuántas letras reales posee la marca para asegurar
    # que cumpla con el mínimo de 3 letras requerido.
    largo = 0
    for caracter in marca:
        if ('A' <= caracter <= 'Z') or ('a' <= caracter <= 'z'):
            largo += 1
            
    return largo >= 3

# OPERACIONES DEL SISTEMA (ALTA, BAJA Y MODIFICACIÓN)
# Funciones encargadas de interactuar con el usuario y alterar las
# estructuras de datos en la memoria RAM.

def registrar_producto(ids, descripciones, categorias, precios, stocks, marcas):
    # Permite la carga interactiva (manual) o la simulación rápida (aleatoria).
    # Al final, añade los datos validados al final de cada lista mediante .append() respetando el paralelismo.
    print("\n--- Registrar Nuevo Producto (Alta) ---")
    print("1. Ingreso Manual por teclado")
    print("2. Generación Automática Aleatoria (Para pruebas)")
    
    opcion = input("Seleccione método de carga (1-2): ")
    while opcion != "1" and opcion != "2":
        opcion = input("Opción inválida. Seleccione 1 o 2: ")
        
    if opcion == "1":
        id_prod = input("ID Producto (4-10 caracteres, alfanumérico/_): ")
        while not validar_id_producto(id_prod):
            id_prod = input("ID Inválido. Ingrese nuevamente: ")
            
        desc = input("Descripción (Debe empezar con letra): ")
        while not validar_descripcion(desc):
            desc = input("Descripción Inválida. Ingrese nuevamente: ")
            
        cat = validar_categoria()
        
        precio = float(input("Precio unitario en USD (Positivo): "))
        while precio <= 0: # Validación de número positivo con decimales 
            precio = float(input("El precio debe ser mayor a 0. Ingrese nuevamente: "))
            
        stock = int(input("Stock disponible (Entero positivo): "))
        while stock < 0: # Validación de entero positivo o cero 
            stock = int(input("El stock no puede ser negativo. Ingrese nuevamente: "))
            
        marca = input("Marca fabricante (Mínimo 3 letras): ")
        while not validar_marca(marca):
            marca = input("Marca inválida. Ingrese nuevamente: ")
            
    else:
        # Generación aleatoria usando el módulo random para agilizar pruebas de cátedra 
        id_prod = "PROD" + str(random.randint(100, 999))
        desc = "Componente Gamer " + str(random.randint(1, 100))
        cat = random.choice(["Monitores", "Sillas", "Periféricos", "Hardware", "Accesorios"])
        precio = round(random.uniform(10.0, 500.0), 2)
        stock = random.randint(0, 50) 
        marca = random.choice(["Logitech", "Razer", "HyperX", "ASUS", "Corsair"])
        print(f"\nProducto generado: {id_prod} - {desc} - {marca}")

    # Sincronización en Listas Paralelas: Todos guardan en el mismo índice del vector 
    ids.append(id_prod)
    descripciones.append(desc)
    categorias.append(cat)
    precios.append(precio)
    stocks.append(stock)
    marcas.append(marca)
    print("¡Producto registrado con éxito!")

def eliminar_producto(ids, descripciones, categorias, precios, stocks, marcas):
    """
    EXPOSICIÓN: Busca un ID sin usar .index(). Si lo halla, comprueba que su stock
    sea exactamente 0 y pide confirmación antes de removerlo de los vectores.
    """
    print("\n--- Eliminar Producto (Baja) ---")
    id_buscar = input("Ingrese el ID del producto a eliminar: ")
    
    posicion = -1
    i = 0
    largo = len(ids)
    # Búsqueda secuencial manual con ciclo estricto (parar al encontrar el elemento) 
    while i < largo and posicion == -1:
        if ids[i] == id_buscar:
            posicion = i # Se guarda la posición común de las listas 
        i += 1
        
    if posicion == -1:
        print("Error: El identificador de producto no existe.")
    else:
        if stocks[posicion] != 0: # Regla de negocio: Solo se elimina si no hay stock disponible 
            print(f"No se puede eliminar: El producto tiene {stocks[posicion]} unidades en stock.")
        else:
            confirmar = input(f"¿Está seguro que desea eliminar '{descripciones[posicion]}'? (S/N): ")
            if confirmar.upper() == "S":
                # Al usar .pop(posicion), eliminamos el elemento en paralelo de todas las listas 
                ids.pop(posicion)
                descripciones.pop(posicion)
                categorias.pop(posicion)
                precios.pop(posicion)
                stocks.pop(posicion)
                marcas.pop(posicion)
                print("Producto eliminado correctamente.")
            else:
                print("Operación cancelada.")

def modificar_stock(descripciones, stocks):
    # EXPOSICIÓN: Localiza el producto mediante su descripción comercial exacta.
    #Si existe, modifica el elemento de la lista de stocks usando asignación directa por índice.
    print("\n--- Modificar Cantidad en Stock ---")
    desc_buscar = input("Ingrese la descripción exacta del producto: ")
    
    posicion = -1
    i = 0
    largo = len(descripciones)
    while i < largo and posicion == -1:
        if descripciones[i] == desc_buscar:
            posicion = i
        i += 1
        
    if posicion == -1:
        print("Error: No se encontró ningún producto con esa descripción.")
    else:
        print(f"Producto encontrado: {descripciones[posicion]} | Stock actual: {stocks[posicion]}")
        nuevo_stock = int(input("Ingrese la nueva cantidad de stock: "))
        while nuevo_stock < 0:
            nuevo_stock = int(input("El stock no puede ser negativo. Ingrese nuevamente: "))
            
        stocks[posicion] = nuevo_stock # Modificación en memoria RAM
        print("¡Stock actualizado con éxito!")


# REPORTE Y ALGORITMO DE ORDENAMIENTO MANUAL
# Genera el informe ordenado pedido. No altera los vectores originales.
# Usa ordenamiento de burbuja manual 


def mostrar_informe_general(ids, descripciones, categorias, precios, stocks, marcas):
    # Duplica los vectores de datos para ordenar las copias y proteger los datos
    # originales. Aplica el método Burbuja combinando dos criterios de ordenamiento.

    print("\n--- INFORME GENERAL DE STOCK --- ")
    
    largo = len(ids)
    if largo == 0:
        print("No hay productos registrados en el sistema.")
        return
        
    # Clonación manual de colecciones para preservar el orden original de carga
    c_ids = list(ids)
    c_desc = list(descripciones)
    c_cat = list(categorias)
    c_prec = list(precios)
    c_stock = list(stocks)
    c_marca = list(marcas)
    
    i = 0
    while i < largo - 1:
        j = 0
        while j < largo - i - 1:
            debe_intercambiar = False
            
            # CRITERIO 1: Mayor a menor por Stock 
            if c_stock[j] < c_stock[j + 1]:
                debe_intercambiar = True
                
            # CRITERIO 2: Si empatan en stock, ordena alfabéticamente  
            elif c_stock[j] == c_stock[j + 1]:
                if c_desc[j] > c_desc[j + 1]:
                    debe_intercambiar = True
                    
            if debe_intercambiar:
                # INTERCAMBIO EN ESPEJO: Si se mueve una estructura, se tienen que mover todas
                # las demás listas paralelas para no mezclar los datos de los productos.
                c_ids[j], c_ids[j+1] = c_ids[j+1], c_ids[j]
                c_desc[j], c_desc[j+1] = c_desc[j+1], c_desc[j]
                c_cat[j], c_cat[j+1] = c_cat[j+1], c_cat[j]
                c_prec[j], c_prec[j+1] = c_prec[j+1], c_prec[j]
                c_stock[j], c_stock[j+1] = c_stock[j+1], c_stock[j]
                c_marca[j], c_marca[j+1] = c_marca[j+1], c_marca[j]
            j += 1
        i += 1

    # Salida formateada de datos simulando una tabla en consola
    print(f"{'ID':<12} | {'Descripción':<25} | {'Categoría':<15} | {'Marca':<12} | {'Precio (USD)':<12} | {'Stock':<6}")
    print("-" * 92)
    
    k = 0
    while k < largo:
        print(f"{c_ids[k]:<12} | {c_desc[k]:<25} | {c_cat[k]:<15} | {c_marca[k]:<12} | {c_prec[k]:<12.2f} | {c_stock[k]:<6}")
        k += 1


# CONTROLADOR PRINCIPAL DEL PROGRAMA
# Coordina la inicialización del sistema y el flujo del menú

def mostrar_menu():
    print("\n=========================================")
    print("SISTEMA DE GESTIÓN: PRO-GAMER LOGISTICS")
    print("=========================================")
    print("1. Registrar nuevo producto (Alta)")
    print("2. Eliminar producto del sistema (Baja)")
    print("3. Modificar cantidad en stock (Modificación)")
    print("4. Informe General - Visualización de los datos")
    print("8. Salir")
    print("=========================================")

def main():
    # Inicialización en la RAM de las 6 listas paralelas requeridas por el enunciado 
    lista_ids = []
    lista_descripciones = []
    lista_categorias = []
    lista_precios = []
    lista_stocks = []
    lista_marcas = []
    
    ejecutando = True 
    
    while ejecutando:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-4 o 8 para salir): ")
        
        if opcion == "1":
            registrar_producto(lista_ids, lista_descripciones, lista_categorias, lista_precios, lista_stocks, lista_marcas)
        elif opcion == "2":
            eliminar_producto(lista_ids, lista_descripciones, lista_categorias, lista_precios, lista_stocks, lista_marcas)
        elif opcion == "3":
            modificar_stock(lista_descripciones, lista_stocks)
        elif opcion == "4":
            mostrar_informe_general(lista_ids, lista_descripciones, lista_categorias, lista_precios, lista_stocks, lista_marcas)
        elif opcion == "8":
            print("\nFinalizando la ejecución del sistema. ¡Hasta luego!")
            ejecutando = False # Condición lógica que vuelve falso el bucle while 
        else:
            print("\nOpción no válida. Por favor, intente con los números indicados del menú.")


main()