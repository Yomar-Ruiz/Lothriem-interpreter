def parser_factor(tokens, posicion):

    if posicion >= len(tokens):
        return None, posicion

    token = tokens[posicion]

    if token["tipo"] == "NUMBER":

        valor = float(token["valor"])

        if valor.is_integer():
            valor = int(valor)

        posicion += 1

        return valor, posicion

    if token["tipo"] == "STRING":

        valor = token["valor"]

        posicion += 1

        return valor, posicion

    if token["tipo"] == "BOOLEAN":

        valor = token["valor"] == "true"

        posicion += 1

        return valor, posicion

    if token["tipo"] == "IDENTIFIER":

        nombre = token["valor"]

        posicion += 1

        return {
            "tipo": "IDENTIFIER",
            "nombre": nombre
        }, posicion

    if token["tipo"] == "LEFT_PAREN":

        posicion += 1

        valor, posicion = parser_comparacion(
            tokens,
            posicion
        )

        if valor is None:
            return None, posicion

        if posicion >= len(tokens):
            return None, posicion

        token = tokens[posicion]

        if token["tipo"] != "RIGHT_PAREN":
            return None, posicion

        posicion += 1

        return valor, posicion

    return None, posicion


def parser_termino(tokens, posicion):

    izquierda, posicion = parser_factor(
        tokens,
        posicion
    )

    if izquierda is None:
        return None, posicion

    while posicion < len(tokens):

        token = tokens[posicion]

        if token["tipo"] not in [
            "MULTIPLY",
            "DIVIDE"
        ]:
            break

        operador = token["valor"]

        posicion += 1

        derecha, posicion = parser_factor(
            tokens,
            posicion
        )

        if derecha is None:
            return None, posicion

        izquierda = {
            "tipo": "BINARY_EXPRESSION",
            "operador": operador,
            "izquierda": izquierda,
            "derecha": derecha
        }

    return izquierda, posicion


def parser_expresion(tokens, posicion):

    izquierda, posicion = parser_termino(
        tokens,
        posicion
    )

    if izquierda is None:
        return None, posicion

    while posicion < len(tokens):

        token = tokens[posicion]

        if token["tipo"] not in [
            "PLUS",
            "MINUS"
        ]:
            break

        operador = token["valor"]

        posicion += 1

        derecha, posicion = parser_termino(
            tokens,
            posicion
        )

        if derecha is None:
            return None, posicion

        izquierda = {
            "tipo": "BINARY_EXPRESSION",
            "operador": operador,
            "izquierda": izquierda,
            "derecha": derecha
        }

    return izquierda, posicion


def parser_comparacion(tokens, posicion):

    izquierda, posicion = parser_expresion(
        tokens,
        posicion
    )

    if izquierda is None:
        return None, posicion

    if posicion >= len(tokens):
        return izquierda, posicion

    token = tokens[posicion]

    operadores_comparacion = [
        "GREATER",
        "LESS",
        "GREATER_EQUAL",
        "LESS_EQUAL",
        "EQUAL_EQUAL",
        "NOT_EQUAL"
    ]

    if token["tipo"] not in operadores_comparacion:
        return izquierda, posicion

    operador = token["valor"]

    posicion += 1

    derecha, posicion = parser_expresion(
        tokens,
        posicion
    )

    if derecha is None:
        return None, posicion

    return {
        "tipo": "COMPARISON_EXPRESSION",
        "operador": operador,
        "izquierda": izquierda,
        "derecha": derecha
    }, posicion


def parser_declaracion(tokens, posicion):

    if posicion >= len(tokens):
        return None, posicion

    token = tokens[posicion]

    if token["tipo"] != "TYPE":
        return None, posicion

    tipo_variable = token["valor"]

    posicion += 1

    if posicion >= len(tokens):
        return None, posicion

    token = tokens[posicion]

    if token["tipo"] != "IDENTIFIER":
        return None, posicion

    nombre_variable = token["valor"]

    posicion += 1

    if posicion >= len(tokens):
        return None, posicion

    token = tokens[posicion]

    if token["tipo"] != "EQUAL":
        return None, posicion

    posicion += 1

    valor, posicion = parser_comparacion(
        tokens,
        posicion
    )

    if valor is None:
        return None, posicion

    return {
        "tipo": "VARIABLE_DECLARATION",
        "variable_tipo": tipo_variable,
        "nombre": nombre_variable,
        "valor": valor
    }, posicion


def parser_asignacion(tokens, posicion):

    if posicion >= len(tokens):
        return None, posicion

    token = tokens[posicion]

    if token["tipo"] != "IDENTIFIER":
        return None, posicion

    nombre_variable = token["valor"]

    posicion += 1

    if posicion >= len(tokens):
        return None, posicion

    token = tokens[posicion]

    if token["tipo"] != "EQUAL":
        return None, posicion

    posicion += 1

    valor, posicion = parser_comparacion(
        tokens,
        posicion
    )

    if valor is None:
        return None, posicion

    return {
        "tipo": "VARIABLE_ASSIGNMENT",
        "nombre": nombre_variable,
        "valor": valor
    }, posicion


def parser_bloque(tokens, posicion):

    if posicion >= len(tokens):
        return None, posicion

    token = tokens[posicion]

    if token["tipo"] != "LEFT_BRACE":
        return None, posicion

    posicion += 1

    instrucciones = []

    while posicion < len(tokens):

        token = tokens[posicion]

        if token["tipo"] == "RIGHT_BRACE":

            posicion += 1

            return instrucciones, posicion

        instruccion, nueva_posicion = parser_instruccion(
            tokens,
            posicion
        )

        if instruccion is None:
            return None, posicion

        instrucciones.append(instruccion)

        posicion = nueva_posicion

    return None, posicion


def parser_morgoth_dice(tokens, posicion):

    if posicion >= len(tokens):
        return None, posicion

    token = tokens[posicion]

    if token["tipo"] != "MORGOTH_DICE":
        return None, posicion

    posicion += 1

    condicion, posicion = parser_comparacion(
        tokens,
        posicion
    )

    if condicion is None:
        return None, posicion

    bloque, posicion = parser_bloque(
        tokens,
        posicion
    )

    if bloque is None:
        return None, posicion

    else_bloque = None

    if posicion < len(tokens):

        token = tokens[posicion]

        if token["tipo"] == "SAURON_DICE":

            posicion += 1

            else_bloque, posicion = parser_bloque(
                tokens,
                posicion
            )

            if else_bloque is None:
                return None, posicion

    return {
        "tipo": "IF",
        "condicion": condicion,
        "bloque": bloque,
        "else_bloque": else_bloque
    }, posicion


def parser_instruccion(tokens, posicion):

    if posicion >= len(tokens):
        return None, posicion

    token = tokens[posicion]

    if token["tipo"] == "MORGOTH_DICE":

        return parser_morgoth_dice(
            tokens,
            posicion
        )

    if token["tipo"] == "TYPE":

        return parser_declaracion(
            tokens,
            posicion
        )

    if token["tipo"] == "IDENTIFIER":

        return parser_asignacion(
            tokens,
            posicion
        )

    return None, posicion


def elrond(tokens):

    posicion = 0

    instrucciones = []

    while posicion < len(tokens):

        instruccion, nueva_posicion = parser_instruccion(
            tokens,
            posicion
        )

        if instruccion is None:
            return None

        instrucciones.append(instruccion)

        posicion = nueva_posicion

    return {
        "tipo": "PROGRAM",
        "instrucciones": instrucciones
    }