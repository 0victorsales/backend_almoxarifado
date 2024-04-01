from src.servicos.LayoutPdf import GerarLayoutPdf

class GerarPdf():
    @staticmethod
    def gerar_pdf(dados_usuario, origem):
        layout_pdf = GerarLayoutPdf.layout_pdf(dados_usuario, origem)
        return layout_pdf
    