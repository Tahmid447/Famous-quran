"""Application tests with controlled publisher data and real synthetic media, not a physical iPhone."""
import base64, json, os, shutil, subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'verification-artifacts'; OUT.mkdir(exist_ok=True)
CLIP=OUT/'synthetic-test.mp4'
provided=os.environ.get('SYNTHETIC_FILE')
if provided:
    shutil.copyfile(provided,CLIP)
else:
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-f','lavfi','-i','color=c=black:s=160x90:r=1:d=1200','-f','lavfi','-i','anullsrc=r=8000:cl=mono','-t','1200','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-b:a','16k','-movflags','+faststart',str(CLIP),'-y'],check=True)
report={'scope':'Chromium application tests with source fixtures and an actual 20-minute synthetic MP4. Not physical iPhone PiP, real YouTube playback, or religious source validation.','checks':[],'errors':[]}
blank=base64.b64decode('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7')
with sync_playwright() as pl:
    opts={'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage']}
    if os.environ.get('BROWSER_PATH'):opts['executable_path']=os.environ['BROWSER_PATH']
    browser=pl.chromium.launch(**opts)
    ctx=browser.new_context(viewport={'width':1440,'height':1000},service_workers='block')
    page=ctx.new_page();page.on('pageerror',lambda e:report['errors'].append(str(e)))
    def route(r):
        u=r.request.url
        if '/api/community-videos?' in u:
            r.fulfill(content_type='application/json',body=json.dumps({'videos':[{'id':'H4N5eFbLl9A','name':'Mishary Rashid Alafasy','title':'Source fixture only','range':'Surah 55 - source fixture'}]}));return
        if '/api/recordings?' in u:
            r.fulfill(content_type='application/json',body=json.dumps({'tracks':[{'name':n,'url':'https://server11.mp3quran.net/x/025.mp3','scope':'full-surah'} for n in ['Mishary Rashid Alafasy','Abdul Rahman Al-Sudais','Abdul Rahman Al-Ossi','Yasser Al-Dosari']]}));return
        if '/api/mushaf?section=' in u:
            r.fulfill(content_type='application/json',body=json.dumps({'images':[{'name':'p363.gif','original':'https://www.equraninstitute.com/quranreading/quraan_images/p363.gif'}]}));return
        if '/api/mushaf?image=' in u:r.fulfill(content_type='image/gif',body=blank);return
        if 'quranenc.com/api/' in u:
            if '/translations/list/' in u:val=[]
            elif '/sura/' in u:
                s=int(u.rsplit('/',1)[1]);val=[{'sura':s,'aya':n,'translation':'Publisher-data fixture. Not a religious quotation.','footnotes':'Fixture note.'} for n in range(1,111)]
            else:
                s,n=map(int,u.rsplit('/',2)[-2:]);val={'sura':s,'aya':n,'translation':'Publisher-data fixture. Not a religious quotation.','footnotes':'Fixture note.'}
            r.fulfill(content_type='application/json',body=json.dumps({'result':val}));return
        if 'api.alquran.cloud' in u:
            r.fulfill(content_type='application/json',body=json.dumps({'data':{'ayahs':[{'numberInSurah':n,'text':'Fixture only','audio':''} for n in range(1,111)]}}));return
        if 'hadeethenc.com/api/' in u:
            r.fulfill(content_type='application/json',body=json.dumps({'id':10113,'hadeeth':'Hadith source fixture, not quotation.','grade':'Fixture grade','explanation':'Fixture explanation'} if 'one/' in u else []));return
        if 'i.ytimg.com' in u:r.fulfill(content_type='image/gif',body=blank);return
        if '127.0.0.1:8765' in u:r.continue_();return
        r.abort()
    ctx.route('**/*',route)
    try:
        page.goto('http://127.0.0.1:8765',wait_until='networkidle')
        assert page.locator('#grid .card').count()==30
        assert page.locator('#completeSurahs .surah-card').count()==7
        assert page.evaluate('window.PASSAGES.length')==37
        report['checks'].append('30 unchanged passage IDs plus seven separate full-surah cards')
        page.click('[data-open="1"]');page.wait_for_selector('#guidePanel.active .source-quote')
        assert page.locator('#guidePanel').is_visible() and not page.locator('#ayahPanel').is_visible()
        for rank in range(1,31):
            page.evaluate('(r)=>Q.open(r)',rank)
            page.wait_for_selector('#guidePanel.active .source-quote')
            assert page.locator('#guidePanel h2').inner_text()
        report['checks'].append('Every original passage opens a source-selected introduction')
        for lang in ['bn','ja','en']:
            page.evaluate('(lang)=>{Q.lang=lang;Q.language()}',lang)
            page.wait_for_selector('#guidePanel.active .source-quote')
            assert page.locator('#guidePanel h2').inner_text()==page.evaluate('FQ_COMMUNITY.guides[29].theme[Q.lang]')
        report['checks'].append('English, Bangla, Japanese guide selection')
        page.evaluate("Q.open(101,'ayahs')")
        page.wait_for_selector('.reading-pages')
        assert page.locator('#ayahPanel .ayah-card').count()==83
        assert page.locator('#ayahPanel .ayah-card:visible').count()==20
        page.click('[data-page-next]');assert page.locator('#ayah-21').is_visible()
        report['checks'].append('Full Ya-Sin has 83 verse entries with 20-verse reading pages')
        page.evaluate('Q.open(103)');page.wait_for_selector('#guidePanel.active .source-quote')
        page.locator('.practice-details').evaluate('(el)=>el.open=true')
        assert 'weak' in page.locator('.practice-details').inner_text()
        assert page.locator('.practice-details a').get_attribute('href').startswith('https://dorar.net/')
        page.evaluate('Q.open(104)');page.wait_for_selector('#guidePanel.active .source-quote')
        page.locator('.practice-details').evaluate('(el)=>el.open=true')
        assert 'Friday Fajr prayer' in page.locator('.practice-details').inner_text()
        report['checks'].append('Weak poverty promise distinguished from sahih Friday-prayer evidence')
        page.evaluate('Q.open(1)');page.wait_for_selector('#guideImport');page.click('#guideImport')
        page.set_input_files('#nativeImport',str(CLIP));page.wait_for_selector('[data-native-open]')
        page.click('[data-native-open]');page.wait_for_function('document.querySelector("#nativeVideo").readyState>=1')
        page.click('#nativePlay');page.wait_for_function('document.querySelector("#nativeVideo").currentTime>0.1')
        v=page.locator('#nativeVideo')
        assert not v.evaluate('(v)=>v.paused') and v.evaluate('(v)=>v.duration')>1199
        parent=v.evaluate('(v)=>v.parentElement.id');src=v.get_attribute('src')
        page.locator('#nativeSeek').fill('750');page.locator('#nativeSeek').dispatch_event('change')
        page.wait_for_function('document.querySelector("#nativeVideo").currentTime>=899')
        t0=v.evaluate('(v)=>v.currentTime')
        page.locator('[data-close="utilityDialog"]').click();page.wait_for_timeout(900)
        assert v.get_attribute('src')==src and not v.evaluate('(v)=>v.paused')
        page.evaluate('Q.open(3)');page.wait_for_timeout(900)
        assert v.get_attribute('src')==src and v.evaluate('(v)=>v.parentElement.id')==parent
        assert v.evaluate('(v)=>v.currentTime')>t0 and not v.evaluate('(v)=>v.paused')
        report['checks'].append('Actual synthetic video plays and seeks to 15:00/20:00; element and source survive utility close and another passage')
        report['nativePiPAvailable']=page.evaluate('document.pictureInPictureEnabled')
        page.click('#nativePip');page.wait_for_timeout(300)
        report['nativePiPEntered']=page.evaluate('document.pictureInPictureElement===document.querySelector("#nativeVideo")')
        if report['nativePiPEntered']:page.evaluate('document.exitPictureInPicture()')
        page.click('#nativeMode');page.wait_for_function('document.querySelector("#nativeAudio").readyState>=1')
        page.click('#nativePlay');page.wait_for_timeout(500)
        assert not page.locator('#nativeAudio').evaluate('(a)=>a.paused')
        assert page.locator('#nativeVideo').evaluate('(v)=>v.paused')
        report['checks'].append('Same MP4 audio track plays through native audio; video decoder is stopped')
        page.locator('#nativeClose').click()
        page.set_viewport_size({'width':390,'height':844})
        page.evaluate('Q.open(105)');page.wait_for_selector('#guidePanel.active')
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        report['checks'].append('390px viewport has no document horizontal overflow')
        assert not report['errors'],report['errors']
    except Exception as e:
        report['failure']=str(e);page.screenshot(path=str(OUT/'community-failure.png'));raise
    finally:
        (OUT/'community-browser.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        ctx.close();browser.close()
print(json.dumps(report,indent=2))
