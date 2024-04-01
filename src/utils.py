import locale



locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def converter_valor_item(valor_float):
    """
        Formata o número float para duas casas decimais com separador de milhar e converte para string
        Usando format() com nformat() para aplicar o locale
    """

    # Formata o número float para duas casas decimais com separador de milhar e converte para string
    valor_string = locale.format_string("R$ %.2f", valor_float, grouping=True)
    return valor_string




def limitar_nome_produto(produto, limite=50):

    produto_limitado = produto[:limite]
    if len(produto) > limite and produto[limite] != ' ' and produto_limitado[-1] != ' ':
        ultima_palavra_completa = produto_limitado.rsplit(' ', 1)[0]
        return ultima_palavra_completa + '.'
    else:
        return produto_limitado


def lim_tamanho_centro_custo(produto, limite=16):
    # Ajusta o limite para 16 e remove espaços no final se necessário
    produto_limitado = produto[:limite].rstrip()
    return produto_limitado

def configurar_email(email):
    nome_usuario = email.split('@')[0]
    return nome_usuario