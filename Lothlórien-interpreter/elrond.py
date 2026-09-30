def parser_factor(tokens, posicion):
    token = tokens[posicion]

    if token["tipo"] != "NUMBER":
        return None, posicion

    valor = float(token["valor"])

    if valor.is_integer():
        valor = int(valor)

    posicion += 1

    return valor, posicion

def parser_termino(tokens, posicion):
    left, posicion = parser_factor(tokens, posicion)

    if left is None:
        return None,posicion

    while posicion < len(tokens):
        token = tokens[posicion]
        if token["tipo"] not in ["MULTIPLY", "DIVIDIR"]:
            break

        operdor = token["valor"]

        posicion += 1

        derecha, posicion = parser_factor(tokens, posicion)

        if derecha is None:
            return None, posicion

        izquierda = {
            "tipo": "BINARY_EXPRESSION",
            "operador": operdor,
            "izuiquierda": left,
            "derecha": derecha
        }
        return izquierda, posicion

    