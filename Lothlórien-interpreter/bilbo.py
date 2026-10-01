def clasificar_token(valor, tipos):

    if valor in tipos:
        return "TYPE"

    if valor == "true" or valor == "false":
        return "BOOLEAN"

    if valor.replace(".", "", 1).isdigit():
        return "NUMBER"

    if valor == "MorgothDice":
        return "MORGOTH_DICE"

    if valor == "SauronDice":
        return "SAURON_DICE"

    return "IDENTIFIER"


def bilbo(codigo):

    tokens = []
    actual = ""
    dentro_de_texto = False

    tipos = [
        "hobbit",
        "dwarf",
        "elf",
        "orc"
    ]

    operadores = {
        "=": "EQUAL",
        "-": "MINUS",
        "+": "PLUS",
        "*": "MULTIPLY",
        "/": "DIVIDE",
        "(": "LEFT_PAREN",
        ")": "RIGHT_PAREN",
        "{": "LEFT_BRACE",
        "}": "RIGHT_BRACE",
        ">": "GREATER",
        "<": "LESS",
        ">=": "GREATER_EQUAL",
        "<=": "LESS_EQUAL",
        "==": "EQUAL_EQUAL",
        "!=": "NOT_EQUAL"
    }

    caracteres = list(codigo)

    posicion = 0

    while posicion < len(caracteres):

        caracter = caracteres[posicion]

        if caracter == '"':

            dentro_de_texto = not dentro_de_texto

            if not dentro_de_texto:

                tokens.append({
                    "tipo": "STRING",
                    "valor": actual
                })

                actual = ""

            posicion += 1
            continue

        if caracter.isspace() and not dentro_de_texto:

            if actual:

                tipo = clasificar_token(
                    actual,
                    tipos
                )

                tokens.append({
                    "tipo": tipo,
                    "valor": actual
                })

                actual = ""

            posicion += 1
            continue

        if not dentro_de_texto:

            operador = None

            if posicion + 1 < len(caracteres):

                dos_caracteres = (
                    caracteres[posicion]
                    + caracteres[posicion + 1]
                )

                if dos_caracteres in operadores:

                    operador = dos_caracteres

            if operador is not None:

                if actual:

                    tipo = clasificar_token(
                        actual,
                        tipos
                    )

                    tokens.append({
                        "tipo": tipo,
                        "valor": actual
                    })

                    actual = ""

                tokens.append({
                    "tipo": operadores[operador],
                    "valor": operador
                })

                posicion += 2
                continue

            if caracter in operadores:

                if actual:

                    tipo = clasificar_token(
                        actual,
                        tipos
                    )

                    tokens.append({
                        "tipo": tipo,
                        "valor": actual
                    })

                    actual = ""

                tokens.append({
                    "tipo": operadores[caracter],
                    "valor": caracter
                })

                posicion += 1
                continue

        actual += caracter

        posicion += 1

    if actual:

        tipo = clasificar_token(
            actual,
            tipos
        )

        tokens.append({
            "tipo": tipo,
            "valor": actual
        })

    return tokens