// Usage: set window.__job = {url, filename, title, desc, date:'Nov 25, 2026', time:'1:30 PM'} then run.
async function ytUpload(job){
  const S=ms=>new Promise(r=>setTimeout(r,ms));
  function deep(root, sel, out=[]) { root.querySelectorAll(sel).forEach(e=>out.push(e)); root.querySelectorAll('*').forEach(e=>{ if(e.shadowRoot) deep(e.shadowRoot, sel, out); }); return out; }
  const norm=s=>(s||'').replace(/[  ]/g,' ').replace(/\s+/g,' ').trim();
  const log=[];
  // open dialog
  let inp=deep(document,'input[type=file][name=Filedata]')[0];
  if(!inp){ const b=deep(document,'ytcp-button,button').find(x=>/upload videos/i.test(x.innerText||'')); if(b){b.click();} else { deep(document,'ytcp-button,button').find(x=>norm(x.innerText)==='Create').click(); await S(800); deep(document,'tp-yt-paper-item,[role=menuitem]').find(x=>/upload videos/i.test(x.innerText||'')).click(); } await S(2500); inp=deep(document,'input[type=file][name=Filedata]')[0]; }
  const blob=await (await fetch(job.url)).blob(); log.push('fetched '+blob.size);
  const dt=new DataTransfer(); dt.items.add(new File([blob], job.filename, {type:'video/mp4'})); inp.files=dt.files; inp.dispatchEvent(new Event('change',{bubbles:true}));
  await S(7000);
  function setBox(el, text){ el.focus(); const sel=document.getSelection(); const r=document.createRange(); r.selectNodeContents(el); sel.removeAllRanges(); sel.addRange(r); document.execCommand('insertText', false, text); el.dispatchEvent(new Event('input',{bubbles:true})); }
  const boxes=deep(document,'ytcp-uploads-dialog #textbox'); setBox(boxes[0], job.title); setBox(boxes[1], job.desc); await S(600);
  deep(document,'ytcp-uploads-dialog tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]')[0].click();
  const more=deep(document,'ytcp-uploads-dialog ytcp-button#toggle-button').find(b=>/show more/i.test(b.innerText)); if(more){more.click(); await S(1200);}
  const pick=n=>{const r=deep(document,`ytcp-uploads-dialog tp-yt-paper-radio-button[name=${n}]`)[0]; r&&r.click();};
  pick('VIDEO_PAID_PRODUCT_PLACEMENT_NO'); pick('VIDEO_HAS_ALTERED_CONTENT_NO'); await S(500);
  for(let i=0;i<3;i++){ deep(document,'ytcp-uploads-dialog ytcp-button#next-button')[0].click(); await S(2000); }
  deep(document,'ytcp-uploads-dialog #second-container-expand-button')[0].click(); await S(1500);
  const picker=deep(document,'ytcp-uploads-dialog ytcp-datetime-picker')[0];
  // date
  if(norm(picker.innerText.split('\n')[0])!==job.date){
    const di=deep(picker,'#datepicker-trigger, ytcp-dropdown-trigger')[0]; di.click(); await S(800);
    const dinp=deep(document,'ytcp-date-picker input, tp-yt-iron-input input').filter(i=>i.offsetParent).pop();
    dinp.focus(); dinp.select(); document.execCommand('insertText',false,job.date); dinp.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',keyCode:13,bubbles:true})); await S(800);
  }
  const tin=deep(picker,'input').find(i=>/AM|PM/.test(i.value)); tin.focus(); tin.click(); await S(1000);
  const it=deep(document,'tp-yt-paper-item').find(i=>norm(i.textContent)===job.time); it.click(); await S(800);
  log.push('when '+norm(picker.innerText.split('\n')[0])+' '+norm(tin.value));
  if(norm(tin.value)!==job.time) return {error:'time not set', log};
  deep(document,'ytcp-uploads-dialog ytcp-button#done-button')[0].click(); await S(5000);
  const d=deep(document,'ytcp-video-share-dialog, ytcp-uploads-still-processing-dialog, tp-yt-paper-dialog').filter(x=>x.offsetParent).map(x=>norm(x.innerText).slice(0,220));
  const close=deep(document,'ytcp-button,button').filter(b=>b.offsetParent && /^close$/i.test(norm(b.innerText)))[0]; close&&close.click(); await S(1000);
  return {log, d};
}
