/* Owner-provided media only. A native video element is not a YouTube extractor. */
(() => {
  'use strict';
  const $=Q.$, E=Q.esc, tr=k=>window.FQ_COMMUNITY.labels[Q.lang]?.[k]||window.FQ_COMMUNITY.labels.en[k]||k;
  const box=document.createElement('section');
  box.id='nativeMedia'; box.className='native-media'; box.hidden=true;
  box.setAttribute('aria-label','Native recording player');
  box.innerHTML='<header id="nativeDrag"><strong id="nativeTitle"></strong><button type="button" id="nativeClose" aria-label="Close player">&#215;</button></header><video id="nativeVideo" controls playsinline webkit-playsinline preload="metadata"></video><audio id="nativeAudio" controls preload="metadata" hidden></audio><div class="native-actions"><button type="button" id="nativePlay"></button><button type="button" id="nativeMode"></button><button type="button" id="nativePip"></button><button type="button" id="nativeDownload"></button></div><label class="native-seek"><span id="nativeClock">0:00 / 0:00</span><input id="nativeSeek" type="range" min="0" max="1000" value="0" step="1"></label><label class="native-volume"><span id="nativeVolumeText"></span><input id="nativeVolume" type="range" min="0" max="100" value="100"></label><p id="nativeStatus" role="status"></p>';
  document.body.append(box);
  const video=$('#nativeVideo'), audio=$('#nativeAudio'), seek=$('#nativeSeek'), vol=$('#nativeVolume');
  const originalStop=Q.stop;
  let record=null, blobURL=null, media=video, scrubbing=false, paintAt=0, generation=0, desiredTime=0;
  function time(n){n=Math.max(0,Math.floor(Number(n)||0));return Math.floor(n/60)+':'+String(n%60).padStart(2,'0');}
  function labels(){ $('#nativePlay').textContent=tr(media.paused?'play':'pause');$('#nativePip').textContent=tr('nativePip');$('#nativeDownload').textContent=tr('download');$('#nativeMode').textContent=tr(media===video?'audio':'video');$('#nativeVolumeText').textContent=tr('volume');seek.setAttribute('aria-label',tr('seek'));vol.setAttribute('aria-label',tr('volume'));}
  function update(force=false){if(document.hidden&&!force)return;const now=performance.now();if(!force&&now-paintAt<350)return;paintAt=now;labels();const duration=Number.isFinite(media.duration)?media.duration:0;seek.disabled=duration<=0;if(!scrubbing){seek.value=String(duration?Math.round(media.currentTime/duration*1000):0);$('#nativeClock').textContent=time(media.currentTime)+' / '+time(duration);}if(!vol.matches(':active'))vol.value=String(Math.round(media.volume*100));$('#nativePip').disabled=media!==video||!video.videoWidth||video.readyState<1;}
  function status(s){$('#nativeStatus').textContent=s;}
  function session(){if(!navigator.mediaSession||!record)return;try{navigator.mediaSession.metadata=new MediaMetadata({title:record.label,artist:record.reciter||'Famous Quran',album:'Owner-provided recording'});}catch{}const actions={play:()=>play(),pause:()=>media.pause(),seekto:x=>{if(Number.isFinite(x.seekTime))media.currentTime=x.seekTime;},seekbackward:x=>{media.currentTime=Math.max(0,media.currentTime-(x.seekOffset||10));},seekforward:x=>{if(Number.isFinite(media.duration))media.currentTime=Math.min(media.duration,media.currentTime+(x.seekOffset||10));},stop:()=>{media.pause();}};for(const [k,fn] of Object.entries(actions))try{navigator.mediaSession.setActionHandler(k,fn);}catch{}}
  function play(){if(!record)return;document.querySelectorAll('audio,video').forEach(el=>{if(el!==media)el.pause();});Q.stopBrowsing?.();session();const p=media.play();p?.catch(e=>{status(tr('chooseFirst')+' ('+e.name+')');});return p;}
  async function prepare(r,audioOnly=false){
    if(!r?.blob||!r.blob.size)throw Error('A local media file is required');
    const token=++generation;Q.stop();
    if(document.pictureInPictureElement===video)await document.exitPictureInPicture().catch(()=>{});
    if(token!==generation)return;
    video.pause();audio.pause();video.removeAttribute('src');audio.removeAttribute('src');video.load();audio.load();
    if(blobURL)URL.revokeObjectURL(blobURL);record=r;blobURL=URL.createObjectURL(r.blob);
    media=r.type==='video'&&!audioOnly?video:audio;desiredTime=0;
    video.hidden=media!==video;audio.hidden=media!==audio;media.src=blobURL;media.load();
    $('#nativeTitle').textContent=r.label;$('#nativeMode').hidden=r.type!=='video';box.hidden=false;status(tr('ready'));update(true);
    window.dispatchEvent(new Event('fq:native-ready'));
  }
  function switchMode(){if(!record||record.type!=='video')return;const old=media,wasPlaying=!old.paused;desiredTime=old.currentTime;old.pause();old.removeAttribute('src');old.load();media=old===video?audio:video;video.hidden=media!==video;audio.hidden=media!==audio;media.src=blobURL;media.load();labels();status(tr('ready'));if(wasPlaying)status(tr('ready'));}
  function pip(){if(media!==video||video.readyState<1||!video.videoWidth){status(tr('chooseFirst'));return;}try{if(video.webkitSupportsPresentationMode?.('picture-in-picture')){video.webkitSetPresentationMode(video.webkitPresentationMode==='picture-in-picture'?'inline':'picture-in-picture');return;}if(document.pictureInPictureElement===video){document.exitPictureInPicture().catch(()=>status(tr('unsupported')));return;}if(document.pictureInPictureEnabled&&typeof video.requestPictureInPicture==='function'){video.requestPictureInPicture().catch(()=>status(tr('unsupported')));return;}status(tr('unsupported'));}catch{status(tr('unsupported'));}}
  $('#nativePlay').onclick=()=>media.paused?play():media.pause();$('#nativeMode').onclick=switchMode;$('#nativePip').onclick=pip;
  $('#nativeClose').onclick=()=>{media.pause();try{if(video.webkitPresentationMode==='picture-in-picture')video.webkitSetPresentationMode('inline');}catch{}box.hidden=true;if(document.pictureInPictureElement===video)document.exitPictureInPicture().catch(()=>{});};
  $('#nativeDownload').onclick=()=>{if(record)Q.download(record.blob,record.label.replace(/[\\/]/g,'_'));};
  seek.oninput=()=>{scrubbing=true;const d=Number.isFinite(media.duration)?media.duration:0;$('#nativeClock').textContent=time(d*Number(seek.value)/1000)+' / '+time(d);};
  seek.onchange=()=>{if(Number.isFinite(media.duration)&&media.duration>0)media.currentTime=media.duration*Number(seek.value)/1000;scrubbing=false;update(true);};
  seek.addEventListener('pointercancel',()=>{scrubbing=false;update(true);});
  vol.oninput=()=>{const requested=Number(vol.value)/100;try{media.volume=requested;}catch{}if(Math.abs(media.volume-requested)>.02)status(tr('phoneVolume'));};
  for(const el of [video,audio]){
    el.addEventListener('loadedmetadata',()=>{if(el!==media)return;if(desiredTime>0&&Number.isFinite(el.duration))el.currentTime=Math.min(desiredTime,el.duration);desiredTime=0;update(true);});
    el.addEventListener('timeupdate',()=>update());
    for(const ev of ['play','pause','ended','volumechange','seeked'])el.addEventListener(ev,()=>{if(el!==media)return;try{if(navigator.mediaSession)navigator.mediaSession.playbackState=el.paused?'paused':'playing';}catch{}update(true);});
    el.addEventListener('error',()=>status(tr('fileError')+(el.error?' ('+el.error.code+')':'')));
  }
  Q.stop=()=>{video.pause();audio.pause();originalStop();};
  const drag=$('#nativeDrag');let dragging=false,dx=0,dy=0;
  function place(x,y){const r=box.getBoundingClientRect();box.style.left=Math.max(8,Math.min(x,innerWidth-r.width-8))+'px';box.style.top=Math.max(8,Math.min(y,innerHeight-r.height-8))+'px';box.style.right='auto';box.style.bottom='auto';}
  drag.addEventListener('pointerdown',e=>{if(e.target.closest('button,input')||e.button!==0)return;const r=box.getBoundingClientRect();dx=e.clientX-r.left;dy=e.clientY-r.top;dragging=true;drag.setPointerCapture(e.pointerId);e.preventDefault();});
  drag.addEventListener('pointermove',e=>{if(dragging)place(e.clientX-dx,e.clientY-dy);});
  drag.addEventListener('pointerup',()=>dragging=false);drag.addEventListener('pointercancel',()=>dragging=false);
  window.addEventListener('resize',()=>{if(!box.hidden){const r=box.getBoundingClientRect();place(r.left,r.top);}});
  window.addEventListener('fq:language',()=>{labels();if(!box.hidden)status(tr('nativeHelp'));});
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)update(true);});
  // The importer deliberately does not upload a file or claim public redistribution.
  async function importer(rank){
    const p=window.PASSAGES.find(x=>x.rank===rank);if(!p)return;
    Q.panel(tr('nativeTitle'),'<p>'+E(tr('importHelp'))+'</p><p>'+E(tr('pendingPublic'))+'</p><input id="nativeImport" type="file" accept="video/mp4,video/webm,audio/*" aria-label="'+E(tr('import'))+'"><div id="nativeSaved"></div><p>'+E(tr('nativeHelp'))+'</p>');
    const input=$('#nativeImport'),target=$('#nativeSaved');
    async function list(){const keys=(await Q.idb('keys')).filter(k=>typeof k==='string'&&k.startsWith('media:'));const records=[];for(const key of keys){const r=await Q.idb('get',key);if(r.blob&&(r.passageRank===rank||r.url.startsWith('local:')&&!r.passageRank))records.push(r);}if(!target.isConnected)return;
      target.innerHTML=records.length?records.map((r,i)=>'<article class="offline-card"><h4>'+E(r.label)+'</h4><p>'+E(tr('localOnly'))+'</p><button class="btn" data-native-open="'+i+'">'+E(tr(r.type==='video'?'video':'audio'))+'</button>'+(r.type==='video'?' <button class="btn" data-native-audio="'+i+'">'+E(tr('audio'))+'</button>':'')+'</article>').join(''):'<p>'+E(tr('noFile'))+'</p>';
      Q.$$('[data-native-open]',target).forEach(b=>b.onclick=()=>prepare(records[+b.dataset.nativeOpen]).catch(e=>status(e.message)));
      Q.$$('[data-native-audio]',target).forEach(b=>b.onclick=()=>prepare(records[+b.dataset.nativeAudio],true).catch(e=>status(e.message)));
    }
    input.onchange=async()=>{const file=input.files?.[0];if(!file)return;if(file.size>100*1048576||!file.size||!(/^(audio\/|video\/(mp4|webm))/.test(file.type))){Q.toast(tr('fileError'));return;}input.disabled=true;try{const url='local:'+crypto.randomUUID();await Q.idb('put','media:'+url,{url,label:file.name,type:file.type.startsWith('video/')?'video':'audio',blob:file,bytes:file.size,at:Date.now(),passageRank:rank});await list();Q.toast(tr('saved'));}catch{Q.toast(Q.t('storageError'));}finally{input.disabled=false;}};
    await list();
  }
  Q.nativeMedia={prepare,importer,pip,element:video};labels();
})();
