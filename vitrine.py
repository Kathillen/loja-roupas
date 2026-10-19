# Lista: coleção que você pode modificar.  []
# Tupla: coleção que não pode ser modificada. ()
# Dicionário: coleção que organiza informações por chave e valor. {}

# Característica	        Lista	       Tupla	    Dicionário
# Sintaxe	                []	           ()	        {}
# Mutável?	            Sim 	       Não	        Sim
# Permite repetidos?      Sim	           Sim	        Chaves não
# Acesso	                Índice	       Índice	    Chave
# Exemplo	            ["a", "b"]	       ("a", "b")	{"nome": "Ana"}


#tupla

tamanhos = ("pp", "p", "m", "g", "gg" ) # tuplas sao imutaveis diferente das listas que podem ser alteradas a qualquer momento 

# lista  de dicionario 

vitrine = [
    {"nome": "camiseta basica", "preco": 39.90, "tamanho": "m"},
    {"nome": "calca jeans", "preco": 129.90, "tamanho": "g"},
    {"nome": "moletom", "preco": 159.90, "tamanho": "p"},
]

# Lista de pares com nome do item e a quantidade

carrinho = [("camiseta basica", 3), ("Calca jeans", 1)]

# dicionário: nome -> preço
precos = {}
for produto in vitrine:
    precos[produto["nome"]] = produto["preco"]

total = 0
for nome, quantidade in carrinho:
    total = total + precos[nome] * quantidade

print("Peças na vitrine:", len(vitrine)) # len é pra mostrar a quantidade de items .length
print("Total do carrinho: R$", round(total, 2)) # deixa o resultado com precisão de duas casas decimais, como normalmente usamos para representar valores em reais.