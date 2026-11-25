#!/usr/bin/env python3
"""Gera a LP a partir de src/.

  python3 build.py            -> cria dist/ (produção) e preview.html (arquivo único)

dist/      : arquivos para publicar (usa imagens locais em dist/assets/img/, GTM ligado)
preview.html: um arquivo só, para revisar no celular. Imagens: as versões geradas de img-originais/ (embutidas)
              ou, se faltar o original, a do site atual. Fontes embutidas,
              GTM DESLIGADO (a prévia não dispara nenhuma conversão) e envio do formulário simulado.
"""
import base64, pathlib, shutil, re

ROOT = pathlib.Path(__file__).parent
SRC, DIST = ROOT / "src", ROOT / "dist"

SITE = "https://drafabianamarques.com"
UP = SITE + "/wp-content/uploads/"
GTM_ID = "GTM-KHCNXTJ3"
# Endereço do Apps Script que grava os leads na planilha e avisa por e-mail (ver integracoes/COMO-INSTALAR.md).
# Vazio: o formulário só leva a pessoa ao WhatsApp com as respostas. O preview nunca envia nada.
FORM_ENDPOINT = ""

# chave: (URL atual no site, nome-base do original em img-originais/, larguras geradas, atributo sizes)
# Se existir img-originais/<nome-base>.(jpg|jpeg|png|webp), o build gera <nome-base>-<largura>.webp em
# dist/assets/img/ (versões 1x e 2x, com srcset) e o preview usa a menor delas embutida.
# Se não existir, o preview usa a imagem do site atual e o dist aponta para <nome-base>-<1ª largura>.webp (avisa no final).
IMG = {
    "hero":             ("2026/01/BG_3.webp",                                     "dra-fabiana-topo",    (800, 1500), "(min-width:900px) 1020px, 190vw"),
    "clinica":          ("2026/01/1.-Foto-Dra.-Fabiana-Marques-.png",             "dra-fabiana-perfil",  (800, 1080), "(min-width:900px) 50vw, 100vw"),
    "unitario":         ("2026/02/1.-Implante-Unitario--1024x683.webp",           "implante-unitario",   (600, 1024), "(min-width:900px) 530px, 92vw"),
    "protocolo":        ("2026/02/1.-Implante-PROTOCOLO--1024x683.webp",          "protese-protocolo",   (600, 1024), "(min-width:900px) 530px, 92vw"),
    "orto-fixo":        ("2026/02/2.-Ortodontia-com-aparelho-fixo-1024x683.webp", "orto-fixo",           (600, 1024), "(min-width:900px) 530px, 80vw"),
    "orto-alinhadores": ("2026/02/2.-Ortodontia-com-alinhadores-1024x683.webp",   "orto-alinhadores",    (600, 1024), "(min-width:900px) 530px, 80vw"),
    "ortopedia":        ("2026/02/2.-Ortopedia-funcional-1024x683.webp",          "ortopedia-funcional", (600, 1024), "(min-width:900px) 530px, 80vw"),
    "bruxismo":         ("2026/02/2.-Bruxismo-1024x683.webp",                     "bruxismo",            (600, 1024), "(min-width:900px) 530px, 80vw"),
    "consultorio-1":    ("2026/01/BG_1.webp",                                     "consultorio-1",       (600, 1200), "(min-width:900px) 520px, 335px"),   # larga, em cima
    "consultorio-2":    ("2026/01/BG_2.webp",                                     "consultorio-2",       (600, 1200), "(min-width:900px) 390px, 250px"),
    "consultorio-3":    ("2026/01/BG_3.webp",                                     "consultorio-3",       (600, 1200), "(min-width:900px) 390px, 250px"),
    "consultorio-4":    ("2026/01/BG_4.webp",                                     "consultorio-4",       (400, 600),  "(min-width:900px) 170px, 110px"),   # vertical
}
ORIG = ROOT / "img-originais"
CACHE = ROOT / ".img-cache"     # versões geradas (não vai para o git); refeitas quando o original muda

def original(base):
    for ext in ("jpg", "jpeg", "png", "webp"):
        f = ORIG / f"{base}.{ext}"
        if f.exists():
            return f
    return None

def variants(base, widths):
    """Gera (uma vez) as versões webp de um original. Devolve [(largura, arquivo)] ou [] se não houver original."""
    src = original(base)
    if not src:
        return []
    from PIL import Image, ImageOps
    CACHE.mkdir(exist_ok=True)
    out, im = [], None
    for w in widths:
        f = CACHE / f"{base}-{w}.webp"
        if not f.exists() or f.stat().st_mtime < src.stat().st_mtime:
            if im is None:
                im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")   # gira pela câmera e descarta EXIF
            w2 = min(w, im.width)
            im.resize((w2, round(im.height * w2 / im.width)), Image.LANCZOS).save(f, "WEBP", quality=80, method=6)
        out.append((w, f))
    # larguras maiores que o original viram a mesma imagem: remove duplicatas
    seen, uniq = set(), []
    for w, f in out:
        from PIL import Image
        real = Image.open(f).width
        if real not in seen:
            seen.add(real); uniq.append((real, f))
    return uniq

# Títulos principais: Playfair Display (gratuita, SIL OFL), escolha da Rayana em 25/11/2026.
TITLE_FONT = ("Playfair Display", "playfair-display-latin-400-normal.woff2")

