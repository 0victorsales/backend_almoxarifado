from flask import jsonify, request, send_from_directory
import os
import base64
from settings import app
from src.classes.ClasseOmie import ClasseOmie
from src.classes.ClasseGerarPdf import GerarPdf
from flask_cors import CORS

CORS(app)

omie_metodos = ClasseOmie()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')



@app.route('/departamentos')
def listar_departamentos():
    return omie_metodos.get_departamentos()


@app.route('/produtos')
def listar_produtos():
    produtos = omie_metodos.get_produtos()
    departamentos = omie_metodos.get_departamentos()
    lista_produtos = []
    for produto in produtos:
        codigoProduto = produto["codigoProduto"]
        nomeProduto = produto["nomeProduto"]
        unidadeMedida = produto["unidadeMedida"]
        valor = produto["valor"]
        dic = {
            "codigoProduto": codigoProduto,
            "nomeProduto": nomeProduto,
            "unidadeMedida": unidadeMedida,
            "valor": valor,
            "centroCusto": departamentos
        }
        lista_produtos.append(dic)
    return jsonify(lista_produtos)


@app.route('/pdf-solicitacao', methods=['POST'])
def gerar_pdf_solicitacao():
    dados_usuario = request.json
    print(dados_usuario)
    origem = 'pdf-solicitacao'
    buffer = GerarPdf.gerar_pdf(dados_usuario, origem)
    pdf_content = buffer.getvalue()
    pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
    return jsonify({'pdfBase64': pdf_base64})


@app.route('/pdf-devolucao', methods=['POST'])
def gerar_pdf_devolucao():
    dados_usuario = request.json
    origem = 'pdf-devolucao'
    buffer = GerarPdf.gerar_pdf(dados_usuario, origem)
    pdf_content = buffer.getvalue()
    pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
    return jsonify({'pdfBase64': pdf_base64})

