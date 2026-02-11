from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import Dict, Union


class CalculadoraVenda:
    # Tabela de descontos conforme a imagem
    TABELA_CREDIARIO = {1: 0.20, 4: 0.16, 5: 0.12, 7: 0.08, 9: 0.04, 11: 0.00}
    TABELA_CARTAO = {1: 0.20, 4: 0.18, 5: 0.16, 7: 0.14, 9: 0.12, 11: 0.10}
    TAXA_ENTRADA_DINHEIRO = Decimal('0.20')

    @staticmethod
    def processar(
        total_bruto: Union[float, str, Decimal],
        valor_entrada: Union[float, str, Decimal],
        metodo_entrada: str,  # 'dinheiro' ou 'cartao'
        prazo: int,
        tipo_venda: str       # 'crediario' ou 'cartao'
    ) -> Dict:
        try:
            # Conversão segura para Decimal
            total = Decimal(str(total_bruto).replace(',', '.'))
            entrada = Decimal(str(valor_entrada).replace(',', '.'))

            # 1. Validações de Erro
            if total <= 0:
                raise ValueError("O valor total do produto deve ser maior que zero.")
            if entrada < 0:
                raise ValueError("O valor da entrada não pode ser negativo.")
            if entrada > total:
                raise ValueError("A entrada não pode ser maior que o valor total.")

            # Seleção da tabela
            tabela = CalculadoraVenda.TABELA_CREDIARIO if tipo_venda == 'crediario' else CalculadoraVenda.TABELA_CARTAO
            if prazo not in tabela:
                raise ValueError(f"Prazo {prazo}x não encontrado na tabela de taxas.")

            # 2. Cálculos da Entrada
            taxa_e = CalculadoraVenda.TAXA_ENTRADA_DINHEIRO if metodo_entrada == 'dinheiro' else Decimal('0')
            desc_entrada_rs = (entrada * taxa_e).quantize(Decimal('0.01'), ROUND_HALF_UP)

            # 3. Cálculos do Saldo
            saldo_bruto = total - entrada
            taxa_s = Decimal(str(tabela[prazo]))
            desc_saldo_rs = (saldo_bruto * taxa_s).quantize(Decimal('0.01'), ROUND_HALF_UP)

            # 4. Totais e Porcentagens
            total_desc_rs = desc_entrada_rs + desc_saldo_rs
            desc_medio_pct = (total_desc_rs / total * 100).quantize(Decimal('0.01'), ROUND_HALF_UP)

            return {
                "sucesso": True,
                "entrada": {
                    "desconto_rs": float(desc_entrada_rs),
                    "desconto_pct": float(taxa_e * 100)
                },
                "parcelado": {
                    "desconto_rs": float(desc_saldo_rs),
                    "desconto_pct": float(taxa_s * 100),
                    "valor_final_parcelamento": float(saldo_bruto - desc_saldo_rs)
                },
                "total_geral": {
                    "desconto_rs": float(total_desc_rs),
                    "desconto_pct": float(desc_medio_pct)
                }
            }

        except (ValueError, InvalidOperation) as e:
            return {"sucesso": False, "erro": str(e)}
