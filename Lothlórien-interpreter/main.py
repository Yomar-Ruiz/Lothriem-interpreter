from bilbo import bilbo
from elrond import elrond
from gandalf import gandalf


codigo = """
dwarf gimli = 10

gimli = 25

dwarf resultado = gimli + 5

MorgothDice resultado > 20 {
    hobbit mensaje = "El resultado es mayor que 20"
}
SauronDice {
    hobbit mensaje = "El resultado no es mayor que 20"
}
"""


entorno = {}


tokens = bilbo(codigo)

print("TOKENS:")

for token in tokens:
    print(token)


ast = elrond(tokens)

print("\nAST:")
print(ast)


resultado = gandalf(
    ast,
    entorno
)

print("\nRESULTADO:")
print(resultado)


print("\nENTORNO FINAL:")
print(entorno)