import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os 
load_dotenv()


app_key = os.getenv('APP_KEY')
app_secret = os.getenv('APP_SECRET')
url_produtos = 'https://app.omie.com.br/api/v1/geral/produtos/'
url_ajuste_estoque = 'https://app.omie.com.br/api/v1/estoque/ajuste/'
url_departamento = 'https://app.omie.com.br/api/v1/geral/departamentos/'


class ClasseOmie():

    @staticmethod
    def get_produtos():
        try:
            produtos = []
            pagina = 1
            total_paginas = 1
            while pagina <= total_paginas:
                payload = json.dumps({
                    'call': 'ListarProdutos',
                    'app_key': app_key,
                    'app_secret': app_secret,
                    'param': [
                        {
                            "pagina": pagina,
                            "registros_por_pagina": 500,
                            "apenas_importado_api": "N",
                            "filtrar_apenas_omiepdv": "N",
                            "inativo": "N"
                        }
                    ]
                })
                headers = {'Content-Type': 'application/json'}

                response = requests.post(
                    url=url_produtos, headers=headers, data=payload)
                if response.status_code != 200:
                    raise Exception(
                        f"Erro HTTP ao buscas produtos: {response.status_code}")
                response_data = response.json()
                produtos_da_pagina = response_data.get(
                    "produto_servico_cadastro")

                for dados_produtos in produtos_da_pagina:
                    codigo_produto = dados_produtos['codigo_produto']
                    nome_produto = dados_produtos['descricao']
                    unidade_de_medida = dados_produtos['unidade']
                    valor_produto = dados_produtos["valor_unitario"]

                    dic = {
                        "codigoProduto": codigo_produto,
                        "nomeProduto": nome_produto,
                        "unidadeMedida": unidade_de_medida,
                        "valor": valor_produto
                    }
                    produtos.append(dic)

                    total_paginas = response_data.get("total_de_paginas", 1)
                    pagina += 1
            return produtos

        except Exception as e:
            raise e

    def post_entrada_estoque(cod_produto, quantidade, valor_produto):
        # Obter a data atual
        data_atual = datetime.now()
        # Convertendo para dd/mm/aaaa
        data_hoje = data_atual.strftime('%d/%m/%Y')
        try:
            payload = json.dumps({
                'call': 'IncluirAjusteEstoque',
                'app_key': app_key,
                'app_secret': app_secret,
                'param': [
                    {
                        "id_prod": cod_produto,
                        "data": data_hoje,
                        "quan": quantidade,
                        "obs": "Ajuste feito pela integração",
                        "origem": "PDV",
                        "tipo": "ENT",
                        "motivo": "PDV",
                        "valor": valor_produto,

                    }
                ]
            })

            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                url=url_ajuste_estoque, headers=headers, data=payload)

            if response.status_code != 200:
                print("Falha na requisição:", response.text)
                raise Exception(
                    f'Erro ao fazer movimento de estoque: {response.status_code}')
            return response.json()

        except Exception as e:
            raise e

    def post_saida_estoque(self, cod_produto, quantidade, valor):
        # Obter a data atual
        data_atual = datetime.now()
        # Convertendo para dd/mm/aaaa
        data_hoje = data_atual.strftime('%d/%m/%Y')
        try:
            payload = json.dumps({
                'call': 'IncluirAjusteEstoque',
                'app_key': app_key,
                'app_secret': app_secret,
                'param': [
                    {
                        "id_prod": cod_produto,
                        "data": data_hoje,
                        "quan": quantidade,
                        "obs": "Ajuste feito pela integração",
                        "origem": "PDV",
                        "tipo": "SAI",
                        "motivo": "PDV",
                        "valor": valor,

                    }
                ]
            })
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                url=url_ajuste_estoque, headers=headers, data=payload)
            resposta = response.json()
            print(f'Resposta: {resposta}')
            if response.status_code != 200:
                raise Exception(
                    f'Erro ao fazer movimento de estoque: {response.status_code}')
            status = resposta["descricao_status"]

            return status

        except Exception as e:
            raise e

    @staticmethod
    def get_departamentos():
        try:
            pagina = 1
            total_paginas = 1
            while pagina <= total_paginas:
                payload = json.dumps({
                    'call': 'ListarDepartamentos',
                    'app_key': app_key,
                    'app_secret': app_secret,
                    'param': [
                        {
                            "pagina": pagina,
                            "registros_por_pagina": 500

                        }
                    ]
                })

                headers = {'Content-Type': 'application/json'}
                response = requests.post(
                    url=url_departamento, headers=headers, data=payload)

                if response.status_code != 200:
                    print("Falha na requisição:", response.text)
                    raise Exception(
                        f'Erro ao listar departamentos: {response.status_code}')
                response_data = response.json()
                departamentos = response_data.get("departamentos")

                lista_departamentos = []
                for departamento in departamentos:
                    centroCusto = departamento["descricao"]
                    lista_departamentos.append(centroCusto)

                total_paginas = response_data.get("total_de_paginas", 1)
                pagina += 1
            return lista_departamentos

        except Exception as e:
            raise e