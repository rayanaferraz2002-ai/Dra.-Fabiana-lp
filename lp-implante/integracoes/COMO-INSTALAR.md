# Planilha + aviso por e-mail dos leads (Google Apps Script)

Cada envio do formulário vira uma linha numa planilha do Google e um e-mail para `dra.fabiana.s.orto@gmail.com`.
Independente disso, a pessoa continua sendo levada ao WhatsApp com as respostas.

Faça tudo **logado na conta Google do consultório** (`dra.fabiana.s.orto@gmail.com`).

1. Em drive.google.com, crie uma planilha nova chamada **Leads LP Implante**.
2. Na planilha: **Extensões → Apps Script**.
3. Apague o que estiver no editor e cole todo o conteúdo de `apps-script-leads.gs`. Clique em **Salvar** (ícone de disquete).
4. No topo do editor, escolha a função **testar** e clique em **Executar**.
   O Google pede autorização: escolha a conta do consultório → "Avançado" → "Acessar (não seguro)" → **Permitir**.
   (O aviso aparece porque o script é seu e não foi publicado na loja do Google; é normal.)
   Confira: a aba **Leads** ganhou uma linha "TESTE - pode apagar" e chegou um e-mail de teste. Pode apagar a linha.
5. **Implantar → Nova implantação** → engrenagem → **App da Web**:
   - Descrição: `LP implante`
   - Executar como: **Eu**
   - Quem pode acessar: **Qualquer pessoa**
   Clique em **Implantar** e copie o **URL do app da Web** (termina em `/exec`).
6. Mande esse endereço para a Raya Criativa, que coloca na página (`ENDPOINT` em `src/index.html`).

Se um dia mudar o script, use **Implantar → Gerenciar implantações → editar (lápis) → Versão: nova versão**, para manter o mesmo endereço.

## Cuidados (LGPD)

- Compartilhe a planilha só com quem atende os leads. O interesse ("implante unitário", "prótese protocolo") pode ser considerado dado de saúde.
- Defina por quanto tempo os contatos ficam guardados e apague os antigos.
- O e-mail de aviso só vai para o endereço do consultório.
- Limite do Google numa conta comum: cerca de 100 e-mails por dia.
