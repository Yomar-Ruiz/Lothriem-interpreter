def gandalf(codigo):

    if codigo.startswith("say"):
        codigo = codigo.removeprefix("say").strip().strip('"')

    elif codigo.startswith("Hobbit"):
        partes = codigo.split()
        print(partes)