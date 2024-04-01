from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from src import utils
from datetime import datetime
from src.utils import limitar_nome_produto, lim_tamanho_centro_custo, configurar_email
data_hoje = datetime.now()
data_hoje_formatado = data_hoje.strftime('%d/%m/%Y')



class GerarLayoutPdf():
    
    @staticmethod
    def layout_pdf(dados_usuario, origem):
        buffer = BytesIO()
        pagesize = letter[1], letter[0]
        c = canvas.Canvas(buffer, pagesize=pagesize)
        width, height = pagesize

        # FIXME - MOCK DADOS
        num_reqisicao = ""

        # NOTE - Cabeçalho
        def cabecalho(num_reqisicao, data_hoje_formatado, solicitante):
            solicitacao = 'Requisição de Produtos ao Almoxarifado'
            devolucao = 'Devolução de Produtos ao Almoxarifado'
            logo_path = '' 
            logo_width = 70
            logo_height = 70
           
            c.drawImage(logo_path, 40, height - logo_height - 23, width=logo_width, height=logo_height) 

            # vertical direita
            c.setLineWidth(0.2)
            c.line(115, height - 20, 115, 92)
            c.line(500, height - 20, 500, 182)
            c.line(580, height - 20, 580, 152)
            c.line(640, height - 45, 640, 542)
            c.line(690, height - 45, 690, 542)
            # horizontal
            c.line(500, height - 45, width - 28, height - 45)
            c.line(500, height - 70, width - 28, height - 70)
            c.line(25, height - 95, width - 28, height - 95)

            # Definindo as coordenadas e dimensões do retângulo
            x = 25
            y = height - 520
            rect_width = 740
            rect_height = 500
            # Desenha o retângulo sem preenchimento
            c.rect(x, y, rect_width, rect_height, fill=0)

            # CONFIGURANDO LETRAS E FONTES
            c.setFont("Helvetica-Bold", 16)
            if origem == 'pdf-solicitacao':
                c.drawString(145, height - 60, f"{solicitacao}")
            else:
                c.drawString(145, height - 60, f"{devolucao}")
            c.setFont("Helvetica", 8)
            c.drawString(505, height - 35, "Nº da Requisição")
            c.drawString(505, height - 60, "Data da emissão")
            c.drawString(650, height - 60, "Página")
            c.setFont("Helvetica", 9)
            c.drawString(505, height - 85, "Solicitante")
            c.setFont("Helvetica", 12)

            # variaveis
            c.setFont("Helvetica-Bold", 9)
            c.drawString(585, height - 35, f"{num_reqisicao}")
            c.drawString(585, height - 60, f"{data_hoje_formatado}")
            # c.drawString(720, height - 60, f"{num_pagina}")
            c.drawString(585, height - 85, f"{solicitante}")

        # NOTE - Titulo
        def titulo():
            # horizontal
            c.setLineWidth(0.2)
            c.line(25, height - 140, width - 28, height - 140)
            c.line(415, height - 122, width - 292, height - 122)
            # vertical
            c.line(60, height - 95, 60, 182)
            c.line(370, height - 95, 370, 182)
            c.line(415, height - 95, 415, 182)
            c.line(640, height - 95, 640, 152)
            c.line(455, height - 122, 455, 182)
            c.line(710, height - 95, 710, 182)

            # CONFIGURANDO LETRAS E FONTES
            c.setFont("Helvetica", 10)
            c.drawString(32, height - 120, "Item")
            c.drawString(70, height - 120, "Código")
            c.drawString(220, height - 120, "Descrição")
            c.drawString(385, height - 120, "Un")
            c.drawString(428, height - 113, "Quantidade")
            c.setFont("Helvetica", 7)
            c.drawString(420, height - 134, "Solicitada")
            c.drawString(463, height - 134, "Atendida")
            c.setFont("Helvetica", 9)
            c.drawString(505, height - 120, "Centro de Custo")
            c.drawString(590, height - 120, "Autorizado")
            c.drawString(648, height - 120, "Valor Unitário")
            c.drawString(715, height - 120, "Valor Total")

        # NOTE - Footer
        def footer():
            # horizontal
            c.setLineWidth(0.2)
            c.line(25, height - 430, width - 28, height - 430)
            c.line(25, height - 460, width - 28, height - 460)
            # vertical
            c.line(270, height - 430, 270, 152)
            c.line(350, height - 430, 350, 152)

            # CONFIGURANDO LETRAS E FONTES
            c.setFont("Helvetica", 9)
            c.drawString(32, height - 450, "Separado por")
            c.drawString(280, height - 450, "Entregue por")
            c.drawString(587, height - 450, "Valor Total")
            c.drawString(32, height - 495, "Observação")
            c.setFont("Helvetica", 11)
            c.drawString(
                32, height - 570, "Salvador,          /                /                 . ")
            c.drawString(470, height - 570,
                            "__________________________________________ ")
            c.setFont("Helvetica-Bold", 6)
            c.drawString(570, height - 580, "Assinatura do Recebedor")
            c.setFont("Helvetica", 11)

        buffer = BytesIO()
        pagesize = letter[1], letter[0]
        c = canvas.Canvas(buffer, pagesize=pagesize)
        width, height = pagesize

        # FIXME - MOCK DADOS
        num_reqisicao = ""

        
        # NOTE - Adicionando itens no corpo do pdf
        valor_total_solicitacao = 0
        y_pos = height - 155
       
        dados = dados_usuario["dadosSolicitacao"]
        produtos = dados["produtos"]
        email_solicitante = dados["nomeUsuario"]
        email_solicitante_abreviado = configurar_email(email_solicitante)
        nome_solicitante = email_solicitante_abreviado #FIXME - Alterar modo de obter email do usuario
        try:
            observacao = dados["observacao"]
        except:
            pass
        
        if len(produtos) > 14:

            # Calcula o número de páginas necessárias
            num_paginas = len(produtos) // 14 + \
                (1 if len(produtos) % 14 else 0)
            indice_item = 1
            for pagina_atual in range(num_paginas):
                if pagina_atual > 0:
                    c.showPage()

                c.drawString(720, height - 60, f"{pagina_atual + 1}")

                # Define a posição inicial para os produtos na página atual
                y_pos = height - 155

                # Calcula o índice inicial e final dos produtos para a página atual
                inicio = pagina_atual * 14
                fim = inicio + 14 if inicio + \
                    14 < len(produtos) else len(produtos)

                for produto in produtos[inicio:fim]:
                    c.setFont("Helvetica-Bold", 9)
                    nome_produto_completo = produto["nomeProduto"]
                    centro_custo_completo = produto["centroCusto"]
                    codigo_produto = produto["codigoProduto"]
                    unidade_medida = produto["unidadeMedida"]
                    valor_produto = produto["valor"]
                    quantidade = produto["quantidade"]
                    
                    centro_custo = lim_tamanho_centro_custo(centro_custo_completo)
                    nome_produto = limitar_nome_produto(nome_produto_completo)

                    c.drawString(40, y_pos, f'{indice_item}')
                    c.drawString(63, y_pos, str(codigo_produto))
                    c.drawString(120, y_pos, str(nome_produto))
                    c.drawString(385, y_pos, str(unidade_medida))
                    c.drawString(430, y_pos, str(quantidade))
                    c.drawString(505, y_pos, str(centro_custo))
                    valor_produto_convertido = utils.converter_valor_item(
                        valor_produto)
                    c.drawString(650, y_pos, str(valor_produto_convertido))
                    valor_total_item = valor_produto * quantidade
                    valor_total_item_convertido = utils.converter_valor_item(valor_total_item)
                    c.drawString(712, y_pos, str(valor_total_item_convertido))
                    valor_total_solicitacao = valor_total_solicitacao + valor_total_item
                    indice_item += 1

                    y_pos -= 20

                # NOTE - Chamando funções
                cabecalho(num_reqisicao, data_hoje_formatado, nome_solicitante)
                titulo()
                footer()

            if origem == 'pdf-devolucao':
                utils.drawString_wrapped(c, 120, height - 475, observacao)

            c.setFont("Helvetica-Bold", 9)
            valor_total_solicitacao_convertido = utils.converter_valor_item(valor_total_solicitacao)
            c.drawString(645, height - 450, f"{valor_total_solicitacao_convertido}") 

        else:
            # NOTE - Chamando funções
            cabecalho(num_reqisicao, data_hoje_formatado, nome_solicitante)
            titulo()
            footer()
            c.drawString(720, height - 60, "1")

            # Se todos os produtos couberem em uma única página
            c.setFont("Helvetica-Bold", 9)
            y_pos = height - 155
            indice_item = 1
            for produto in produtos:
                nome_produto_completo = produto["nomeProduto"]
                centro_custo_completo = produto["centroCusto"]
                codigo_produto = produto["codigoProduto"]
                unidade_medida = produto["unidadeMedida"]
                valor_produto = produto["valor"]
                quantidade = produto["quantidade"]

                centro_custo = lim_tamanho_centro_custo(centro_custo_completo)
                nome_produto = limitar_nome_produto(nome_produto_completo)

                c.setFont("Helvetica", 9)
                c.drawString(40, y_pos, f'{indice_item}')
                c.drawString(63, y_pos,str(codigo_produto))
                c.drawString(120, y_pos, str(nome_produto))
                c.drawString(385, y_pos, str(unidade_medida))
                c.drawString(430, y_pos, str(quantidade))
                c.drawString(505, y_pos, str(centro_custo))
                valor_produto_convertido = utils.converter_valor_item(
                    valor_produto)
                c.drawString(650, y_pos, str(valor_produto_convertido))
                valor_total_item = valor_produto * quantidade
                valor_total_item_convertido = utils.converter_valor_item(
                    valor_total_item)
                c.drawString(712, y_pos, str(valor_total_item_convertido))
                valor_total_solicitacao = valor_total_solicitacao + valor_total_item
                indice_item += 1
                y_pos -= 20

            c.setFont("Helvetica-Bold", 9)
            valor_total_solicitacao_convertido = utils.converter_valor_item(valor_total_solicitacao)
            c.drawString(645, height - 450, f"{valor_total_solicitacao_convertido}")
            c.setFont("Helvetica", 11)
            if origem == 'pdf-devolucao':
                utils.drawString_wrapped(c, 120, height - 475, observacao)

        # Finaliza o PDF
        c.save()

        # Move o ponteiro do buffer para o início do buffer
        buffer.seek(0)

        return buffer