# (arquivo em fonts/, família, peso, estilo)
FONTS = [
    (TITLE_FONT[1], TITLE_FONT[0], 400, "normal"),             # títulos principais
    ("montserrat-latin-400-normal.woff2", "Montserrat", 400, "normal"),   # texto corrido
    ("montserrat-latin-700-normal.woff2", "Montserrat", 700, "normal"),   # botões, rótulos, perguntas
    ("montserrat-latin-700-italic.woff2", "Montserrat", 700, "italic"),   # destaque no texto corrido
    ("montserrat-latin-800-italic.woff2", "Montserrat", 800, "italic"),   # títulos secundários
]
PRELOAD = [TITLE_FONT[1], "montserrat-latin-400-normal.woff2"]

def font_css(embed: bool, prefix: str, only=None) -> str:
    out = []
    for name, fam, w, st in FONTS:
        if only and name not in only:
            continue
        f = ROOT / "fonts" / name
        url = ("data:font/woff2;base64," + base64.b64encode(f.read_bytes()).decode()) if embed else f"{prefix}fonts/{name}"
        out.append(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};font-display:swap;src:url({url}) format('woff2')}}")
    return "\n".join(out)

# logo da clínica (recolorido a partir do logo branco do site: marca/logo-vinho.png e marca/logo-creme.png)
LOGOS = ["logo-vinho.png", "logo-creme.png"]

GTM_HEAD = ("<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
            "var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
            f"j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM_ID}');</script>")
GTM_BODY = (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" '
            'style="display:none;visibility:hidden"></iframe></noscript>')

def render(tpl: str, *, preview: bool, fontprefix: str, only_fonts=None) -> str:
    s = tpl
    s = s.replace("{{FONT_CSS}}", font_css(preview, fontprefix, only_fonts))
    s = s.replace("{{TITLE_FONT}}", f"'{TITLE_FONT[0]}'")
    s = s.replace("{{FONT_PRELOAD}}", "" if preview else "\n".join(
        f'<link rel="preload" as="font" type="font/woff2" crossorigin href="{fontprefix}fonts/{n}">' for n in PRELOAD))
    for name in LOGOS:
        key = name[:-4]
        url = ("data:image/png;base64," + base64.b64encode((ROOT / "marca" / name).read_bytes()).decode()) if preview else f"{fontprefix}assets/img/{name}"
        s = s.replace("{{%s}}" % key, url)
    s = s.replace("{{GTM_HEAD}}", "" if preview else GTM_HEAD)
    s = s.replace("{{GTM_BODY}}", "" if preview else GTM_BODY)
    s = s.replace("{{GTM_NOSCRIPT_NOTE}}", "")
    s = s.replace("{{PREVIEW}}", "true" if preview else "false")
    s = s.replace("{{ENDPOINT}}", "" if preview else FORM_ENDPOINT)
    s = s.replace("{{CANONICAL}}", SITE + "/implantodontia-lp/")
    s = s.replace("{{URL_OBRIGADO}}", "/implantodontia-lp/obrigado/")   # dentro da pasta da LP: não mexe no /obrigado/ do WordPress
    s = s.replace("{{URL_PRIVACIDADE}}", SITE + "/privacy-policy/")     # conferido no rodapé do site (nov/2026)
    s = s.replace("{{URL_TERMOS}}", SITE + "/termos-e-condicoes/")      # conferido no rodapé do site (nov/2026)
    for k, (live, base, widths, sizes) in IMG.items():
        v = variants(base, widths)
        if preview:
            src = ("data:image/webp;base64," + base64.b64encode(v[0][1].read_bytes()).decode()) if v else UP + live
            s = s.replace("{{img:%s}}" % k, src).replace("{{imgabs:%s}}" % k, UP + live)
            s = s.replace("{{srcset:%s}}" % k, "").replace("{{presrcset:%s}}" % k, "")
            continue
        url = lambda f: f"{fontprefix}assets/img/{f.name}"
        files = v or [(widths[0], pathlib.Path(f"{base}-{widths[0]}.webp"))]
        s = s.replace("{{img:%s}}" % k, url(files[0][1]))
        s = s.replace("{{imgabs:%s}}" % k, SITE + url(files[-1][1]))
        ss = ", ".join(f"{url(f)} {w}w" for w, f in files)
        s = s.replace("{{srcset:%s}}" % k, f' srcset="{ss}" sizes="{sizes}"' if len(files) > 1 else "")
        s = s.replace("{{presrcset:%s}}" % k, f' imagesrcset="{ss}" imagesizes="{sizes}"' if len(files) > 1 else "")
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
    (DIST / "fonts").mkdir()
    for name, *_ in FONTS:
        shutil.copy(ROOT / "fonts" / name, DIST / "fonts" / name)
    for name in LOGOS:
        shutil.copy(ROOT / "marca" / name, DIST / "assets" / "img" / name)
    # produção: caminhos absolutos a partir da raiz do site (a LP fica em /implantodontia-lp/)
    base = "/implantodontia-lp/"
    (DIST / "index.html").write_text(render(index, preview=False, fontprefix=base), encoding="utf-8")
    (DIST / "obrigado" / "index.html").write_text(render(thanks, preview=False, fontprefix=base), encoding="utf-8")
    for k, (live, base, widths, sizes) in IMG.items():
        for w, f in variants(base, widths):
            shutil.copy(f, DIST / "assets" / "img" / f.name)
    print("ok: preview.html e dist/ gerados")
    missing = sorted({base for _, base, *_ in IMG.values() if not original(base)})
    if missing:
        print("faltam as imagens originais em img-originais/ (o dist/ ainda não tem estas):", ", ".join(missing))

if __name__ == "__main__":
    main()
