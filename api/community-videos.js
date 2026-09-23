/* Fixed publisher discovery and primary YouTube metadata verification; no downloads or URL proxy. */
const existing=require('./recordings.js');
const content=require('../community-content.json');
const allowed=new Map(content.catalogue.map(s=>[s.surahNo,s]));
const cache=new Map();
const seeds={19:['zndYpTZWhFc'],36:['z-W_NfyAP3Q'],55:['H4N5eFbLl9A'],56:['NDE6iXOK7_Q'],67:['ifGIMi82aFE']};
function normal(s){return String(s).normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9\u0600-\u06ff]+/gi,'').toLowerCase();}
async function get(url,json=true){const r=await fetch(url,{signal:AbortSignal.timeout(9000),redirect:'error'});if(!r.ok)throw Error('Publisher HTTP '+r.status);const txt=await r.text();if(txt.length>2000000)throw Error('Publisher response too large');return json?JSON.parse(txt):txt;}
module.exports=async(req,res)=>{
 res.setHeader('X-Content-Type-Options','nosniff');if(req.method!=='GET')return res.status(405).json({error:'GET only'});
 const surah=Number(req.query.surah),s=allowed.get(surah);if(!s)return res.status(400).json({error:'Unsupported chapter'});
 const saved=cache.get(surah);if(saved&&Date.now()-saved.at<3600000){res.setHeader('Cache-Control','public, max-age=600, s-maxage=3600');return res.json(saved.value);}
 const aliases=(s.aliases||[s.surah.replace(/^Al-|^Ar-|^As-|^An-|^At-/,'')]).map(normal);aliases.push(normal(s.arabicName));
 const matches=title=>aliases.some(a=>a.length>2&&normal(title).includes(a));
 const choices=existing.wanted.filter(w=>w.page);
 const results=await Promise.allSettled(choices.map(async w=>{
   const source='https://surahquran.com/video-sheikh-'+w.page+'-sora-'+surah+'-en.html';let ids=w.page==='127'?[...(seeds[surah]||[])]:[];
   try{const html=await get(source,false);ids.push(...[...html.matchAll(/(?:youtube(?:-nocookie)?\.com\/(?:embed\/|watch\?v=)|youtu\.be\/)([A-Za-z0-9_-]{11})/g)].slice(0,3).map(m=>m[1]));}catch{}
   for(const id of [...new Set(ids)].slice(0,3)){
    try{const url='https://www.youtube.com/watch?v='+id,m=await get('https://www.youtube.com/oembed?url='+encodeURIComponent(url)+'&format=json');
      if(!matches(m.title)||!w.pattern.test(m.title+' '+m.author_name))continue;
      return{id,name:w.name,title:m.title,author:m.author_name,url,source,metadataSource:'https://www.youtube.com/oembed?url='+encodeURIComponent(url)+'&format=json',range:'Surah '+surah+' | '+m.title,scope:'source-recording',checkedAt:new Date().toISOString()};
    }catch{}
   }
   throw Error('No independently matching video metadata');
 }));
 const videos=results.filter(x=>x.status==='fulfilled').map(x=>x.value);const value={surah,videos,checkedAt:new Date().toISOString(),unavailable:results.filter(x=>x.status==='rejected').length};
 if(videos.length){cache.set(surah,{at:Date.now(),value});res.setHeader('Cache-Control','public, max-age=600, s-maxage=3600');}
 else res.setHeader('Cache-Control','no-store');return res.status(200).json(value);
};
module.exports.normal=normal;
