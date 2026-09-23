import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const read=f=>fs.readFileSync(f,'utf8'),write=(f,s)=>fs.writeFileSync(f,s);
const D=JSON.parse(read('community-content.json'));
const langs=['en','bn','ja'];
assert.equal(D.guides.length,30);assert.equal(D.fullSurahs.length,7);
for(const g of [...D.guides,...D.fullSurahs])for(const l of langs)assert(g.theme[l],g.rank+' theme '+l);
for(const l of langs)for(const k of Object.keys(D.labels.en))assert(D.labels[l][k],l+' missing '+k);
for(const n of Object.values(D.practiceNotes)){for(const l of langs)assert(n[l]);assert(n.sources.length);for(const s of n.sources)assert(s.url.startsWith('https://'));}
for(const f of ['community-study.js','native-media.js','community.css'])fs.copyFileSync(f,'public/'+f);
const bootstrap='window.FQ_COMMUNITY='+JSON.stringify(D)+';\n'+`for(const s of window.FQ_COMMUNITY.fullSurahs){window.PASSAGES.push({...s,kind:'full',open:'',peak:'',peakAt:'',why:'',signal:'Full surah',evidence:'',tags:['full'],reciters:['Mishary Rashid Alafasy','Abdul Rahman Al-Sudais','Abdul Rahman Al-Ossi','Yasser Al-Dosari'],read:s.sections.map(n=>'https://www.equraninstitute.com/quranreading/'+n),listen:'https://www.youtube.com/results?search_query='+encodeURIComponent(s.surah+' Mishary Rashid Alafasy')});}`;
write('public/community-content.js',bootstrap);
let html=read('public/index.html');assert(html.includes('<script src="/app-v2.js">'));
html=html.replace('<script src="/app-v2.js">','<script src="/community-content.js"></script><script src="/app-v2.js">');
html=html.replace('</head>','<link rel="stylesheet" href="/community.css"></head>');
html=html.replace('</body>','<script src="/native-media.js"></script><script src="/community-study.js"></script></body>');
write('public/index.html',html);
function patch(file,old,next){let s=read('public/'+file);assert(s.includes(old),file+' anchor missing: '+old.slice(0,90));s=s.replace(old,next);write('public/'+file,s);}
// Avoid rendering the recordings panel twice for a single opening.
patch('community-study.js','Q.tab(tab);await pending;','await pending;');
patch('native-media.js','Q.stopBrowsing?.();session();','Q.stop();session();');
// Non-modal study windows keep the permanent native media outside an inert/removed dialog subtree.
for(const file of ['app-v2.js','experience-v3.js'])write('public/'+file,read('public/'+file).replaceAll('.showModal()', '.show()'));
patch('app-v2.js','let a=P.filter(p=>','let a=P.filter(p=>!p.kind).filter(p=>');
patch('app-v2.js','if(!p)return;Q.stop();Q.active=p;','if(!p)return;Q.stopBrowsing?.();Q.active=p;');
patch('app-v2.js',"if(lang==='ja'){content=reading.rows.find(x=>x.n===n)?.translation?.footnotes||'';label=Q.t('footnotes')+' | Saeed Sato / QuranEnc';}","if(lang==='ja'){const z=Q.unbox(await Q.json(`https://quranenc.com/api/v1/translation/aya/japanese_mokhtasar/${s}/${n}`));content=z?.translation||'';label='Al-Mukhtasar / QuranEnc / japanese_mokhtasar';}");
// Keep the real <audio> attached to body for its entire playback lifetime, rather than moving it with the controls.
patch('experience-v3.js','document.body.append(mini);mini.appendChild(player);','document.body.append(mini);document.body.appendChild(player);player.dataset.persistentMedia="true";player.style.display="none";');
patch('experience-v3.js','const miniHost=dialog.open?dialog:document.body;','const miniHost=document.body;');
patch('experience-v3.js','if(a!==player)a.pause();','if(a!==player&&!a.hasAttribute("data-persistent-media"))a.pause();');
patch('native-media.js','video id="nativeVideo"','video data-persistent-media="true" id="nativeVideo"');
patch('native-media.js','audio id="nativeAudio"','audio data-persistent-media="true" id="nativeAudio"');
// Never represent a YouTube page link as a native PiP API call.
const stringsCtx=vm.createContext({window:{}});vm.runInContext(read('public/v3-strings.js'),stringsCtx);for(const lang of langs){stringsCtx.window.FQ_V3_TEXT[lang].systemPip='YouTube';stringsCtx.window.FQ_V3_TEXT[lang].iosAudioHelp=D.labels[lang].backgroundAdvice;}write('public/v3-strings.js','window.FQ_V3_TEXT='+JSON.stringify(stringsCtx.window.FQ_V3_TEXT)+';');
// Add independently resolved recordings without discarding the pinned Ibrahim performances.
patch('experience-v3.js',"let clips=p.surahNo===25?[...clips25]:[];","let clips=[...new Map([...(p.surahNo===25?clips25:[]),...(Q.communityVideos?.[p.surahNo]||[])].map(c=>[c.id,c])).values()];");
patch('experience-v3.js',"m.rank===Q.reading?.rank;","m.rank===Q.playQueue?.rank;");
// Clear the video-progress timer while hidden; no background visual work or repeated player rebuilding.
patch('experience-v3.js','function startVideoTicker(){clearInterval(floatTicker);floatTicker=setInterval(refreshVideoControls,500);refreshVideoControls();}',"function startVideoTicker(){clearInterval(floatTicker);floatTicker=null;if(document.hidden)return;floatTicker=setInterval(()=>{if(!document.hidden)refreshVideoControls();},1000);refreshVideoControls();}document.addEventListener('visibilitychange',()=>{clearInterval(floatTicker);floatTicker=null;if(!document.hidden&&floatYt)startVideoTicker();});");
patch('experience-v3.js',"player.addEventListener('timeupdate',syncMini);","let miniPaintAt=0;player.addEventListener('timeupdate',()=>{if(!document.hidden&&performance.now()-miniPaintAt>350){miniPaintAt=performance.now();syncMini();}});");
patch('app-v2.js','player.ontimeupdate=()=>Q.updatePlayback?.();','player.ontimeupdate=null;');
patch('app-v2.js',"$('#utilityDialog').onclose=Q.stop;","$('#utilityDialog').onclose=()=>Q.stopBrowsing?.();");
// Loading a library panel should not stop a user-selected native recording.
patch('media-v2.js',"Q.stop();const box=$$('.offline-player',target)[i]","if(Q.nativeMedia){return Q.nativeMedia.prepare(v,audioOnly);}Q.stop();const box=$$('.offline-player',target)[i]");
patch('media-v2.js','Q.offline=async()=>{Q.stop();','Q.offline=async()=>{Q.stopBrowsing?.();');
let worker=read('public/sw.js');worker=worker.replace('const ASSETS=[',"const ASSETS=['/community-content.js','/community-study.js','/native-media.js','/community.css',");write('public/sw.js',worker);
for(const file of ['community-content.js','community-study.js','native-media.js','app-v2.js','experience-v3.js'])new vm.Script(read('public/'+file),{filename:file});
const ctx=vm.createContext({window:{}});for(const f of ['passages-1.js','passages-2.js','passages-3.js','community-content.js'])vm.runInContext(read('public/'+f),ctx);assert.equal(ctx.window.PASSAGES.length,37);assert.equal(new Set(ctx.window.PASSAGES.map(p=>p.rank)).size,37);
for(const g of [...D.guides,...D.fullSurahs]){const p=ctx.window.PASSAGES.find(x=>x.rank===g.rank),[a,b]=p.range.match(/\d+/g).map(Number);for(const n of g.keyAyahs)assert(n>=a&&n<=b,p.rank+' source verse outside range');}
const {verify}=await import('./verify.mjs');const checks=await verify();checks.push('30 source-mapped introductions and 7 full surahs; 3 languages','Original IDs and notes keys unchanged','Native media support awaiting owner-provided public file; no YouTube extraction','Japanese Al-Mukhtasar edition configured; publisher coverage checked separately');
const hash=createHash('sha256');for(const f of fs.readdirSync('public').sort())if(f!=='release.json')hash.update(f).update(fs.readFileSync('public/'+f));const revision=hash.digest('hex').slice(0,16);
worker=read('public/sw.js');assert(/const SHELL=[^;]+;/.test(worker));worker=worker.replace(/const SHELL=[^;]+;/,"const SHELL='fq-shell-"+revision+"';");write('public/sw.js',worker);
write('public/release.json',JSON.stringify({version:'4.0.0',revision,commit:process.env.VERCEL_GIT_COMMIT_SHA||process.env.GITHUB_SHA||'local',builtAt:new Date().toISOString(),checks,scope:'Source maps and browser checks; physical iPhone lock-screen/thermal testing is not implied.'},null,2));
console.log('Community build:',checks.length,'checks passed');
