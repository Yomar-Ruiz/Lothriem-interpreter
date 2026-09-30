def parser_factor(tokens, posicion):

    token = tokens[posicion]

    if token["tipo"] == "NUMBER":

        valor = float(token["valor"])

        if valor.is_integer():
            valor = int(valor)

        posicion += 1
        
        return valor, posicion

    if token["tipo"] == "LEFT_PAREN":

        posicion += 1

        valor, posicion = parser_expresion(tokens, posicion)

        if valor is None:
            return None, posicion

        if posicion >= len(tokens):
            return None, posicion

        token = tokens[posicion]

        if token["tipo"] != "RIGHT_PAREN":
            return None, posicion

        posicion += 1

        return valor, posicion

    if token["tipo"] == "IDENTIFIER":
        nombre = token["valor"]
        posicion += 1

        return {
            "tipo": "IDENTIFIER",
            "nombre": nombre
        }, posicion

    return None, posicion


def parser_termino(tokens, posicion):

    izquierda, posicion = parser_factor(tokens, posicion)

    if izquierda is None:
        return None, posicion

    while posicion < len(tokens):

        token = tokens[posicion]

        if token["tipo"] not in ["MULTIPLY", "DIVIDE"]:
            break

        operador = token["valor"]

        posicion += 1

        derecha, posicion = parser_factor(tokens, posicion)

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

    izquierda, posicion = parser_termino(tokens, posicion)

    if izquierda is None:
        return None, posicion

    while posicion < len(tokens):

        token = tokens[posicion]

        if token["tipo"] not in ["PLUS", "MINUS"]:
            break

        operador = token["valor"]

        posicion += 1

        derecha, posicion = parser_termino(tokens, posicion)

        if derecha is None:
            return None, posicion

        izquierda = {
            "tipo": "BINARY_EXPRESSION",
            "operador": operador,
            "izquierda": izquierda,
            "derecha": derecha
        }

    return izquierda, posicion


def elrond(tokens):

    posicion = 0


    token = tokens[posicion]

    if token["tipo"] != "TYPE":
        return None

    tipo_variable = token["valor"]

    posicion += 1


    token = tokens[posicion]

    if token["tipo"] != "IDENTIFIER":
        return None

    nombre_variable = token["valor"]

    posicion += 1

    token = tokens[posicion]

    if token["tipo"] != "EQUAL":
        return None

    posicion += 1

    valor, posicion = parser_expresion(tokens, posicion)

    if valor is None:
        return None

    ast = {
        "tipo": "VARIABLE_DECLARATION",
        "variable_tipo": tipo_variable,
        "nombre": nombre_variable,
        "valor": valor
    }

    return ast