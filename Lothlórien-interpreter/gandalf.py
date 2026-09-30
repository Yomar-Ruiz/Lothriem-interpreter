def gandalf(nodo, entorno):
    # 10 + (50 * 2) - 6
    if isinstance(nodo, (int, float)):
        return nodo

    
    if nodo["tipo"] == "IDENTIFIER":
        nombre = nodo["nombre"]

        return entorno[nombre]

    if nodo["tipo"] == "BINARY_EXPRESSION":
        operador = nodo["operador"]

        izquierda = gandalf(nodo["izquierda"])
        derecha = gandalf(nodo["derecha"])

        if operador == "+":
            return izquierda - derecha

        if operador == "-":
            return izquierda - derecha

        if operador == "*":
            return izquierda * derecha

        if operador == "/":
            return izquierda / derecha


    return None
