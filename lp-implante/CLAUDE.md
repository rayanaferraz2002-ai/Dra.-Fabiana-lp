# LP de implante — Dra. Fabiana Marques

Cliente da Raya Criativa (quem pede é a Rayana). Landing page para anúncios do Google Ads da clínica
Dra. Fabiana Marques Odontologia (Vila Prudente, São Paulo; CRO-SP 58.746). 86% do gasto do Ads vem do celular,
então o celular é a prioridade. Responda e escreva sempre em português do Brasil.

Leia também `LEIAME.md` (estado, pendências, como publicar) e `COMPLIANCE.md` (frases pendentes de revisão).

## Como o projeto funciona

- HTML, CSS e JS puros, sem framework. Fontes hospedadas em `fonts/` (definidas pela Rayana):
  - títulos principais (H1, H2, citação): **Gangitem** (177Studio; a clínica tem licença, confirmada pela Rayana em 25/11/2026). `fonts/gangitem.woff2` é o arquivo do site da clínica reduzido aos caracteres do português. Sem ele, o `build.py` usa Playfair Display;
  - texto corrido: Montserrat 400; destaque no texto (`<strong>`): Montserrat 700 itálico; títulos secundários (H3, chamadas acima dos títulos): Montserrat 800 itálico; botões e rótulos: Montserrat 700.
- Layout de referência: vitaprimeodonto.com.br/implantes (estrutura e ritmo das seções), com a identidade da Dra. Não copiar textos, fotos nem marca de lá.
- Cores: creme `#FFF5EC`, vinho `#753E3E`, destaque `#C67D74`. O `#C67D74` tem contraste baixo para texto (2,96:1 no creme), então fica em ícones, linhas e fundos;
  palavras em destaque usam `--rose-tit` `#B06A61` (títulos), `--rose-txt` `#A35A52` (texto pequeno) e `--rose-claro` `#F0C6BF` (sobre o vinho).
- Logo: `marca/logo-vinho.png` e `marca/logo-creme.png`, recoloridos a partir do logo branco do site (`1.1.-LOGO-BRANCO.png`).
- Código-fonte em `src/index.html` e `src/obrigado.html`. Não edite `preview.html` nem `dist/` à mão.
- `python3 build.py` gera `preview.html` (arquivo único, imagens e fontes embutidas, sem GTM, formulário simulado) e `dist/` (produção).
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
5. **`/implantodontia-lp/obrigado/`** (dentro da pasta da LP; o `/obrigado/` do WordPress não é tocado) é `noindex` e só emite `lead_confirmado` se o formulário foi enviado na sessão. `tools/flow.py` verifica isso.
6. **Não invente dados da clínica** (horário, CEP, telefone fixo, URLs). Onde faltar, deixe `[confirmar com a clínica]` visível e liste no `LEIAME.md`.
7. **Formulário → WhatsApp.** Depois do envio, a pessoa vai para a página de obrigado, que registra o `lead_confirmado` e então abre o WhatsApp da clínica
   com as respostas (nome, interesse, e-mail). A mensagem fica só no `sessionStorage`, nunca na URL da página nem no `dataLayer`.
   Com `ENDPOINT` definido (planilha/e-mail), os dados também vão para lá, em paralelo, sem atrasar a pessoa. `tools/flow.py` verifica o fluxo.
8. **Desempenho e acessibilidade.** Foto do topo sem lazy-load e com `fetchpriority="high"`; todas as imagens com `alt`, `width` e `height`;
   1 só H1; sem rolagem horizontal; alvos de toque com no mínimo 48 px; contraste legível.

## Metas que o `check.py` mostra e que devem continuar verdadeiras

- No celular 375×812, os botões **WhatsApp** e **Ligar** do topo ficam inteiros na primeira tela (hoje terminam em 498 px; a página antiga tinha o botão a 897 px).
- Barra fixa de WhatsApp/Ligar só aparece depois que os botões do topo saem da tela.
- Nenhum erro de JavaScript; apenas Montserrat e a fonte dos títulos carregadas.

## Pendências conhecidas (fazer primeiro)

1. **Imagens.** Feito: o `build.py` lê `img-originais/<nome>.(jpg|png|webp)` (nomes no dicionário `IMG` e em `img-originais/LEIA-ME.txt`),
   gera versões webp 1x/2x em `dist/assets/img/` com `srcset`/`sizes` (cache em `.img-cache/`, fora do git) e embute a menor no preview.
   Para trocar uma foto, substitua o arquivo em `img-originais/` e rode o build. Os 6 cartões de tratamento ainda usam as versões do site (1500 px).
2. **Textos:** revisão do CFO concluída em 25/11/2026 (ver `COMPLIANCE.md`); marcações `data-pendente` retiradas. Texto novo de benefício ou resultado volta a precisar de revisão e de marcação.
3. **Fonte Gangitem:** instalada (licença confirmada em 25/11/2026).
4. **Dados faltando:** telefone fixo (se houver) e o endereço `/exec` do script de leads (`FORM_ENDPOINT` no `build.py`).
   Links conferidos no site: Política de Privacidade `/privacy-policy/` e Termos `/termos-e-condicoes/`.
5. **Decisões tomadas** (nov/2026, ver `LEIAME.md`): LP indexável; e-mail opcional; clique no WhatsApp como conversão principal; sem banner de cookies por enquanto.

Para publicar na hospedagem é preciso acesso, que a Rayana ainda não passou. Não tente publicar; entregue `dist/` pronto e descreva os passos do `LEIAME.md`.
