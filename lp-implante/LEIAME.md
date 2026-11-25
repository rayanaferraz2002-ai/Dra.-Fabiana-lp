# LP de implante — Dra. Fabiana Marques

Reconstrução em código puro (sem WordPress e sem Elementor) da página `/implantodontia-lp/`.

## Arquivos

- `preview.html`: a página inteira em um arquivo só, para revisar no celular. Não dispara rastreamento e o formulário só simula o envio.
- `src/index.html` e `src/obrigado.html`: o código-fonte.
- `build.py`: gera `preview.html` e a pasta `dist/` (`python3 build.py`).
- `dist/`: o que vai para a hospedagem (`index.html`, `obrigado/index.html`, `fonts/`, `assets/img/`).
- `marca/`: logo da clínica em vinho e em creme (recolorido a partir do logo branco do site).
- `COMPLIANCE.md`: frases pendentes de revisão do CFO.

## O que muda em relação à página atual

| Antes | Agora |
|---|---|
| Foto do topo some até a pessoa rolar (cache) | A foto carrega direto, sem lazy-load, com espaço reservado |
| Botão de agendar a 897 px (tela de 812 px) | WhatsApp e "Ligar" inteiros na primeira tela (até 730 px) |
| Sem WhatsApp nem telefone antes do formulário | WhatsApp e telefone clicáveis no topo, no formulário e numa barra fixa que aparece ao rolar |
| 7 botões abrindo um pop-up antes do WhatsApp | Botões levam ao WhatsApp ou ao formulário |
| `/obrigado/` conta como lead mesmo vindo da busca | A conversão só dispara se a pessoa enviou o formulário nesta sessão; `noindex` na página |
| Formulário sem consentimento, com campo livre de saúde | Consentimento LGPD, sem campo livre, lista opcional de interesse |
| Sem H1 nem descrição | 1 H1, título, descrição, dados estruturados da clínica (schema Dentist) |
| 5 fontes, CSS do Elementor | 2 fontes hospedadas junto (Playfair Display nos títulos, Montserrat no texto), CSS próprio |
| Imagens sem descrição | Todas com descrição (alt) |
| Página de ~14.000 px no celular | ~11.300 px (formulário e perguntas frequentes subiram) |

## Visual (novembro de 2026)

Layout inspirado na página de implantes da Vita Prime (estrutura e ritmo), com a identidade da Dra. Fabiana:
creme `#FFF5EC`, vinho `#753E3E` e destaque `#C67D74`; Playfair Display nos títulos e Montserrat no texto; logo do site no topo e no rodapé.

- **Topo:** logo, CRO, título, texto e botões; a foto da Dra. vem logo abaixo dos botões (no desktop, ao lado), sem divisão reta: ela se dissolve no fundo creme num degradê esfumaçado.
- **"Quem vai cuidar de você":** foto cheia, sem moldura, com o mesmo degradê (no desktop, ocupa a metade esquerda e se dissolve só na divisão com o texto; bordas de cima e de baixo retas).
- **Seções intercaladas** em creme, branco e vinho, com cartões arredondados e ícones em rosé, e um botão de agendamento ao fim das seções principais, com a nota "Atendimento particular".
- **Ordem:** topo → faixa → frase → Tratamentos especializados → Dra. Fabiana → Onde fica o consultório → Indicações → Como funciona → Etapas → Agende (formulário) → Perguntas frequentes → Outros tratamentos → Contato.
- **"Onde fica o consultório?":** 4 fotos do consultório (Drive da clínica: IMG_1496 em cima, larga, e IMG_1495, IMG_1492 e IMG_1506 embaixo), endereço e mapa do Google.
  O mapa é um `iframe` do Google Maps com `loading="lazy"`: só carrega quando a pessoa chega perto da seção, mas, ao carregar, o Google pode gravar cookies (vale considerar no banner de cookies, ver "Decisões em aberto").
- **No celular,** "Outros tratamentos" é um carrossel de arrastar para o lado.
- **Botão de WhatsApp em vinho** (antes era verde), como na referência, que usa a cor da marca. Se preferir o verde do WhatsApp, é uma troca de uma linha (`.btn-wa`).
- **Contraste:** o `#C67D74` não tem contraste suficiente para texto (2,96:1 no creme). Ele aparece em ícones, linhas e fundos; as palavras em destaque usam tons mais escuros do mesmo rosé.

Ordem das seções: o formulário e as perguntas frequentes continuam antes de "Outros tratamentos".
Também corrigi erros de texto: "Extracções", "Golpes ou acidentes" (virou "Traumas ou acidentes"), "excelencia", "sorrido" e "Privacidad".

## O que ainda falta (precisa de você ou da clínica)

1. **Fonte dos títulos:** resolvido. Playfair Display (a Gangitem foi testada, e a Rayana preferiu manter a Playfair).
2. **Imagens.** Já estão em `img-originais/` e o build gera as versões leves (1x e 2x) sozinho:
   topo = foto do procedimento do site (`BG_3`, 1500 px); "Quem vai cuidar de você" = `perfil.png` do Drive (1080×1350);
   consultório = 4 fotos do Drive (2048 px). Os cartões de tratamento usam as versões do site (1500 px); se houver originais maiores, é só trocar.
