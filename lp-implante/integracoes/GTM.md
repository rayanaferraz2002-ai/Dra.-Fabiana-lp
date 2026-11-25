# GTM da LP de implante (contêiner GTM-KHCNXTJ3)

A LP não usa Elementor: os acionadores antigos (envio de formulário do Elementor, pop-up, visita a `/obrigado/`) não funcionam nela.
A página manda estes eventos ao `dataLayer` (sem dados pessoais):

| Evento | Quando | Parâmetro |
|---|---|---|
| `whatsapp_click` | clique em qualquer botão de WhatsApp | `link_location`: hero, formulario, barra_fixa |
| `phone_click` | clique em "Ligar" ou no telefone | `link_location`: hero, formulario, barra_fixa, contato |
| `cta_click` | clique em "Agendar minha avaliação/consulta" (leva ao formulário) | `link_location`: tratamentos, indicacoes, sobre, atendimento |
| `form_submit_lead` | envio válido do formulário (antes de sair da página) | `link_location`: formulario |
| `lead_confirmado` | na página `/implantodontia-lp/obrigado/`, só depois de um envio real, uma vez | — |

Decisão (25/11/2026): **`lead_confirmado` e `whatsapp_click` são conversões principais** no Google Ads.
Quem envia o formulário e é levado ao WhatsApp pela página de obrigado não gera `whatsapp_click`, então não conta duas vezes.

## Atalho: importar

`integracoes/gtm-importar-lp-implante.json` cria de uma vez a variável, os 5 acionadores e a tag do GA4.
As 2 tags de conversão do Google Ads são criadas à mão (precisam do ID e do rótulo de cada conversão).
GTM → Administrador → Importar contêiner → escolher o arquivo → espaço de trabalho **Novo** → opção **Mesclar** + **Renomear tags, acionadores e variáveis conflitantes**.

## Ordem recomendada

1. Montar tudo num **espaço de trabalho novo** do GTM, **sem publicar**.
2. Subir a LP na Hostinger.
3. Testar com o **Visualizar** do GTM na LP publicada.
4. **Publicar** o contêiner logo em seguida (enquanto não publicar, a LP nova não conta conversões).

## 1. Variável

Variáveis → Variáveis definidas pelo usuário → Nova → **Variável da camada de dados**
- Nome: `DLV - link_location` · Nome da variável da camada de dados: `link_location`

Variáveis integradas → Configurar → marcar **Event** e **Page Path** (se não estiverem).

## 2. Acionadores (tipo "Evento personalizado")

Crie um para cada evento, com o nome do evento exatamente igual:
`CE - lead_confirmado`, `CE - whatsapp_click`, `CE - phone_click`, `CE - cta_click`, `CE - form_submit_lead`.

## 3. Tags

**GA4 (uma tag para todos os eventos)**
- Tipo: Google Analytics: evento do GA4 · ID de medição: `G-ZD1WSSR2J8` (ou a tag do Google já existente)
- Nome do evento: `{{Event}}` · Parâmetro: `link_location` = `{{DLV - link_location}}`
- Acionadores: os 5 acionadores acima.
- No GA4, marque `lead_confirmado` como evento-chave (e `whatsapp_click`, se quiserem ver lá também).

**Google Ads: conversão do formulário**
- No Google Ads: Metas → Conversões → Nova ação de conversão → Site → criar manualmente.
  Categoria "Enviar formulário de lead", nome "LP Implante: formulário", contagem **Uma**, ação **principal**. Copie o **ID** e o **Rótulo**.
- No GTM: Tag "Acompanhamento de conversões do Google Ads" com esse ID e rótulo · Acionador: `CE - lead_confirmado`.

**Google Ads: conversão do WhatsApp**
- Mesma coisa: categoria "Contato", nome "LP Implante: clique WhatsApp", contagem **Uma**, ação **principal**.
- Tag de conversão com ID e rótulo dela · Acionador: `CE - whatsapp_click`.

Use o ID da conta do Google Ads que roda a campanha (o contêiner tem `AW-17925773615` e `AW-17878631107`; confira qual é o atual).
Confirme que existe a tag **Vinculador de conversões** em "All Pages".

**Meta Pixel (opcional)**: tag HTML com `<script>fbq('track','Lead');</script>` no `CE - lead_confirmado`
(e `fbq('track','Contact')` no `CE - whatsapp_click`), com sequenciamento para disparar depois da tag base do Pixel.

## 4. Conferir os acionadores antigos (importante)

Eles podem disparar também na LP nova e contar conversão em dobro ou errada:
- **Visita à página de obrigado**: se a condição for "Page URL **contém** obrigado", ela passa a pegar `/implantodontia-lp/obrigado/`
  (inclusive visitas diretas, sem envio). Troque para "Page Path **igual a** `/obrigado/`" ou exclua `/implantodontia-lp/`.
- **Clique em link do WhatsApp** (Click URL contém `wa.me` ou `whatsapp`): também pegaria os botões da LP, duplicando o `whatsapp_click`.
  Adicione a condição "Page Path **não começa com** `/implantodontia-lp`".
- **Envio de formulário** genérico (gtm.formSubmit): ligue "Verificar validação" ou exclua `/implantodontia-lp`.
- Gatilhos de **pop-up do Elementor**: não existem na LP; podem ficar para o resto do site.

## 5. Testar (Visualizar / Tag Assistant), com a LP publicada

1. Clique em WhatsApp no topo → aparece `whatsapp_click` (link_location hero) e dispara GA4 + conversão WhatsApp.
2. Clique em Ligar → `phone_click` (só GA4).
3. Envie o formulário com dados de teste → `form_submit_lead`, depois na página de obrigado `lead_confirmado` com GA4 + conversão do formulário;
   em seguida abre o WhatsApp (o `whatsapp_click` **não** deve disparar aqui).
4. Recarregue a página de obrigado → nada de `lead_confirmado`.
5. Confira que nenhum acionador antigo disparou junto.
6. Apague a linha de teste da planilha. Publique o contêiner com o nome "LP implante nova".
