/**
 * Leads da LP de implante — Dra. Fabiana Marques
 * Recebe o formulário da página, grava uma linha nesta planilha e manda um aviso por e-mail.
 * Instalação: ver integracoes/COMO-INSTALAR.md
 */

var EMAIL_AVISO = 'dra.fabiana.s.orto@gmail.com';   // quem recebe o aviso de cada lead
var ABA = 'Leads';
var CAMPOS = ['nome', 'celular', 'email', 'interesse', 'consentimento', 'pagina',
              'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid'];
var CABECALHO = ['Data e hora', 'Nome', 'WhatsApp', 'E-mail', 'Interesse', 'Consentimento', 'Página',
                 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid'];

function doPost(e) {
  try {
    var d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    var nome = limpa(d.nome), tel = String(d.celular || '').replace(/\D/g, '');
    // descarta envios inválidos (o formulário já valida; isto barra chamadas soltas)
    if (!nome || tel.length < 10 || tel.length > 13 || d.consentimento !== true) return resposta('ignorado');

    var lock = LockService.getScriptLock();
    lock.waitLock(10000);
    try {
      var aba = planilha();
      var agora = Utilities.formatDate(new Date(), 'America/Sao_Paulo', 'dd/MM/yyyy HH:mm');
      var linha = [agora].concat(CAMPOS.map(function (c) {
        if (c === 'consentimento') return 'sim';
        if (c === 'celular') return tel;
        return limpa(d[c]);
      }));
      aba.appendRow(linha.map(seguro));
    } finally {
      lock.releaseLock();
    }

    var corpo = [
      'Novo contato pela LP de implante:',
      '',
      'Nome: ' + nome,
      'WhatsApp: ' + tel + '  (abrir conversa: https://wa.me/55' + tel.replace(/^55/, '') + ')',
      'E-mail: ' + (limpa(d.email) || '-'),
      'Interesse: ' + (limpa(d.interesse) || '-'),
      'Origem: ' + ([limpa(d.utm_source), limpa(d.utm_campaign)].filter(String).join(' / ') || '-'),
      '',
      'A pessoa também foi levada ao WhatsApp da clínica com estas respostas.',
      'Planilha: ' + SpreadsheetApp.getActiveSpreadsheet().getUrl()
    ].join('\n');
    MailApp.sendEmail(EMAIL_AVISO, 'Novo lead (implante): ' + nome, corpo);

    return resposta('ok');
  } catch (err) {
    console.error(err);
    return resposta('erro');
  }
}

// Abrir o endereço /exec no navegador mostra "ok": serve para testar se a implantação está no ar.
function doGet() { return resposta('ok'); }

function planilha() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var aba = ss.getSheetByName(ABA) || ss.insertSheet(ABA);
  if (aba.getLastRow() === 0) {
    aba.appendRow(CABECALHO);
    aba.setFrozenRows(1);
    aba.getRange(1, 1, 1, CABECALHO.length).setFontWeight('bold');
  }
  return aba;
}

function limpa(v) { return String(v == null ? '' : v).trim().slice(0, 200); }

// evita que um texto começando com = + - @ vire fórmula na planilha
function seguro(v) { v = String(v); return /^[=+\-@]/.test(v) ? "'" + v : v; }

function resposta(t) { return ContentService.createTextOutput(t).setMimeType(ContentService.MimeType.TEXT); }

/** Rode esta função uma vez pelo editor (botão "Executar") para autorizar e testar: grava uma linha e manda um e-mail de teste. */
function testar() {
  var r = doPost({ postData: { contents: JSON.stringify({
    nome: 'TESTE - pode apagar', celular: '11900000000', email: '', interesse: 'Implante unitário',
    consentimento: true, pagina: '/implantodontia-lp/', utm_source: 'teste' }) } });
  Logger.log(r.getContent());
}
