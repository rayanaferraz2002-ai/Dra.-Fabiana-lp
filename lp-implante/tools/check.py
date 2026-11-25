#!/usr/bin/env python3
"""Confere o preview.html no celular (375x812) e no desktop. Rode depois de `python3 build.py`.
Saídas: métricas em JSON e screenshots em tools/out/."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _chrome import launch, sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "tools" / "out"; OUT.mkdir(parents=True, exist_ok=True)
URL = (ROOT / "preview.html").as_uri()

JS = """() => {
  const r = s => { const e=document.querySelector(s); if(!e) return null; const b=e.getBoundingClientRect(); return {top:Math.round(b.top+scrollY), bottom:Math.round(b.bottom+scrollY)} };
  return { viewportH: innerHeight, docH: document.documentElement.scrollHeight,
           overflowX: document.documentElement.scrollWidth > innerWidth,
           h1: document.querySelectorAll('h1').length,
           whatsapp: r('#hero-cta .btn-wa'), ligar: r('#hero-cta .btn-line'),
           fontes: [...new Set([...document.querySelectorAll('body *')].map(e=>getComputedStyle(e).fontFamily.split(',')[0]))],
           imgsSemAlt: [...document.querySelectorAll('img')].filter(i=>!i.alt).length,
           heroLazy: document.querySelector('.hero-photo img').loading === 'lazy' }
}"""

def main():
    res = {}
    with sync_playwright() as p:
        b = launch(p)
        for name, vp, mobile in (("mobile", {"width": 375, "height": 812}, True), ("desktop", {"width": 1280, "height": 800}, False)):
            ctx = b.new_context(viewport=vp, device_scale_factor=2 if mobile else 1, is_mobile=mobile, has_touch=mobile)
            pg = ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.route("**/*", lambda r: r.abort() if r.request.url.startswith("http") else r.continue_())  # sem rede: imagens ficam cinza
            pg.goto(URL, wait_until="load"); pg.wait_for_timeout(400)
            m = pg.evaluate(JS); m["erros_js"] = errs
            if mobile:
                m["barra_fixa_no_topo"] = pg.evaluate("document.getElementById('bar').classList.contains('show')")
                pg.evaluate("scrollTo(0,1600)"); pg.wait_for_timeout(300)
                m["barra_fixa_apos_rolar"] = pg.evaluate("document.getElementById('bar').classList.contains('show')")
                pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(200)
                m["WHATSAPP_NA_PRIMEIRA_TELA"] = bool(m["ligar"] and m["ligar"]["bottom"] <= m["viewportH"])
            pg.screenshot(path=str(OUT / f"{name}-topo.png"))
            pg.screenshot(path=str(OUT / f"{name}-pagina-toda.png"), full_page=True)
            res[name] = m; ctx.close()
        b.close()
    print(json.dumps(res, indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main()
