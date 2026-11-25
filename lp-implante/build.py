#!/usr/bin/env python3
"""Gera a LP a partir de src/.

  python3 build.py            -> cria dist/ (produção) e preview.html (arquivo único)

dist/      : arquivos para publicar (usa imagens locais em dist/assets/img/, GTM ligado)
preview.html: um arquivo só, para revisar no celular. Imagens vêm do site atual, fontes embutidas,
              GTM DESLIGADO (a prévia não dispara nenhuma conversão) e envio do formulário simulado.
"""
import base64, pathlib, shutil, re

ROOT = pathlib.Path(__file__).parent
SRC, DIST = ROOT / "src", ROOT / "dist"

SITE = "https://drafabianamarques.com"
UP = SITE + "/wp-content/uploads/"
GTM_ID = "GTM-KHCNXTJ3"

# chave: (URL atual no site, nome do arquivo local em dist/assets/img/)
IMG = {
    "hero":                ("2026/01/1.-Foto-Dra.-Fabiana-Marques-.png",            "dra-fabiana-topo.jpg"),
    "clinica":             ("2026/01/BEM-VINDO.png",                                "clinica.jpg"),
    "unitario":            ("2026/02/1.-Implante-Unitario--1024x683.webp",          "implante-unitario.webp"),
    "protocolo":           ("2026/02/1.-Implante-PROTOCOLO--1024x683.webp",         "protese-protocolo.webp"),
    "orto-fixo":           ("2026/02/2.-Ortodontia-com-aparelho-fixo-1024x683.webp", "orto-fixo.webp"),
    "orto-alinhadores":    ("2026/02/2.-Ortodontia-com-alinhadores-1024x683.webp",  "orto-alinhadores.webp"),
    "ortopedia":           ("2026/02/2.-Ortopedia-funcional-1024x683.webp",         "ortopedia-funcional.webp"),
    "bruxismo":            ("2026/02/2.-Bruxismo-1024x683.webp",                    "bruxismo.webp"),
}

FONTS = [400, 600, 700]
def font_css(embed: bool, prefix: str) -> str:
    out = []
    for w in FONTS:
        f = ROOT / "fonts" / f"montserrat-latin-{w}-normal.woff2"
        url = ("data:font/woff2;base64," + base64.b64encode(f.read_bytes()).decode()) if embed else f"{prefix}fonts/{f.name}"
        out.append(f"@font-face{{font-family:Montserrat;font-style:normal;font-weight:{w};font-display:swap;src:url({url}) format('woff2')}}")
    return "\n".join(out)

GTM_HEAD = ("<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
            "var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
            f"j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM_ID}');</script>")
GTM_BODY = (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" '
            'style="display:none;visibility:hidden"></iframe></noscript>')

def render(tpl: str, *, preview: bool, fontprefix: str) -> str:
    s = tpl
    s = s.replace("{{FONT_CSS}}", font_css(preview, fontprefix))
    s = s.replace("{{FONT_PRELOAD}}", "" if preview else "\n".join(
        f'<link rel="preload" as="font" type="font/woff2" crossorigin href="{fontprefix}fonts/montserrat-latin-{w}-normal.woff2">' for w in (600, 700)))
    s = s.replace("{{GTM_HEAD}}", "" if preview else GTM_HEAD)
    s = s.replace("{{GTM_BODY}}", "" if preview else GTM_BODY)
    s = s.replace("{{GTM_NOSCRIPT_NOTE}}", "")
    s = s.replace("{{PREVIEW}}", "true" if preview else "false")
    s = s.replace("{{CANONICAL}}", SITE + "/implantodontia-lp/")
    s = s.replace("{{URL_OBRIGADO}}", "/obrigado/")
    s = s.replace("{{URL_PRIVACIDADE}}", SITE + "/politica-de-privacidade/")   # CONFIRMAR a URL real
    s = s.replace("{{URL_TERMOS}}", SITE + "/termos-e-condicoes/")             # CONFIRMAR a URL real
    for k, (live, local) in IMG.items():
        s = s.replace("{{img:%s}}" % k, (UP + live) if preview else f"{fontprefix}assets/img/{local}")
        s = s.replace("{{imgabs:%s}}" % k, (UP + live) if preview else f"{SITE}{fontprefix}assets/img/{local}")
    left = re.findall(r"\{\{[^}]+\}\}", s)
    assert not left, f"placeholders sem valor: {left}"
    return s

def main():
    index = (SRC / "index.html").read_text(encoding="utf-8")
    thanks = (SRC / "obrigado.html").read_text(encoding="utf-8")

    (ROOT / "preview.html").write_text(render(index, preview=True, fontprefix=""), encoding="utf-8")

    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "obrigado").mkdir(parents=True)
    (DIST / "assets" / "img").mkdir(parents=True)
    shutil.copytree(ROOT / "fonts", DIST / "fonts")
    # produção: caminhos absolutos a partir da raiz do site (a LP fica em /implantodontia-lp/)
    base = "/implantodontia-lp/"
    (DIST / "index.html").write_text(render(index, preview=False, fontprefix=base), encoding="utf-8")
    (DIST / "obrigado" / "index.html").write_text(render(thanks, preview=False, fontprefix=base), encoding="utf-8")
    print("ok: preview.html e dist/ gerados")
    missing = [local for _, local in IMG.values() if not (ROOT / "img-originais" / local).exists()]
    if missing:
        print("faltam as imagens originais em img-originais/:", ", ".join(missing))

if __name__ == "__main__":
    main()
