import json,base64
from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path(__file__).resolve().parents[1]/'verification-artifacts';out.mkdir(exist_ok=True)
blank=base64.b64decode('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7')
report={'scope':'Playwright WebKit at iPhone size; checks Safari/WebKit DOM and tap-triggered media path, not physical-iPhone background suspension','checks':[],'errors':[]}
with sync_playwright() as p:
 browser=p.webkit.launch(headless=True)
 ctx=browser.new_context(viewport={'width':390,'height':844},user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1',service_workers='block')
 page=ctx.new_page();page.on('pageerror',lambda e:report['errors'].append(str(e)))
 page.add_init_script("""HTMLMediaElement.prototype.play=function(){this.dataset.playCalled='1';return Promise.resolve()};HTMLMediaElement.prototype.pause=function(){};HTMLMediaElement.prototype.load=function(){};""")
 def route(r):
  u=r.request.url
  if '127.0.0.1:8765' in u:r.continue_();return
  if '/api/recordings?' in u:
   if 'kind=native' in u:r.fulfill(content_type='application/json',body=json.dumps({'videos':[{'name':'Yasser Al-Dosari','title':'Publisher direct video','url':'https://www.mp3quran.net/uploads/videos/group1_pbuh/test.mp4','scope':'publisher-direct-mp4'}]}));return
   r.fulfill(content_type='application/json',body=json.dumps({'tracks':[{'name':n,'url':'https://server11.mp3quran.net/t'+str(i)+'/025.mp3','scope':'full-surah'} for i,n in enumerate(['Mishary Rashid Alafasy','Abdul Rahman Al-Sudais','Abdul Rahman Al-Ossi','Yasser Al-Dosari'])]}));return
  if '/api/mushaf?' in u:r.fulfill(content_type='application/json',body=json.dumps({'images':[]}));return
  if 'quranenc.com/api/' in u:r.fulfill(content_type='application/json',body='{"result":[]}');return
  if 'api.alquran.cloud' in u:r.fulfill(content_type='application/json',body='{"data":{"ayahs":[]}}');return
  if 'i.ytimg.com' in u:r.fulfill(content_type='image/gif',body=blank);return
  r.abort()
 ctx.route('**/*',route)
 page.goto('http://127.0.0.1:8765',wait_until='domcontentloaded');page.wait_for_selector('#grid .card')
 page.click('[data-recordings="1"]');page.wait_for_selector('[data-full-play]')
 page.locator('[data-full-play]').first.click();page.wait_for_timeout(30)
 audio=page.locator('#ayahPlayer')
 assert audio.get_attribute('data-play-called')=='1','tap did not invoke HTMLMediaElement.play'
 assert '025.mp3' in (audio.get_attribute('src') or ''),'audio src was not assigned synchronously'
 assert page.locator('#v3Tracks audio').count()==0,'dead per-card audio control remains'
 assert page.locator('#v3NativeVideo').count()==1,'native publisher video surface missing'
 assert page.locator('#v3NativePip').count()==1,'System PiP control missing'
 assert page.locator('#studyDialog').bounding_box()['width']<=390
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 report['checks']+=['Publisher audio play() is invoked from the tap path','No dead per-card audio controls','Native HTML5 video and System PiP control render','iPhone-size layout fits']
 assert not report['errors'],report['errors']
 (out/'webkit-ios-report.json').write_text(json.dumps(report,indent=2))
 ctx.close();browser.close()
print(json.dumps(report,indent=2))
