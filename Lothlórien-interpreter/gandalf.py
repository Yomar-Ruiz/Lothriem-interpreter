TIPOS = {
    "hobbit": str,
    "dwarf": int,
    "elf": float,
    "orc": bool
}


OPERACIONES = {
    "+": {
        ("dwarf", "dwarf"),
        ("dwarf", "elf"),
        ("elf", "dwarf"),
        ("elf", "elf"),
        ("hobbit", "hobbit")
    },

    "-": {
        ("dwarf", "dwarf"),
        ("dwarf", "elf"),
        ("elf", "dwarf"),
        ("elf", "elf")
    },

    "*": {
        ("dwarf", "dwarf"),
        ("dwarf", "elf"),
        ("elf", "dwarf"),
        ("elf", "elf")
    },

    "/": {
        ("dwarf", "dwarf"),
        ("dwarf", "elf"),
        ("elf", "dwarf"),
        ("elf", "elf")
    }
}


COMPARACIONES_NUMERICAS = {
    ">",
    "<",
    ">=",
    "<="
}


COMPARACIONES_IGUALDAD = {
    "==",
    "!="
}


def comprobar_tipo(tipo_variable, valor):

    if tipo_variable == "dwarf":
        return type(valor) is int

    if tipo_variable == "elf":
        return type(valor) is int or type(valor) is float

    tipo_esperado = TIPOS[tipo_variable]

    return isinstance(valor, tipo_esperado)


def tipo_de_valor(valor):

    if type(valor) is bool:
        return "orc"

    if type(valor) is int:
        return "dwarf"

    if type(valor) is float:
        return "elf"

    if type(valor) is str:
        return "hobbit"

    raise TypeError(
        f"No conozco el tipo del valor: {valor}"
    )


def comprobar_operacion(operador, izquierda, derecha):

    tipo_izquierda = tipo_de_valor(izquierda)
    tipo_derecha = tipo_de_valor(derecha)

    combinacion = (
        tipo_izquierda,
        tipo_derecha
    )

    if combinacion not in OPERACIONES[operador]:

        raise TypeError(
            f"No se puede usar '{operador}' entre "
            f"'{tipo_izquierda}' y '{tipo_derecha}'"
        )


def comprobar_comparacion(
    operador,
    izquierda,
    derecha
):

    tipo_izquierda = tipo_de_valor(izquierda)
    tipo_derecha = tipo_de_valor(derecha)

    tipos_numericos = {
        "dwarf",
        "elf"
    }

    if operador in COMPARACIONES_NUMERICAS:

        if (
            tipo_izquierda not in tipos_numericos
            or tipo_derecha not in tipos_numericos
        ):

            raise TypeError(
                f"No se puede usar '{operador}' entre "
                f"'{tipo_izquierda}' y '{tipo_derecha}'"
            )

    if operador in COMPARACIONES_IGUALDAD:

        combinaciones_permitidas = {
            ("dwarf", "dwarf"),
            ("dwarf", "elf"),
            ("elf", "dwarf"),
            ("elf", "elf"),
            ("hobbit", "hobbit"),
            ("orc", "orc")
        }

        combinacion = (
            tipo_izquierda,
            tipo_derecha
        )

        if combinacion not in combinaciones_permitidas:

            raise TypeError(
                f"No se puede comparar '{tipo_izquierda}' "
                f"con '{tipo_derecha}'"
            )


def ejecutar_bloque(bloque, entorno):

    resultado = None

    for instruccion in bloque:

        resultado = gandalf(
            instruccion,
            entorno
        )

    return resultado


def gandalf(nodo, entorno):

    if isinstance(nodo, bool):
        return nodo

    if isinstance(nodo, (int, float)):
        return nodo

    if isinstance(nodo, str):
        return nodo

    if nodo["tipo"] == "PROGRAM":

        resultado = None

        for instruccion in nodo["instrucciones"]:

            resultado = gandalf(
                instruccion,
                entorno
            )

        return resultado

    if nodo["tipo"] == "IDENTIFIER":

        nombre = nodo["nombre"]

        if nombre not in entorno:

            raise Exception(
                f"La variable '{nombre}' no existe"
            )

        return entorno[nombre]["valor"]

    if nodo["tipo"] == "BINARY_EXPRESSION":

        operador = nodo["operador"]

        izquierda = gandalf(
            nodo["izquierda"],
            entorno
        )

        derecha = gandalf(
            nodo["derecha"],
            entorno
        )

        comprobar_operacion(
            operador,
            izquierda,
            derecha
        )

        if operador == "+":
            return izquierda + derecha

        if operador == "-":
            return izquierda - derecha

        if operador == "*":
            return izquierda * derecha

        if operador == "/":
            return izquierda / derecha

    if nodo["tipo"] == "COMPARISON_EXPRESSION":

        operador = nodo["operador"]

        izquierda = gandalf(
            nodo["izquierda"],
            entorno
        )

        derecha = gandalf(
            nodo["derecha"],
            entorno
        )

        comprobar_comparacion(
            operador,
            izquierda,
            derecha
        )

        if operador == ">":
            return izquierda > derecha

        if operador == "<":
            return izquierda < derecha

        if operador == ">=":
            return izquierda >= derecha

        if operador == "<=":
            return izquierda <= derecha

        if operador == "==":
            return izquierda == derecha

        if operador == "!=":
            return izquierda != derecha

    if nodo["tipo"] == "VARIABLE_DECLARATION":

        nombre = nodo["nombre"]
        tipo_variable = nodo["variable_tipo"]

        valor = gandalf(
            nodo["valor"],
            entorno
        )

        if not comprobar_tipo(
            tipo_variable,
            valor
        ):

            tipo_recibido = tipo_de_valor(valor)

            raise TypeError(
                f"La variable '{nombre}' es de tipo "
                f"'{tipo_variable}', pero recibió "
                f"un valor de tipo '{tipo_recibido}'"
            )

        if tipo_variable == "elf":
            valor = float(valor)

        entorno[nombre] = {
            "tipo": tipo_variable,
            "valor": valor
        }

        return valor

    if nodo["tipo"] == "VARIABLE_ASSIGNMENT":

        nombre = nodo["nombre"]

        if nombre not in entorno:

            raise Exception(
                f"La variable '{nombre}' no existe"
            )

        valor = gandalf(
            nodo["valor"],
            entorno
        )

        tipo_variable = entorno[nombre]["tipo"]

        if not comprobar_tipo(
            tipo_variable,
            valor
        ):

            tipo_recibido = tipo_de_valor(valor)

            raise TypeError(
                f"La variable '{nombre}' es de tipo "
                f"'{tipo_variable}', pero recibió "
                f"un valor de tipo '{tipo_recibido}'"
            )

        if tipo_variable == "elf":
            valor = float(valor)

        entorno[nombre]["valor"] = valor

        return valor

    if nodo["tipo"] == "IF":

        condicion = gandalf(
            nodo["condicion"],
            entorno
        )

        if type(condicion) is not bool:

            raise TypeError(
                "La condición de MorgothDice "
                "debe producir un valor booleano"
            )

        if condicion:

            return ejecutar_bloque(
                nodo["bloque"],
                entorno
            )

        if nodo["else_bloque"] is not None:

            return ejecutar_bloque(
                nodo["else_bloque"],
                entorno
            )

        return None

    raise Exception(
        f"Gandalf no sabe cómo interpretar este nodo: {nodo}"
    )