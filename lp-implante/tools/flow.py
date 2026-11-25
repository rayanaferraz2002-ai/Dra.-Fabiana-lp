#!/usr/bin/env python3
"""Testa o fluxo de conversão na versão de produção (dist/): UTMs, formulário, consentimento,
e a regra de que /obrigado/ só gera `lead_confirmado` depois de um envio real. Rode depois de `python3 build.py`."""
import json, pathlib, sys, threading, http.server, socketserver
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _chrome import launch, sync_playwright

DIST = pathlib.Path(__file__).resolve().parent.parent / "dist"
PORT = 8765; BASE = f"http://localhost:{PORT}"

class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = path.split("?")[0].split("#")[0]
        if path.startswith("/implantodontia-lp"): rel = path[len("/implantodontia-lp"):]
        elif path.startswith("/obrigado"): rel = "/obrigado" + path[len("/obrigado"):]
        else: rel = "/__nada__"
        p = DIST / rel.lstrip("/")
        return str(p / "index.html") if p.is_dir() else str(p)
    def log_message(self, *a): pass

def ev(pg): return [e.get("event") for e in pg.evaluate("window.dataLayer") if e.get("event")]

def main():
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("", PORT), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
    res = {}
    with sync_playwright() as p:
        b = launch(p); ctx = b.new_context(viewport={"width": 375, "height": 812}, is_mobile=True, has_touch=True)
        wa = []   # tentativas de abrir o WhatsApp (bloqueadas no teste, só registradas)
        planilha = []   # envios ao Apps Script (bloqueados no teste: nenhum lead falso vai para a planilha)
        def route(r):
            if r.request.url.startswith(BASE): return r.continue_()
            if "wa.me/" in r.request.url: wa.append(r.request.url)
            if "script.google.com/macros/" in r.request.url: planilha.append((r.request.method, r.request.post_data or ""))
            r.abort()
        ctx.route("**/*", route)
        pg = ctx.new_page()
        pg.goto(BASE + "/implantodontia-lp/obrigado/"); pg.wait_for_timeout(300)
        res["1_obrigado_direto_NAO_pode_ter_lead_confirmado"] = ev(pg)
        pg.wait_for_timeout(2700); res["1_obrigado_direto_NAO_abre_whatsapp"] = len(wa) == 0
        res["1_obrigado_noindex"] = pg.evaluate("document.querySelector('meta[name=robots]').content")
        pg.goto(BASE + "/implantodontia-lp/?utm_source=Google+Ads&utm_medium=Pesquisa&utm_campaign=Teste&gclid=ABC123"); pg.wait_for_timeout(300)
        pg.evaluate("document.addEventListener('click',e=>{if(e.target.closest('a[data-wa],a[href^=tel]'))e.preventDefault()},true)")
        pg.click("#hero-cta .btn-wa"); pg.click("#hero-cta .btn-line")
        res["2_eventos_de_clique"] = ev(pg)
        pg.evaluate("document.getElementById('form-lead').scrollIntoView()")
        pg.click("#form-lead button[type=submit]"); res["3_envio_vazio"] = pg.inner_text("#f-status")
        pg.fill("#f-nome", "Teste"); pg.fill("#f-tel", "(11) 91234-5678"); pg.select_option("#f-int", "Prótese protocolo")
        pg.click("#form-lead button[type=submit]"); res["3_sem_consentimento"] = pg.inner_text("#f-status")
        res["4_utms_no_formulario"] = pg.evaluate("Object.fromEntries([...document.querySelectorAll('#form-lead input[type=hidden]')].map(i=>[i.name,i.value]))")
        pg.evaluate("window.open=function(){return null}"); pg.check("#f-ok")
        with pg.expect_navigation(url=BASE + "/implantodontia-lp/obrigado/"):
            pg.click("#form-lead button[type=submit]")
        pg.wait_for_timeout(300); res["5_obrigado_apos_envio_DEVE_ter_lead_confirmado"] = ev(pg)
        pg.wait_for_timeout(2700)
        from urllib.parse import unquote
        endpoint = (DIST / "index.html").read_text(encoding="utf-8").split("var ENDPOINT='")[1].split("'")[0]
        res["5c_envia_para_planilha"] = ("sem ENDPOINT" if not endpoint else
            any(m == "POST" and '"nome":"Teste"' in body and '"gclid":"ABC123"' in body for m, body in planilha))
        res["5b_abre_whatsapp_com_as_respostas"] = unquote(wa[-1].split("text=")[1]) if wa else "NÃO ABRIU"
        n = len(wa); pg.goto(BASE + "/implantodontia-lp/obrigado/"); pg.wait_for_timeout(2700)
        res["6_voltar_ao_obrigado_NAO_conta_de_novo"] = ev(pg); res["6_nem_abre_whatsapp_de_novo"] = len(wa) == n
        b.close()
    srv.shutdown()
    print(json.dumps(res, indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main()
