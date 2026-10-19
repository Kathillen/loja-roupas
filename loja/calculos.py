frete_fixo = 15.0
frete_gratis_a_partir_de = 200.0

def total_carrinho(itens):
    #recebe uma lista de preço e quantidade e retorna o total
    total = 0 
    for preco, quantidade in itens:
        total = total + preco * quantidade
    return total

def frete(valor_compra):
    ## calcula se a compra vai receber um desconto no frete
    if valor_compra >= frete_gratis_a_partir_de:
        return 0.0
    return frete_fixo