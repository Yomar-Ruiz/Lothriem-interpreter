def clasificador_token(valor, tipos):

    if valor in tipos:
        return "TYPE"

    if valor.replace(".","", 1).isdigit():
        return "NUMBER"

    if valor == "true" or valor == "false":
        return "BOOLEAN"

    return "IDENTIFIER"

def bilbo(codigo):
    tokens = []
    dentro_de_texto = False
    actual = ""

    tipos = ["hobbit", "dwarf", "elf", "orc"]

    operadores = {
        "=": "EQUAL",
        "-": "MINUS",
        "+": "PLUS",
        "*": "MULTIPLY",
        "/": "DIVIDE"
    }

    for caracter in codigo:
        if caracter == '"':
            dentro_de_texto = not dentro_de_texto

            if not dentro_de_texto:
                tokens.append({
                    "tipo": "STRING",
                    "valor": actual
                })

                actual = ""

            continue

        if caracter == " " and not dentro_de_texto:

            if actual:

                tipo = clasificador_token(actual, tipos)

                tokens.append({
                    "tipo": tipo,
                    "valor": actual
                })

                actual = ""
            continue

        if caracter in operadores and not dentro_de_texto:

            if actual:
                tipo = clasificador_token(actual, tipos)

                tokens.append({
                    "tipo": tipo,
                    "valor": actual
                })
                actual = ""

            tokens.append({
                "tipo": operadores[caracter],
                "valor": caracter
            })
            continue

        else:
            actual += caracter

    if actual:
        tipo = clasificador_token(actual, tipos)
        tokens.append({
            "tipo": tipo,
            "valor": actual
        })
        
    return tokens