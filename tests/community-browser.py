"""Local UI and synthetic-media tests. Not a physical iPhone or live YouTube test."""
import json, subprocess, shutil, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('verification-artifacts');out.mkdir(exist_ok=True)
report={'scope':'Controlled fixtures and a synthetic MP4; not physical iPhone PiP','checks':[],'errors':[]}
with sync_playwright() as pl:
    binary=shutil.which('google-chrome') or shutil.which('google-chrome-stable') or shutil.which('chromium')
    browser=pl.chromium.launch(headless=True,**({'executable_path':binary} if binary else {}))
    report['browser']=binary or 'Playwright Chromium'
    ctx=browser.new_context(viewport={'width':390,'height':844},has_touch=True,service_workers='block')
    page=ctx.new_page();page.on('pageerror',lambda e:report['errors'].append(str(e)))
    def intercept(route):
        url=route.request.url
        if '/api/recordings?' in url:
            route.fulfill(content_type='application/json',body=json.dumps({'tracks':[]}));return
        if '127.0.0.1:8765' in url:route.continue_();return
        if 'quranenc.com/api/' in url:route.fulfill(content_type='application/json',body='{"result":[]}');return
        if 'api.alquran.cloud' in url:route.fulfill(content_type='application/json',body='{"data":{"ayahs":[]}}');return
        route.abort()
    ctx.route('**/*',intercept)
    try:
        page.goto('http://127.0.0.1:8765',wait_until='networkidle')
        assert page.locator('#grid .card').count()==30
        assert page.locator('#completeGrid .card').count()==6
        report['checks'].append('Original 30 and six complete-surah cards coexist')
        for lang in ['en','bn','ja']:
            page.click('[data-lang="'+lang+'"]')
            for rank in [1,15,31,33,34,35,36]:
                page.evaluate('(rank)=>Q.open(rank)',rank)
                page.wait_for_selector('#summary .reading-guide')
                assert page.locator('#summary .reading-guide').get_attribute('lang')==lang
                assert page.locator('#summary .reading-guide p').first.inner_text().strip()
                assert 'quranenc.com' in page.locator('#summary a').first.get_attribute('href')
                page.click('[data-close="studyDialog"]')
        report['checks'].append('English, Bangla and Japanese guides, sources and complete-surah navigation')
        page.click('[data-lang="en"]')
        page.evaluate("Q.open(31,'recordings')")
        page.wait_for_selector('#passageMediaFile',state='attached')
        assert 'this device' in page.locator('#nativeFileBox').inner_text()
        report['checks'].append('Permission-aware file import stays local')
        if not shutil.which('ffmpeg'):
            raise RuntimeError('FFmpeg is required; native playback must be tested')
        with tempfile.TemporaryDirectory() as temp:
            clip=Path(temp)/'synthetic-test.mp4'
            subprocess.run(['ffmpeg','-loglevel','error','-f','lavfi','-i','color=c=black:s=160x90:r=10','-f','lavfi','-i','sine=frequency=220:sample_rate=22050','-t','8','-c:v','libx264','-profile:v','baseline','-pix_fmt','yuv420p','-c:a','aac','-b:a','24k','-movflags','+faststart',str(clip)],check=True,timeout=30)
            page.locator('#passageMediaFile').set_input_files(str(clip))
            page.wait_for_selector('#nativeMediaDock:not([hidden])')
            report['codecSupport']=page.locator('#nativeVideo').evaluate("(v)=>v.canPlayType('video/mp4; codecs=\"avc1.42E01E, mp4a.40.2\"')")
            page.click('#nativeVideoMode')
            try:
                page.wait_for_function("document.querySelector('#nativeVideo').readyState>=2 && !document.querySelector('#nativeVideo').paused",timeout=15000)
            except Exception:
                report['mediaFailure']=page.locator('#nativeVideo').evaluate('(v)=>({readyState:v.readyState,networkState:v.networkState,error:v.error?.message,src:v.currentSrc})')
                report['mediaStatus']=page.locator('#nativeStatus').inner_text()
                page.screenshot(path=str(out/'native-media-failure.png'))
                raise
            page.wait_for_timeout(800)
            before=page.locator('#nativeVideo').evaluate('(v)=>v.currentTime')
            page.click('[data-close="studyDialog"]');page.wait_for_timeout(700)
            after=page.locator('#nativeVideo').evaluate('(v)=>v.currentTime')
            assert after>before and not page.locator('#nativeVideo').evaluate('(v)=>v.paused')
            page.locator('#nativeVideo').evaluate('(v)=>v.currentTime=4');page.wait_for_timeout(200)
            assert page.locator('#nativeVideo').evaluate('(v)=>v.currentTime')>=4
            page.evaluate("Object.defineProperty(document.querySelector('#nativeVideo'),'requestPictureInPicture',{configurable:true,value:()=>{window.__nativePipCalls=(window.__nativePipCalls||0)+1;return Promise.resolve()}})")
            page.click('#nativePip');assert page.evaluate('window.__nativePipCalls')==1
            report['checks'].append('Native PiP button calls the video API; actual OS PiP is not simulated as a pass')
            page.click('#nativeAudioMode');page.wait_for_timeout(500)
            assert not page.locator('#nativeAudio').evaluate('(v)=>v.paused')
            page.click('#nativeSave');page.wait_for_function("document.querySelector('#nativeStatus').textContent.includes('Saved locally')")
            report['checks'].append('Synthetic MP4 playback continues across closing study; seek, audio-only and local save work')
            report['media']='Synthetic H.264/AAC MP4 decoded; requested recitation file still awaited'
        page.screenshot(path=str(out/'community-mobile.png'),full_page=False)
        page.set_viewport_size({'width':1280,'height':900})
        page.evaluate('Q.open(35)');page.wait_for_selector('#summary .reading-guide')
        page.screenshot(path=str(out/'community-mulk-guide.png'))
        assert not report['errors'],report['errors']
    finally:
        (out/'community-browser.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
        ctx.close();browser.close()
print('Community browser checks passed')
