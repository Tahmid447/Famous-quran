import json,base64
from pathlib import Path
from playwright.sync_api import sync_playwright

blank=base64.b64decode('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7')
out=Path('verification-artifacts');out.mkdir(exist_ok=True)

with sync_playwright() as pl:
    device=dict(pl.devices['iPhone 13'])
    device.pop('default_browser_type',None)
    browser=pl.webkit.launch(headless=True)
    ctx=browser.new_context(**device,service_workers='block')
    page=ctx.new_page()
    errors=[]
    page.on('pageerror',lambda e: errors.append(str(e)))

    def route(r):
        u=r.request.url
        if '/api/recordings?' in u:
            tracks=[{'name':n,'url':'https://server11.mp3quran.net/t'+str(i)+'/025.mp3','scope':'full-surah'} for i,n in enumerate(['Mishary Rashid Alafasy','Abdul Rahman Al-Sudais','Abdul Rahman Al-Ossi','Yasser Al-Dosari'])]
            r.fulfill(content_type='application/json',body=json.dumps({'tracks':tracks}));return
        if '127.0.0.1:8765' in u:r.continue_();return
        if 'i.ytimg.com' in u:r.fulfill(content_type='image/gif',body=blank);return
        if 'quranenc.com/api/' in u:r.fulfill(content_type='application/json',body='{"result":[]}');return
        if 'api.alquran.cloud' in u:r.fulfill(content_type='application/json',body='{"data":{"ayahs":[]}}');return
        r.abort()

    ctx.route('**/*',route)
    page.goto('http://127.0.0.1:8765',wait_until='domcontentloaded')
    page.click('[data-recordings="1"]')
    page.wait_for_selector('.v3-audio-card audio[src]')
    assert page.locator('.v3-audio-card audio[src]').count()==4
    first=page.locator('.v3-audio-card audio').first
    assert first.get_attribute('src').startswith('https://')
    assert first.get_attribute('playsinline') is not None
    assert page.locator('[data-full-play]').first.inner_text()=='Background audio'

    # The iOS-safe path must invoke play synchronously from the user gesture before IndexedDB.
    page.evaluate("""() => {
      window.__fqOrder=[];
      const p=document.querySelector('#ayahPlayer');
      p.play=()=>{window.__fqOrder.push('play');return Promise.resolve()};
      Q.idb=async()=>{window.__fqOrder.push('idb');await new Promise(r=>setTimeout(r,25));return null};
      Q.play(p,'https://server11.mp3quran.net/t0/025.mp3');
    }""")
    page.wait_for_timeout(80)
    order=page.evaluate('window.__fqOrder')
    assert order and order[0]=='play', order

    # Floating audio controls are present and touch-sized on the iPhone viewport.
    page.evaluate("""() => {
      Q.currentPlayback={kind:'full',rank:1,surah:25,surahName:'Al-Furqan',reciterName:'Mishary Rashid Alafasy'};
      const p=document.querySelector('#ayahPlayer');
      Object.defineProperty(p,'duration',{value:1200,configurable:true});
      p.currentTime=120;
      Q.updatePlayback();
    }""")
    assert page.locator('#miniSeek').count()==1
    assert page.locator('#miniVolume').count()==1
    box=page.locator('#persistentPlayer').bounding_box()
    assert box and box['width'] <= device['viewport']['width']

    result={'device':'Playwright WebKit with iPhone 13 profile','gestureOrder':order,'nativeAudioCards':4,'miniSeek':True,'miniVolume':True,'pageErrors':errors}
    (out/'ios-webkit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    assert not errors, errors
    ctx.close();browser.close()

print('iPhone WebKit media smoke: OK')
