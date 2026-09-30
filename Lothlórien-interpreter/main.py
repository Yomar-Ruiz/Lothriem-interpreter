from bilbo import bilbo
from elrond import elrond

codigo =  'dwarf deuda = 1000 + 100'

tokens = bilbo(codigo)

ast = elrond(tokens)

print(ast)