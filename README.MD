# Documentação BACKEND SISTEMA DE ALMOXARIFADO

## Descrição
Este projeto Flask fornece uma API para acessar dados de departamentos, produtos e gerar PDFs de solicitações e devoluções. Ele interage com a API da plataforma Omie para obter os dados de produtos e departamentos, além de gerar os PDFs com base nos dados fornecidos.

## Estrutura do Projeto
O projeto é estruturado da seguinte forma:

- `app.py`: Contém as rotas e a configuração do aplicativo Flask.
- `ClasseOmie.py`: Classe para interagir com a API da Omie para obter dados de produtos e departamentos.
- `GerarPdf.py`: Classe para gerar PDFs com base nos dados fornecidos.
- `GerarLayoutPdf.py`: Classe para definir o layout do PDF com base nos dados fornecidos.
- `utils.py`: Funções utilitárias para formatação de valores, limitação de tamanho de texto, etc.

## Rotas

1. **Rota Padrão**:
   - **Método**: GET
   - **Endpoint**: `/`
   - **Descrição**: Rota padrão que serve os arquivos estáticos do frontend.

2. **Listar Departamentos**:
   - **Método**: GET
   - **Endpoint**: `/departamentos`
   - **Descrição**: Retorna uma lista de departamentos.

3. **Listar Produtos**:
   - **Método**: GET
   - **Endpoint**: `/produtos`
   - **Descrição**: Retorna uma lista de produtos com detalhes, incluindo código do produto, nome, unidade de medida, valor e centro de custo associado.

4. **Gerar PDF de Solicitação**:
   - **Método**: POST
   - **Endpoint**: `/pdf-solicitacao`
   - **Descrição**: Gera um PDF de solicitação com base nos dados fornecidos no corpo da solicitação. Retorna o PDF codificado em base64.

5. **Gerar PDF de Devolução**:
   - **Método**: POST
   - **Endpoint**: `/pdf-devolucao`
   - **Descrição**: Gera um PDF de devolução com base nos dados fornecidos no corpo da solicitação. Retorna o PDF codificado em base64.

## Dependências
- Flask
- Flask-Cors
- ReportLab

## Execução do Projeto
1. Certifique-se de que todas as dependências estão instaladas. Você pode instalar as dependências listadas no arquivo `requirements.txt` usando `pip install -r requirements.txt`.
2. Execute o aplicativo Flask usando `python run.py`.
3. O aplicativo estará disponível em `http://localhost:5000`.

## Configurações Adicionais
Certifique-se de configurar as variáveis de ambiente necessárias para a autenticação com a API da Omie (`APP_KEY` e `APP_SECRET`).