3. **Textos:** revisão do CFO concluída em 25/11/2026 (ver `COMPLIANCE.md`).
4. **Horário de atendimento e CEP:** resolvido (perfil da clínica no Google): seg. a qua. 9h–21h, qui. e sex. 9h–18h, sáb. e dom. fechado; Rua Dr. Roberto Feijó, 535 – Sala 01, CEP 03138-001. Na página e nos dados estruturados.
5. **URLs da Política de Privacidade e dos Termos:** resolvido. Conferido no rodapé do site: `/privacy-policy/` e `/termos-e-condicoes/`.
6. **WhatsApp e telefone.** Usei o WhatsApp Business da clínica (11 94824-6888) para os dois. Confirmar se há um telefone fixo.
7. **Destino do formulário** (planilha do Google + e-mail, via Apps Script). Hoje, depois do envio, a pessoa vai para a página de obrigado
   (que conta a conversão) e o WhatsApp abre com as respostas dela, então nenhum lead se perde; falta só o registro na planilha e o aviso por e-mail.
   Script e roteiro prontos em `integracoes/` (avisos para dra.fabiana.s.orto@gmail.com, planilha na conta do consultório).
   Falta o consultório instalar (`integracoes/COMO-INSTALAR.md`) e mandar o endereço `/exec`, que entra em `FORM_ENDPOINT` no `build.py`.

## Decisões tomadas (novembro de 2026)

- **Indexar a LP:** sim, indexável com canonical próprio (como a página atual).
- **E-mail:** opcional no formulário.
- **Clique no WhatsApp:** conta como **conversão principal** no Google Ads (evento `whatsapp_click`), junto com `lead_confirmado`.
  Configurar no GTM/Ads. Quem envia o formulário e é levado ao WhatsApp pela página de obrigado não gera `whatsapp_click` (só `lead_confirmado`), então não conta duas vezes.
- **Banner de cookies:** não por enquanto (reavaliar depois; o mapa do Google também grava cookies).
- **Página de obrigado:** fica em `/implantodontia-lp/obrigado/`, dentro da pasta da LP. O `/obrigado/` do WordPress continua como está.
- **Crédito da agência no rodapé:** sem crédito por enquanto.

## Rastreamento (atenção antes de publicar)

A página atual carrega tudo pelo Google Tag Manager `GTM-KHCNXTJ3`: GA4 `G-ZD1WSSR2J8`, Google Ads `AW-17925773615` e `AW-17878631107`, Meta Pixel `1599263088187252` e Microsoft Clarity `vdam6fv0c2`.
A nova página usa o mesmo contêiner. **Os acionadores do GTM que dependiam do Elementor (envio de formulário, pop-up, página de obrigado) precisam ser refeitos**, senão o Google Ads pode parar de contar conversões.
A página envia estes eventos ao `dataLayer` (sem dados pessoais):

- `whatsapp_click` e `phone_click`, com `link_location` (hero, barra_fixa, formulario, contato)
- `cta_click`, com `link_location` (tratamentos, indicacoes, atendimento, sobre)
- `form_submit_lead`
- `lead_confirmado`, só na página de obrigado e só depois de um envio real

Se os 2 IDs do Google Ads são mesmo necessários, ou se um é antigo, é uma conferência a fazer no GTM.

## Como publicar (Hostinger, hPanel)

O site está na Hostinger (hPanel, LiteSpeed, com a CDN/Cloudflare na frente). A LP sobe como uma **pasta física** com o mesmo endereço;
o servidor entrega a pasta antes do WordPress, sem mexer no WordPress.

Antes: OK do revisor do CFO, horário/CEP, `FORM_ENDPOINT` preenchido, GTM com os acionadores novos publicados, nota do PageSpeed da página atual anotada.

1. `python3 build.py` e conferir com `tools/check.py` e `tools/flow.py`.
2. hPanel → Arquivos → Gerenciador de Arquivos → `public_html` → criar a pasta `implantodontia-lp`.
3. Subir **todo o conteúdo de `dist/`** para dentro dela (`index.html`, `obrigado/`, `fonts/`, `assets/`). Dá para subir um .zip e usar "Extrair".
4. hPanel → Desempenho → CDN → Limpar cache (e o cache do plugin de otimização do WordPress, se houver).
5. Testar no celular: `drafabianamarques.com/implantodontia-lp/`, WhatsApp, Ligar, formulário (deve ir ao obrigado, abrir o WhatsApp e gravar na planilha).
6. Tag Assistant do GTM (eventos e `lead_confirmado` só após envio) e PageSpeed.
7. Com tudo certo, passar para rascunho a página "implantodontia-lp" do WordPress (ela já não aparece, mas evita confusão).

**Desfazer:** renomear ou apagar a pasta `implantodontia-lp` e limpar o cache; a página do WordPress volta na hora.
