"""Read-only live browser checks. Do not treat embedding metadata as playback."""
import json, time, urllib.request
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];out=root/'verification-artifacts';out.mkdir(exist_ok=True)
report={'scope':'Read-only playback checks with normal YouTube embeds. No downloads, authentication bypass or alternate endpoints.','localVideos':[],'deployments':[]}
def public_json(url):
 req=urllib.request.Request(url,headers={'User-Agent':'FamousQuran-Verification','Accept':'application/vnd.github+json'})
 with urllib.request.urlopen(req,timeout=12) as r:return json.load(r)
try:
 deployments=public_json('https://api.github.com/repos/Tahmid447/Famous-quran/deployments?environment=Production&per_page=3')
 for d in deployments:
  for st in public_json(d['statuses_url']+'?per_page=2'):
   url=st.get('environment_url') or st.get('target_url')
   if url and st.get('state')=='success' and urlparse(url).scheme=='https':
    report['deployments'].append({'url':url,'sha':d.get('sha')});break
except Exception as e:report['deploymentDiscoveryError']=str(e)
with sync_playwright() as pl:
 browser=pl.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 ctx=browser.new_context(viewport={'width':1440,'height':1000});p=ctx.new_page()
 try:
  p.goto('http://127.0.0.1:8765',wait_until='domcontentloaded');p.click('[data-recordings="1"]');p.wait_for_selector('[data-clip]')
  ids=p.locator('[data-clip]').evaluate_all('(xs)=>xs.map(x=>x.dataset.clip)')
  for id in ids:
   p.locator('[data-clip="'+id+'"]').click();p.click('#v3Start');start=time.monotonic();status=''
   while time.monotonic()-start<16:
    p.wait_for_timeout(800);status=p.locator('#v3PlayerStatus').inner_text()
    if 'Playing' in status or any('('+str(c)+')' in status for c in [100,101,150,153]):break
   report['localVideos'].append({'id':id,'status':status,'iframe':p.locator('#fqYouTubeFrame').count(),'playingObserved':status=='Playing'})
   if status=='Playing':p.screenshot(path=str(out/('playing-'+id+'.png')))
 except Exception as e:report['localError']=str(e)
 seen=set();report['hosted']=[]
 for d in report['deployments']:
  url=d['url']
  if url in seen:continue
  seen.add(url);entry=dict(d)
  try:
   r=p.goto(url,wait_until='domcontentloaded',timeout=30000);entry['http']=r.status;entry['finalUrl']=p.url
   if r.status==200 and p.locator('[data-recordings="1"]').count():
    og=p.locator('meta[property="og:url"]');entry['canonical']=og.get_attribute('content') if og.count() else None
    p.click('[data-recordings="1"]');p.wait_for_timeout(2000)
    if p.locator('#v3Start').count():
     p.click('#v3Start');p.wait_for_timeout(16000);entry['videoStatus']=p.locator('#v3PlayerStatus').inner_text();entry['videoTitle']=p.locator('#v3Title').inner_text()
     p.screenshot(path=str(out/'actual-hosted-video.png'))
   report['hosted'].append(entry)
  except Exception as e:entry['error']=str(e);report['hosted'].append(entry)
  if len(report['hosted'])>=2:break
 browser.close()
(out/'embed-audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
