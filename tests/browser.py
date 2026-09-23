import json,base64
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];out=root/'verification-artifacts';out.mkdir(exist_ok=True)
report={'scope':'Real application with controlled network fixtures; not live video playback','checks':[]};blank=base64.b64decode('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7')
with sync_playwright() as pl:
 browser=pl.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 ctx=browser.new_context(viewport={'width':1440,'height':1000},color_scheme='light',service_workers='block');page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 def intercept(r):
  u=r.request.url
  if '/api/recordings?' in u:
   r.fulfill(content_type='application/json',body=json.dumps({'tracks':[{'name':n,'url':'https://server11.mp3quran.net/t'+str(i)+'/025.mp3','scope':'full-surah'} for i,n in enumerate(['Mishary Rashid Alafasy','Abdul Rahman Al-Sudais','Abdul Rahman Al-Ossi','Yasser Al-Dosari'])]}));return
  if '/api/mushaf?section=' in u:
   r.fulfill(content_type='application/json',body=json.dumps({'images':[{'name':n,'url':'/api/mushaf?image='+n,'original':'https://www.equraninstitute.com/quranreading/quraan_images/'+n} for n in ['p363.gif','p364.gif','p365.gif','p366.gif','p367_1.gif']]}));return
  if '/api/mushaf?image=' in u:r.fulfill(content_type='image/gif',body=blank);return
  if '127.0.0.1:8765' in u:r.continue_();return
  if 'iframe_api' in u:r.fulfill(content_type='text/javascript',body='window.YT={Player:class{constructor(id,o){this.id=id;this.o=o;this.t=120;this.s=1;this.v=100;window.__lastYT=this;setTimeout(()=>{o.events.onReady();o.events.onStateChange?.({data:1})},1)}destroy(){document.getElementById(this.id)?.remove()}getCurrentTime(){return this.t}getDuration(){return 1200}seekTo(v){this.t=Number(v)||0}getVolume(){return this.v}setVolume(v){this.v=Number(v)||0}getPlayerState(){return this.s}playVideo(){this.s=1;this.o.events.onStateChange?.({data:1})}pauseVideo(){this.s=2;this.o.events.onStateChange?.({data:2})}}};window.onYouTubeIframeAPIReady?.();');return
  if 'youtube-nocookie.com/embed/' in u:r.fulfill(content_type='text/html',body='<html><body>Network fixture, not real video</body></html>');return
  if 'i.ytimg.com' in u:r.fulfill(content_type='image/gif',body=blank);return
  if 'quranenc.com/api/' in u:r.fulfill(content_type='application/json',body='{"result":[]}');return
  if 'api.alquran.cloud' in u:r.fulfill(content_type='application/json',body='{"data":{"ayahs":[]}}');return
  r.abort()
 ctx.route('**/*',intercept)
 try:
  page.goto('http://127.0.0.1:8765',wait_until='networkidle');assert page.locator('#grid .card').count()==30;report['checks'].append('30 passages render')
  page.select_option('#themeMode','dark');assert page.locator('html').get_attribute('data-theme')=='dark';page.select_option('#themeMode','light');page.reload(wait_until='networkidle');assert page.locator('html').get_attribute('data-theme')=='light';report['checks'].append('Light/dark switch and persisted theme')
  page.evaluate("localStorage.setItem('fq:passage:25:63\u201377','Existing note preserved')")
  page.click('[data-open="1"]')
  page.wait_for_selector('#ayahReciter')
  assert page.locator('#ayahReciter option').all_text_contents()==['Mishary Rashid Alafasy','Abdul Rahman Al-Sudais','Abdul Rahman Al-Ossi','Yasser Al-Dosari'], 'reciter options mismatch: '+str(page.locator('#ayahReciter option').all_text_contents())
  page.select_option('#ayahReciter','mp3:ossi');page.wait_for_timeout(250)
  assert page.locator('[data-play]').count()>0, 'no play buttons rendered'
  assert 'complete-surah' in page.locator('#ayahPanel').inner_text().lower(), 'full-surah safety notice missing: '+page.locator('#ayahPanel').inner_text()[:300]
  page.evaluate("Q.currentPlayback={kind:'full',rank:1,surah:25,surahName:'Al-Furqan',reciterName:'Abdul Rahman Al-Ossi'};Q.updatePlayback()")
  assert not page.locator('#persistentPlayer').is_hidden(), 'persistent audio player did not show'
  page.evaluate("Object.defineProperty(document.querySelector('#ayahPlayer'),'duration',{value:1200,configurable:true});document.querySelector('#ayahPlayer').currentTime=120;Q.updatePlayback()")
  assert page.locator('#miniSeek').count()==1 and page.locator('#miniVolume').count()==1
  page.locator('#miniSeek').fill('500');page.locator('#miniSeek').dispatch_event('change');assert abs(page.locator('#ayahPlayer').evaluate('(e)=>e.currentTime')-600)<2
  page.locator('#miniVolume').fill('35');page.locator('#miniVolume').dispatch_event('input');assert abs(page.locator('#ayahPlayer').evaluate('(e)=>e.volume')-.35)<.05
  report['checks'].append('Floating audio seek and volume controls')
  mb1=page.locator('#persistentPlayer').bounding_box();mh=page.locator('#miniDrag').bounding_box()
  page.mouse.move(mh['x']+10,mh['y']+10);page.mouse.down();page.mouse.move(mh['x']+90,mh['y']+65,steps=6);page.mouse.up();page.wait_for_timeout(80)
  mb2=page.locator('#persistentPlayer').bounding_box()
  assert abs(mb2['x']-mb1['x'])>15 or abs(mb2['y']-mb1['y'])>15, 'audio mini did not drag: '+str((mb1,mb2))
  page.click('[data-close="studyDialog"]');page.wait_for_timeout(120)
  assert not page.locator('#persistentPlayer').is_hidden(), 'audio mini disappeared after dialog close'
  report['checks'].append('Requested four reciters; Ossi/Dosari safe full-surah mode; draggable mini-player survives dialog close')
  page.evaluate("Q.open(1,'recordings')");page.wait_for_timeout(800);assert page.locator('.v3-audio-card').count()>0, 'recording catalogue failed: '+str(page.locator('#v3Tracks').get_attribute('data-error'))+' / '+page.locator('#v3Tracks').inner_text();assert page.locator('#v3Title').inner_text().startswith('Qari Ibrahim Idris');assert page.locator('.v3-video-choice').count()==6;assert page.locator('#videoSelect').count()==0;assert 'Al-Ossi' in page.locator('#v3Tracks').inner_text();assert page.locator('.v3-audio-card audio[src]').count()==4;assert page.locator('[data-full-play]').first.inner_text()=='Background audio';report['checks'].append('Ibrahim first, six source videos, requested reciters, native publisher audio sources and no unrelated catalogue')
  page.click('#v3Start');page.wait_for_selector('#fqYouTubeFrame');frame=page.locator('#fqYouTubeFrame');assert '/K1cA-E6MoBU?' in frame.get_attribute('src');assert 'origin=http%3A%2F%2F127.0.0.1%3A8765' in frame.get_attribute('src');assert frame.get_attribute('referrerpolicy')=='strict-origin-when-cross-origin';assert frame.bounding_box()['height']>=200;assert page.locator('#v3SystemPip').get_attribute('href').startswith('https://www.youtube.com/watch?v=');report['checks'].append('Visible correct iframe, origin/referrer, source/system-PiP handoff and controls; fixture only');page.wait_for_timeout(50);page.click('#v3FloatVideo');page.wait_for_selector('#videoFloatPlayer:not([hidden])');assert page.locator('#fqYouTubeFloatFrame').count()==1;page.wait_for_timeout(80);assert page.locator('#videoFloatSeek').count()==1 and page.locator('#videoFloatVolume').count()==1;page.locator('#videoFloatSeek').fill('500');page.locator('#videoFloatSeek').dispatch_event('change');assert abs(page.evaluate('window.__lastYT.t')-600)<2;page.locator('#videoFloatVolume').fill('40');page.locator('#videoFloatVolume').dispatch_event('input');assert page.evaluate('window.__lastYT.v')==40;report['checks'].append('Floating YouTube seek and volume controls');box1=page.locator('#videoFloatPlayer').bounding_box();h=page.locator('#videoFloatDrag').bounding_box();page.mouse.move(h['x']+25,h['y']+15);page.mouse.down();page.mouse.move(h['x']-95,h['y']-85,steps=6);page.mouse.up();box2=page.locator('#videoFloatPlayer').bounding_box();assert abs(box2['x']-box1['x'])>20 or abs(box2['y']-box1['y'])>20;page.click('[data-close="studyDialog"]');page.wait_for_timeout(180);assert not page.locator('#videoFloatPlayer').is_hidden();report['checks'].append('YouTube float/PiP survives dialog close and is draggable');page.click('#videoFloatDock');page.wait_for_selector('#studyDialog[open]');page.wait_for_selector('#fqYouTubeFrame');assert page.locator('#videoFloatPlayer').is_hidden();report['checks'].append('Floating video docks back into recordings view')
  page.click('[data-v3-mushaf]');page.wait_for_selector('.mushaf-page');assert page.locator('.mushaf-page').count()==5;page.locator('#mushafZoom').fill('140');page.locator('#mushafZoom').dispatch_event('input');assert '140%' in page.locator('#mushafPages').get_attribute('style');page.click('#mushafWide');assert 'wide-reader' in page.locator('#studyDialog').get_attribute('class');page.click('#mushafBack');assert 'wide-reader' not in page.locator('#studyDialog').get_attribute('class');assert page.input_value('#passageNotes')=='Existing note preserved';report['checks'].append('In-site scans, zoom, wide mode, back, notes preservation')
  page.click('[data-close="studyDialog"]');page.click('[data-lang="ja"]');assert page.locator('html').get_attribute('lang')=='ja';assert page.locator('[data-lang="hi"]').count()==0;assert page.locator('#themeLabel').inner_text()=='表示設定';page.click('[data-lang="bn"]');assert page.locator('html').get_attribute('lang')=='bn';report['checks'].append('English Bangla Japanese and translated controls')
  page.click('[data-lang="en"]');page.set_viewport_size({'width':390,'height':844});page.click('[data-recordings="1"]');page.wait_for_selector('.v3-audio-card');assert page.locator('#studyDialog').bounding_box()['width']<=390;assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');report['checks'].append('390px mobile viewport has no page overflow');assert not errors,errors;report['checks'].append('No JavaScript errors in regression flows')
 finally:report['errors']=errors;(out/'browser-report.json').write_text(json.dumps(report,indent=2));ctx.close()
 # No stubbing in this context. Real API data, image bytes, media and browser storage.
 live={'scope':'Real browser and live public services, local test origin','errors':[]};ctx=browser.new_context(viewport={'width':1440,'height':1000},color_scheme='light');page=ctx.new_page();page.on('pageerror',lambda e:live['errors'].append(str(e)))
 try:
  page.goto('http://127.0.0.1:8765',wait_until='domcontentloaded');page.wait_for_selector('#grid .card');page.select_option('#themeMode','light');page.screenshot(path=str(out/'actual-home-light.png'))
  page.click('[data-recordings="1"]');page.wait_for_timeout(16000);live['featured']=page.locator('#v3Title').inner_text();live['reciters']=page.locator('#v3Tracks').inner_text();page.screenshot(path=str(out/'actual-recordings-light.png'));page.locator('[data-full-play]').first.click();page.wait_for_timeout(3500);before=page.locator('#ayahPlayer').evaluate('(e)=>e.currentTime');live['persistentPlayerVisible']=not page.locator('#persistentPlayer').is_hidden();page.click('[data-close="studyDialog"]');page.wait_for_timeout(1800);after=page.locator('#ayahPlayer').evaluate('(e)=>e.currentTime');live['persistentAfterClose']={'before':before,'after':after,'visible':not page.locator('#persistentPlayer').is_hidden(),'paused':page.locator('#ayahPlayer').evaluate('(e)=>e.paused')};page.click('[data-recordings="1"]');page.wait_for_timeout(1000)
  page.click('#v3Start');page.wait_for_timeout(12000);live['playerStatus']=page.locator('#v3PlayerStatus').inner_text();live['iframeCount']=page.locator('#fqYouTubeFrame').count();page.screenshot(path=str(out/'actual-player-light.png'))
  float_btn=page.locator('#v3FloatVideo');live['floatButtonVisible']=float_btn.count()==1
  if float_btn.count()==1:
   float_btn.click();page.wait_for_timeout(1200);live['floatingVideo']={'visible':not page.locator('#videoFloatPlayer').is_hidden(),'iframe':page.locator('#fqYouTubeFloatFrame').count()};page.screenshot(path=str(out/'actual-video-float-light.png'));page.locator('#videoFloatClose').click()
  audio=[]
  for i in range(page.locator('[data-full-play]').count()):
   page.locator('[data-full-play]').nth(i).click();page.wait_for_timeout(2500);audio.append(page.locator('#ayahPlayer').evaluate('(e)=>({currentTime:e.currentTime,readyState:e.readyState,paused:e.paused,error:e.error?.code||null,src:e.currentSrc})'))
  live['audioPlayback']=audio
  if audio:
   page.locator('[data-full-save]').first.click();page.wait_for_function("!document.querySelector('[data-full-save]').disabled",timeout=125000);live['audioSave']=page.locator('#v3AudioStatus0').inner_text();ctx.set_offline(True);page.locator('[data-full-play]').first.click();page.wait_for_timeout(3000);live['savedAudioOffline']=page.locator('#ayahPlayer').evaluate('(e)=>({src:e.currentSrc,time:e.currentTime,paused:e.paused,error:e.error?.code||null})');ctx.set_offline(False)
  page.click('[data-v3-mushaf]');page.wait_for_timeout(15000);live['scans']=page.locator('.mushaf-page img').evaluate_all('(xs)=>xs.map(x=>({src:x.src,loaded:x.complete&&x.naturalWidth>0,width:x.naturalWidth}))');page.click('#mushafWide');page.screenshot(path=str(out/'actual-mushaf-light.png'));page.click('#mushafSave');page.wait_for_function("!document.querySelector('#mushafSave').disabled",timeout=45000);live['scanSave']=page.locator('#mushafStatus').inner_text();page.click('#mushafBack');page.click('[data-close="studyDialog"]');page.select_option('#themeMode','dark');page.click('[data-recordings="1"]');page.wait_for_timeout(1000);page.screenshot(path=str(out/'actual-recordings-dark.png'))
 except Exception as e:live['exception']=str(e)
 finally:(out/'live-browser.json').write_text(json.dumps(live,indent=2));browser.close()
print(json.dumps(report,indent=2));print(json.dumps(live,indent=2))
