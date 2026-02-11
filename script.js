/**
 * Calculadora de Vendas - Grupo G5
 * Integração com backend Python (Decimal, tabelas de desconto).
 */

var API_URL = '/api/calcular';

function formatCurrency(value) {
  if (value === null || value === undefined || isNaN(value)) return 'R$ 0,00';
  return 'R$ ' + Number(value).toFixed(2).replace('.', ',');
}

function formatPercent(value) {
  if (value === null || value === undefined || isNaN(value)) return '0%';
  return Number(value).toFixed(2).replace('.', ',') + '%';
}

function parseDecimal(str) {
  if (str === null || str === undefined) return '';
  var s = String(str).trim().replace(',', '.');
  return s;
}

function mostrarErro(msg) {
  var el = document.getElementById('erro');
  el.textContent = msg;
  el.hidden = false;
}

function esconderErro() {
  document.getElementById('erro').hidden = true;
}

function preencherZeros() {
  document.getElementById('displayEntry').textContent = 'R$ 0,00';
  document.getElementById('displayDiscCash').textContent = '0%';
  document.getElementById('displayCashDiscountValue').textContent = 'R$ 0,00';
  document.getElementById('displayDiscInstallment').textContent = '0%';
  document.getElementById('displayInstallmentDiscountValue').textContent = 'R$ 0,00';
  document.getElementById('displayTotalInstallment').textContent = 'R$ 0,00';
  document.getElementById('displayDiscCredit').textContent = '0%';
  document.getElementById('displayCreditCardDiscountValue').textContent = 'R$ 0,00';
  document.getElementById('displayTotalCreditCard').textContent = 'R$ 0,00';
  document.getElementById('displayTotalDiscount').textContent = 'R$ 0,00';
  document.getElementById('displayAverageDiscount').textContent = '0%';
}

function aplicarResultado(res, entradaStr) {
  var entrada = parseFloat(parseDecimal(entradaStr)) || 0;

  document.getElementById('displayEntry').textContent = formatCurrency(entrada);
  document.getElementById('displayDiscCash').textContent = formatPercent(res.entrada.desconto_pct);
  document.getElementById('displayCashDiscountValue').textContent = formatCurrency(res.entrada.desconto_rs);

  document.getElementById('displayDiscInstallment').textContent = formatPercent(res.parcelado.desconto_pct);
  document.getElementById('displayInstallmentDiscountValue').textContent = formatCurrency(res.parcelado.desconto_rs);
  document.getElementById('displayTotalInstallment').textContent = formatCurrency(res.parcelado.valor_final_parcelamento);

  document.getElementById('displayDiscCredit').textContent = formatPercent(res.parcelado.desconto_pct);
  document.getElementById('displayCreditCardDiscountValue').textContent = formatCurrency(res.parcelado.desconto_rs);
  document.getElementById('displayTotalCreditCard').textContent = formatCurrency(res.parcelado.valor_final_parcelamento);

  document.getElementById('displayTotalDiscount').textContent = formatCurrency(res.total_geral.desconto_rs);
  document.getElementById('displayAverageDiscount').textContent = formatPercent(res.total_geral.desconto_pct);
}

document.addEventListener('DOMContentLoaded', function () {
  preencherZeros();

  var form = document.getElementById('formCalculadora');
  form.addEventListener('submit', function (e) {
    e.preventDefault();

    var totalBruto = parseDecimal(form.productValue.value);
    var valorEntrada = parseDecimal(form.entryValue.value);
    var metodoEntrada = form.querySelector('input[name="metodo_entrada"]:checked').value;
    var prazo = parseInt(form.prazo.value, 10);
    var tipoVenda = form.querySelector('input[name="tipo_venda"]:checked').value;

    if (!totalBruto || !valorEntrada) {
      mostrarErro('Informe o valor do produto e o valor da entrada.');
      return;
    }

    esconderErro();

    fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        total_bruto: totalBruto,
        valor_entrada: valorEntrada,
        metodo_entrada: metodoEntrada,
        prazo: prazo,
        tipo_venda: tipoVenda
      })
    })
      .then(function (resp) { return resp.json(); })
      .then(function (data) {
        if (data.sucesso) {
          aplicarResultado(data, form.entryValue.value);
        } else {
          mostrarErro(data.erro || 'Erro ao calcular.');
        }
      })
      .catch(function () {
        mostrarErro('Não foi possível conectar ao servidor. Verifique se o backend está rodando.');
      });
  });
});
