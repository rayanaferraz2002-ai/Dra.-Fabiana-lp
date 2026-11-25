# LP de implante — Dra. Fabiana Marques

Cliente da Raya Criativa (quem pede é a Rayana). Landing page para anúncios do Google Ads da clínica
Dra. Fabiana Marques Odontologia (Vila Prudente, São Paulo; CRO-SP 58.746). 86% do gasto do Ads vem do celular,
então o celular é a prioridade. Responda e escreva sempre em português do Brasil.

Leia também `LEIAME.md` (estado, pendências, como publicar) e `COMPLIANCE.md` (frases pendentes de revisão).

## Como o projeto funciona

- HTML, CSS e JS puros, sem framework. Fonte única: Montserrat (400, 600, 700), hospedada em `fonts/`.
- Código-fonte em `src/index.html` e `src/obrigado.html`. Não edite `preview.html` nem `dist/` à mão.
- `python3 build.py` gera `preview.html` (arquivo único, imagens do site atual, sem GTM, formulário simulado) e `dist/` (produção).
- `python3 tools/check.py`: mede o celular (375×812) e o desktop, gera screenshots em `tools/out/`.
- `python3 tools/flow.py`: testa o fluxo de conversão em `dist/`. Se faltar navegador: `pip install playwright && playwright install chromium`.
- Rode `build.py`, `check.py` e `flow.py` depois de cada mudança e olhe os screenshots antes de dizer que está pronto.

## Regras que não podem ser quebradas

1. **Normas do CFO.** Sem promessa de resultado, garantia, superlativo ("melhor", "definitivamente", "excelentes resultados", "duradouros").
   Todo texto que ainda espera o revisor tem `data-pendente="Cxx"` e está em `COMPLIANCE.md`. Mantenha a marcação.
   Não invente texto novo de benefício ou resultado; se precisar, escreva neutro, marque `data-pendente` e inclua no `COMPLIANCE.md`.
2. **CRO** (CRO-SP 58.746) visível no topo e no rodapé.
3. **Dado de saúde (LGPD).** Sem campo livre de "motivo da consulta". O formulário tem consentimento obrigatório, e-mail opcional e lista de interesse opcional.
4. **Rastreamento.** GTM `GTM-KHCNXTJ3` só em `dist/` (o preview nunca dispara nada). Eventos do `dataLayer`: `whatsapp_click`, `phone_click`, `cta_click`
   (com `link_location`), `form_submit_lead` e `lead_confirmado`. Não mude esses nomes sem avisar, porque o GTM e o Google Ads dependem deles. Nenhum dado pessoal no `dataLayer`.
5. **`/obrigado/`** é `noindex` e só emite `lead_confirmado` se o formulário foi enviado na sessão. `tools/flow.py` verifica isso.
6. **Não invente dados da clínica** (horário, CEP, telefone fixo, URLs). Onde faltar, deixe `[confirmar com a clínica]` visível e liste no `LEIAME.md`.
7. **Formulário sem destino** (`ENDPOINT` vazio) abre o WhatsApp com a mensagem pronta, para nenhum lead se perder.
8. **Desempenho e acessibilidade.** Foto do topo sem lazy-load e com `fetchpriority="high"`; todas as imagens com `alt`, `width` e `height`;
   1 só H1; sem rolagem horizontal; alvos de toque com no mínimo 48 px; contraste legível.

## Metas que o `check.py` mostra e que devem continuar verdadeiras

- No celular 375×812, os botões **WhatsApp** e **Ligar** do topo ficam inteiros na primeira tela (hoje terminam em 730 px; a página antiga tinha o botão a 897 px).
- Barra fixa de WhatsApp/Ligar só aparece depois que os botões do topo saem da tela.
- Nenhum erro de JavaScript; apenas Montserrat carregada.

## Pendências conhecidas (fazer primeiro)

1. **Imagens originais.** O `build.py` ainda usa as imagens do site atual no preview e só avisa quando faltam arquivos em `img-originais/`.
   Quando os originais estiverem em `img-originais/` (nomes esperados em `img-originais/LEIA-ME.txt`), implementar a etapa que
   redimensiona e comprime (webp ou jpg, versões 1x e 2x, `srcset`) para `dist/assets/img/` e aponta o preview para elas.
2. **Textos aprovados.** Trocar os provisórios (`COMPLIANCE.md`) pelos do arquivo do relatório quando o revisor liberar.
3. **Dados faltando:** horário, CEP, URLs reais da Política de Privacidade e dos Termos, telefone fixo (se houver), destino do formulário.
4. **Decisões em aberto** (listadas no `LEIAME.md`): indexar a LP ou não, e-mail opcional, conversão por clique no WhatsApp, banner de cookies.

Para publicar na hospedagem é preciso acesso, que a Rayana ainda não passou. Não tente publicar; entregue `dist/` pronto e descreva os passos do `LEIAME.md`.
