# Calculadora de Desconto 

Sistema de cálculo de descontos e parcelamentos para PDV. Divide a venda em **entrada** e **saldo parcelado**, aplica percentuais conforme tabela de prazos e forma de pagamento, e exibe total de desconto e desconto médio.

---

## Estrutura do projeto

```
Calculadora-Desconto/
  backend/
    app.py          # API Flask (rota /api/calcular e servir estáticos)
    calculadora.py  # Regras de negócio (Decimal, tabelas)
  index.html        # Interface única
  style.css         # Estilos (paleta #4d7031 e branco)
  script.js         # Formulário, chamada à API e exibição dos resultados
  requirements.txt  # Flask
```

O frontend é estático (HTML/CSS/JS). O backend serve `index.html` na raiz e expõe a API em `/api/calcular`.

---

## Como rodar

1. Instalar dependências (Python 3):

   ```bash
   pip install -r requirements.txt
   ```

2. Subir o servidor a partir da raiz do projeto:

   ```bash
   python backend/app.py
   ```

3. Abrir no navegador: `http://127.0.0.1:5000/`

O app roda só no backend: a mesma origem serve a página e a API. Não é necessário servidor separado para o front.

---

## API

**POST /api/calcular**

Corpo (JSON):

| Campo           | Tipo   | Obrigatório | Descrição                                      |
|----------------|--------|-------------|------------------------------------------------|
| total_bruto    | number/string | Sim   | Valor total do produto                         |
| valor_entrada   | number/string | Sim   | Valor pago de entrada                          |
| metodo_entrada | string | Não (default: dinheiro) | `dinheiro` ou `cartao`              |
| prazo          | int    | Sim         | Número de parcelas: 1, 4, 5, 7, 9 ou 11        |
| tipo_venda     | string | Não (default: crediario) | `crediario` ou `cartao` (parcelado) |

Valores numéricos aceitam vírgula ou ponto como decimal.

Resposta de sucesso (200):

```json
{
  "sucesso": true,
  "entrada": {
    "desconto_rs": 40.0,
    "desconto_pct": 20.0
  },
  "parcelado": {
    "desconto_rs": 32.0,
    "desconto_pct": 4.0,
    "valor_final_parcelamento": 768.0
  },
  "total_geral": {
    "desconto_rs": 72.0,
    "desconto_pct": 7.2
  }
}
```

Em erro de validação ou cálculo (400): `{ "sucesso": false, "erro": "mensagem" }`.

---

## Lógica dos descontos

### Tabela de prazos

O percentual de desconto depende do **prazo** (parcelas) e do **tipo de venda** (crediário ou cartão):

| Prazo  | Crediário | Cartão |
|--------|-----------|--------|
| À vista / 1x | 20% | 20% |
| 4x     | 16% | 18% |
| 5x     | 12% | 16% |
| 7x     | 8%  | 14% |
| 9x     | 4%  | 12% |
| 11x    | 0%  | 10% |

No código, as tabelas estão em `CalculadoraVenda.TABELA_CREDIARIO` e `TABELA_CARTAO` em `backend/calculadora.py`.

### Componentes do cálculo

1. **Desconto da entrada (à vista)**  
   - Se a entrada for **Dinheiro, Pix ou Débito:**  
     `Valor_Entrada * 20%`  
   - Se a entrada for **Cartão:** desconto da entrada = 0 (Valor Desc. à Vista = R$ 0,00).

2. **Saldo parcelado**  
   - Total do parcelamento: `Valor_Produtos - Valor_Entrada`  
   - Desconto do parcelado: `Total_do_Parcelamento * taxa_da_tabela`, onde a taxa é a da coluna Crediário ou Cartão conforme o `tipo_venda` e o `prazo` escolhidos.  
   - Valor final do parcelamento (líquido): `Total_do_Parcelamento - Desconto_do_Parcelado`.

3. **Resumo**  
   - Total Desconto R$: `Desconto_da_Entrada + Valor_Desc._Parcelado`  
   - Desconto Médio %: `(Total_Desconto_R$ / Valor_Produtos) * 100`

Exemplo: produto R$ 1.000,00, entrada R$ 200,00 em dinheiro, 9x crediário (4%).  
- Desconto entrada: 200 * 20% = R$ 40,00.  
- Total parcelamento: 1.000 - 200 = R$ 800,00.  
- Desconto parcelado: 800 * 4% = R$ 32,00.  
- Total desconto: 40 + 32 = R$ 72,00.  
- Desconto médio: (72 / 1.000) * 100 = 7,20%.

---

## Backend (Python)

- **Flask**: servidor HTTP, rota `/` para `index.html` e `POST /api/calcular` para o cálculo.  
- **calculadora.py**: uso de `Decimal` e `ROUND_HALF_UP` para evitar erro de ponto flutuante em valores monetários. Valida totais, entrada, prazo e tipo de venda e retorna um único dicionário com entrada, parcelado e total_geral.

---

## Frontend

- **HTML**: formulário (valor do produto, valor da entrada, forma de pagamento da entrada, prazo, tipo de venda), blocos de resultado (entrada, à vista, crediário, cartão, resumo) e tabela de prazos em referência.  
- **CSS**: layout responsivo, paleta em torno de verde `#4d7031` e branco, sem dependências externas.  
- **JavaScript**: submissão do formulário, `fetch` para `POST /api/calcular`, formatação de moeda e percentual e atualização dos elementos de resultado; exibição de mensagem de erro em caso de falha da API ou validação.

---

## Licença

Conforme arquivo LICENSE no repositório.
