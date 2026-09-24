from playwright.sync_api import sync_playwright
import os,glob
for f in glob.glob('laminas/*.png'): os.remove(f)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg=b.new_page(viewport={'width':1080,'height':1350})
    pg.goto('file://'+os.path.abspath('presentacion-angelica.html'),wait_until='networkidle')
    pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(800)
    pg.pdf(path='Plan_Angelica_Garcia.pdf',width='1080px',height='1350px',print_background=True)
    for i,s in enumerate(pg.query_selector_all('section.s'),1): s.screenshot(path=f'laminas/{i:02d}.png')
    print(pg.evaluate("""[...document.querySelectorAll('section.s')].map((s,i)=>{let m=0;const sr=s.getBoundingClientRect();s.querySelectorAll('*').forEach(e=>{if(e.closest('.num,.brand'))return;const r=e.getBoundingClientRect();m=Math.max(m,r.bottom-sr.top)});return (i+1)+':'+Math.round(m)}).join(' ')"""))
    b.close()
