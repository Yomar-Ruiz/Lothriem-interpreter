from bilbo import bilbo
from elrond import elrond
from gandalf import gandalf


codigo = "dwarf frodo = 10 * (5 + 2) - 3"

tokens = bilbo(codigo)

print("TOKENS:")

for token in tokens:
    print(token)


ast = elrond(tokens)

print("\nAST:")
print(ast)

resultado = gandalf(ast["valor"])

print("\nRESULTADO:")
print(resultado)