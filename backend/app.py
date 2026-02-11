"""
API da Calculadora de Desconto - Grupo G5.
Validação final com Decimal (cálculos financeiros precisos).
"""
import os
from flask import Flask, request, jsonify, send_from_directory

from calculadora import CalculadoraVenda

# Raiz do projeto (pasta acima de backend/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

app = Flask(__name__, static_folder=ROOT_DIR, static_url_path='')


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/calcular', methods=['POST'])
def calcular():
    data = request.get_json(force=True, silent=True) or {}
    total_bruto = data.get('total_bruto')
    valor_entrada = data.get('valor_entrada')
    metodo_entrada = data.get('metodo_entrada', 'dinheiro')
    prazo = data.get('prazo')
    tipo_venda = data.get('tipo_venda', 'crediario')

    if total_bruto is None or valor_entrada is None or prazo is None:
        return jsonify({
            "sucesso": False,
            "erro": "Faltam dados: total_bruto, valor_entrada e prazo são obrigatórios."
        }), 400

    try:
        prazo = int(prazo)
    except (TypeError, ValueError):
        return jsonify({"sucesso": False, "erro": "Prazo deve ser um número inteiro."}), 400

    resultado = CalculadoraVenda.processar(
        total_bruto=total_bruto,
        valor_entrada=valor_entrada,
        metodo_entrada=metodo_entrada,
        prazo=prazo,
        tipo_venda=tipo_venda
    )

    status = 200 if resultado.get('sucesso') else 400
    return jsonify(resultado), status


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
