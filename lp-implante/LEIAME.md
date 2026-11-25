# LP de implante — Dra. Fabiana Marques

Reconstrução em código puro (sem WordPress e sem Elementor) da página `/implantodontia-lp/`.

## Arquivos

- `preview.html`: a página inteira em um arquivo só, para revisar no celular. Não dispara rastreamento e o formulário só simula o envio.
- `src/index.html` e `src/obrigado.html`: o código-fonte.
- `build.py`: gera `preview.html` e a pasta `dist/` (`python3 build.py`).
- `dist/`: o que vai para a hospedagem (`index.html`, `obrigado/index.html`, `fonts/`, `assets/img/`).
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
| 5 fontes, CSS do Elementor | 1 fonte (Montserrat, 3 pesos, hospedada junto), CSS próprio de ~8 KB |
| Imagens sem descrição | Todas com descrição (alt) |
| Página de ~14.000 px no celular | ~11.300 px (formulário e perguntas frequentes subiram) |

Ordem das seções: o formulário e as perguntas frequentes vêm antes de "Outros tratamentos".
Também corrigi erros de texto: "Extracções", "Golpes ou acidentes" (virou "Traumas ou acidentes"), "excelencia", "sorrido" e "Privacidad".

## O que ainda falta (precisa de você ou da clínica)

1. **Imagens originais.** O preview usa as imagens do site atual. A foto do topo tem só 375×500 px, e fica borrada em tela retina.
   Mande os originais (foto da Dra., clínica, tratamentos) e eu preparo as versões leves.
   Hoje a shell do Claude Code não alcança o site da clínica, então eu não consigo baixá-las sozinha.
2. **Textos aprovados** pelo revisor (ver `COMPLIANCE.md`).
3. **Horário de atendimento** e **CEP** (entram na página e nos dados estruturados).
4. **URLs reais** da Política de Privacidade e dos Termos. Hoje estão como `/politica-de-privacidade/` e `/termos-e-condicoes/`, por suposição.
5. **WhatsApp e telefone.** Usei o WhatsApp Business da clínica (11 94824-6888) para os dois. Confirmar se há um telefone fixo.
6. **Destino do formulário** (e-mail, planilha ou CRM). Enquanto não houver, o formulário abre o WhatsApp com a mensagem pronta, então nenhum lead se perde.

## Decisões em aberto

- **Indexar a LP ou não.** Hoje ela está indexável com canonical próprio (como a atual). O relatório aponta cópias duplicadas no Google (LP e página de serviço). A solução costuma ser: LP com `noindex` e a página de serviço indexada. Depende de existir a página de serviço equivalente.
- **E-mail opcional ou obrigatório.** Deixei opcional para aumentar o envio. Era obrigatório.
- **Conversão por clique no WhatsApp.** Antes, o WhatsApp só abria depois do formulário. Agora o clique direto vira evento. Isso muda o que o Google Ads conta como conversão; precisa ser decidido junto com quem cuida da campanha.
- **Banner de cookies com Consent Mode.** Recomendo, por ser clínica e por LGPD, mas reduz as conversões medidas. Não incluí.
- **Crédito da agência no rodapé.** Tirei "Designed by Estratega". Colocar o da Raya Criativa é opcional.

## Rastreamento (atenção antes de publicar)

A página atual carrega tudo pelo Google Tag Manager `GTM-KHCNXTJ3`: GA4 `G-ZD1WSSR2J8`, Google Ads `AW-17925773615` e `AW-17878631107`, Meta Pixel `1599263088187252` e Microsoft Clarity `vdam6fv0c2`.
A nova página usa o mesmo contêiner. **Os acionadores do GTM que dependiam do Elementor (envio de formulário, pop-up, página de obrigado) precisam ser refeitos**, senão o Google Ads pode parar de contar conversões.
A página envia estes eventos ao `dataLayer` (sem dados pessoais):

- `whatsapp_click` e `phone_click`, com `link_location` (hero, barra_fixa, formulario, contato)
- `cta_click`
- `form_submit_lead`
- `lead_confirmado`, só na página de obrigado e só depois de um envio real

Se os 2 IDs do Google Ads são mesmo necessários, ou se um é antigo, é uma conferência a fazer no GTM.

## Como publicar (precisa de acesso à hospedagem)

1. Fazer backup da página atual.
2. Subir `dist/index.html`, `dist/fonts/` e `dist/assets/` para uma pasta `implantodontia-lp/` e `dist/obrigado/index.html` para `obrigado/`. Servidor Apache/LiteSpeed costuma entregar a pasta física antes do WordPress; testar.
3. Despublicar ou redirecionar as páginas do WordPress com o mesmo endereço, para não haver duplicidade.
4. Conferir no celular, no Tag Assistant do GTM e no PageSpeed. **Anote a nota do PageSpeed da página atual antes de trocar**, para comparar.
