/* Shared local-only reader tools. No source edits, telemetry or AI calls. */
((host) => {
  "use strict";
  const statuses = ["unmarked", "later", "read", "unclear", "question"];
  const record = x => x !== null && typeof x === "object" && !Array.isArray(x);
  const hash = x => typeof x === "string" && /^[a-f0-9]{64}$/.test(x);
  const id = x => typeof x === "string" && x.endsWith(".md") && !/[:\\?#%]/.test(x) &&
    !x.startsWith("/") && !x.split("/").some(p => p === "." || p === ".." || !p);
  const project = x => typeof x === "string" && /^[a-z0-9][a-z0-9_-]{0,79}$/.test(x);
  function validateCatalog(c) {
    if (!record(c) || c.schema_version !== "1.0" || c.artifact_kind !== "portal_reader_catalog" ||
        !project(c.project_id) || !hash(c.revision) || !Array.isArray(c.pages) || c.pages.length > 20000)
      throw new Error("Unsupported reader catalog");
    const seen = new Set();
    for (const p of c.pages) {
      if (!record(p) || !id(p.id) || seen.has(p.id) || !hash(p.content_hash) ||
          typeof p.title !== "string" || typeof p.summary !== "string" ||
          typeof p.change_summary !== "string" || typeof p.topic !== "string" ||
          typeof p.url !== "string" || /[:\\?#]/.test(p.url) || p.url.startsWith("/") ||
          p.url.split("/").some(s => s === "..")) throw new Error("Invalid reader page");
      seen.add(p.id);
    }
    return c;
  }
  function blank(projectId) { return {schema_version:"1.0", project_id:projectId, baseline:null, marks:{}}; }
  function validateState(s, projectId) {
    if (!record(s) || s.schema_version !== "1.0" || s.project_id !== projectId || !record(s.marks))
      throw new Error("Unsupported or wrong-project review state");
    if (Object.keys(s.marks).length > 20000) throw new Error("Review state too large");
    for (const [key, mark] of Object.entries(s.marks))
      if (!id(key) || !record(mark) || !statuses.includes(mark.status) || !hash(mark.content_hash))
        throw new Error("Invalid review mark");
    if (s.baseline !== null) {
      if (!record(s.baseline) || !hash(s.baseline.revision) || !Array.isArray(s.baseline.pages) || s.baseline.pages.length > 20000)
        throw new Error("Invalid comparison baseline");
      const seen = new Set();
      for (const p of s.baseline.pages) {
        if (!record(p) || !id(p.id) || seen.has(p.id) || !hash(p.content_hash) || typeof p.title !== "string")
          throw new Error("Invalid baseline page");
        seen.add(p.id);
      }
    }
    return s;
  }
  function changesSince(c, baseline) {
    if (baseline === null) return null;
    const old = new Map(baseline.pages.map(p => [p.id,p])); const now = new Map(c.pages.map(p => [p.id,p]));
    return {added:c.pages.filter(p => !old.has(p.id)),
      changed:c.pages.filter(p => old.has(p.id) && old.get(p.id).content_hash !== p.content_hash),
      removed:baseline.pages.filter(p => !now.has(p.id))};
  }
  function effectiveStatus(page, marks) {
    const mark = marks[page.id];
    return mark?.status === "read" && mark.content_hash !== page.content_hash ? "recheck" : (mark?.status || "unmarked");
  }
  function baselineFor(c) { return {revision:c.revision,pages:c.pages.map(p => ({id:p.id,title:p.title,content_hash:p.content_hash}))}; }
  const core = {validateCatalog, validateState, blank, changesSince, effectiveStatus, baselineFor, statuses};
  if (typeof module !== "undefined" && module.exports) { module.exports = core; return; }
  host.PortalReaderCore = core;
  if (typeof document === "undefined") return;
  const labels = {
    en:{unmarked:"Not marked",later:"To review",read:"Read",unclear:"Not understood",question:"Ask my AI",recheck:"Changed — review again",
      added:"Added",changed:"Changed",removed:"Removed",unchanged:"Unchanged",uncompared:"No baseline yet",
      first:"First use: no previous visit history is known. Create a baseline for future comparisons.",
      create:"Create starting baseline",ack:"I have seen these changes",export:"Export local backup",reset:"Clear this project's marks",
      confirm:"Clear this project's review marks and comparison baseline? This does not delete project files.",
      view:"Pages",all:"All pages",changedOnly:"Added / changed / removed",status:"Review status",any:"All statuses",search:"Find a page",
      prev:"Previous",next:"Next",empty:"No pages match these filters.",
      saved:"Review marks stay in this browser only.",ephemeral:"Browser storage is unavailable. Marks on this page are temporary and can be lost on navigation.",
      badState:"Saved review data is invalid or belongs to another version. It has not been overwritten. Export a backup or explicitly clear it.",
      loadError:"Could not load the reader catalog. Project documents remain available.",retry:"Retry",
      explanation:"Page introduction, not an automatic diff summary: ",changeNote:"Author's latest change note: ",
      removedNote:"No longer in this built catalog; the old page link is not opened.",count:"Shown",pages:"pages",changes:"Changes since your saved baseline",readonly:"Review controls disabled until saved-data error is resolved."},
    tr:{unmarked:"İşaretlenmedi",later:"İnceleyeceğim",read:"Okudum",unclear:"Anlamadım",question:"AI'a soracağım",recheck:"Değişti — yeniden incele",
      added:"Eklendi",changed:"Değişti",removed:"Kaldırıldı",unchanged:"Değişmedi",uncompared:"Başlangıç kaydı yok",
      first:"İlk kullanım: önceki ziyaret geçmişini bilmiyoruz. Sonraki karşılaştırmalar için başlangıç kaydı oluştur.",
      create:"Başlangıç kaydı oluştur",ack:"Bu değişiklikleri gördüm",export:"Yerel yedeği dışa aktar",reset:"Bu projenin işaretlerini temizle",
      confirm:"Bu projenin inceleme işaretleri ve başlangıç kaydı temizlensin mi? Proje dosyaları silinmez.",
      view:"Sayfalar",all:"Bütün sayfalar",changedOnly:"Eklenen / değişen / kaldırılan",status:"İnceleme durumu",any:"Bütün durumlar",search:"Sayfa ara",
      prev:"Önceki",next:"Sonraki",empty:"Bu filtrelerle eşleşen sayfa yok.",
      saved:"İnceleme işaretleri yalnız bu tarayıcıda saklanır.",ephemeral:"Tarayıcı kaydı kullanılamıyor. İşaretler bu sayfada geçici; başka sayfaya geçince kaybolabilir.",
      badState:"Kayıtlı inceleme verisi bozuk veya başka sürüme ait. Üzerine yazılmadı. Yedeği dışa aktarabilir veya açıkça temizleyebilirsin.",
      loadError:"İnceleme kataloğu yüklenemedi. Proje belgelerine erişebilirsin.",retry:"Yeniden dene",
      explanation:"Sayfa tanıtımı; otomatik değişiklik özeti değil: ",changeNote:"Yazarın son değişiklik notu: ",
      removedNote:"Bu derlemenin kataloğunda artık yok; eski sayfa bağlantısı açılmaz.",count:"Gösterilen",pages:"sayfa",changes:"Başlangıç kaydından beri değişiklikler",readonly:"Kayıtlı veri sorunu çözülene kadar inceleme kontrolleri kapalı."}
  };
  const catalogs = new Map(), sessions = new Map();
  const make = (tag,text,cls) => { const e=document.createElement(tag); if(text!==undefined)e.textContent=text; if(cls)e.className=cls; return e; };
  const select = (options) => { const e=make("select"); for(const [v,t] of options){const o=make("option",t);o.value=v;e.append(o);} return e; };
  const keyFor = id => `project-context-portal:reader:v1:${id}`;
  function session(projectId) {
    if (!sessions.has(projectId)) sessions.set(projectId,{state:blank(projectId),bad:false,unavailable:false,raw:null,listeners:new Set()});
    return sessions.get(projectId);
  }
  function read(projectId) {
    const s=session(projectId);
    if(s.unavailable)return s;
    try {s.raw=localStorage.getItem(keyFor(projectId));}
    catch(_){s.unavailable=true;return s;}
    try {
      s.state=s.raw===null ? blank(projectId) : validateState(JSON.parse(s.raw),projectId); s.bad=false;
    } catch(_){s.bad=true;}
    return s;
  }
  function update(projectId,action,reset=false) {
    const s=read(projectId); if(s.bad&&!reset)return;
    const state=reset?blank(projectId):s.state; action(state); s.state=state;s.bad=false;
    try{localStorage.setItem(keyFor(projectId),JSON.stringify(state));s.raw=JSON.stringify(state);}
    catch(_){s.unavailable=true;}
    for(const render of s.listeners)render();
  }
  function download(projectId) {
    const s=read(projectId); const body=s.bad?s.raw:JSON.stringify(s.state,null,2);
    const url=URL.createObjectURL(new Blob([body],{type:"application/json"})); const a=make("a");
    a.href=url;a.download=`${projectId}-reader-backup.json`;document.body.append(a);a.click();a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  function pageLink(page,base) {
    const target=new URL(page.url,base);
    if(target.origin!==base.origin || !target.pathname.startsWith(base.pathname))throw new Error("Unsafe reader link");
    return target.href;
  }
  function message(s,t,e){e.setAttribute("role",s.bad?"alert":"status");e.textContent=s.bad?t.badState:s.unavailable?t.ephemeral:t.saved;}
  function toolbar(root,c,base,t) {
    const page=c.pages.find(p=>p.id===root.dataset.readerPage); if(!page)throw new Error("Reader page not in catalog");
    const pick=root.querySelector('[data-reader-mark]'),msg=root.querySelector('[data-reader-message]');
    pick.replaceChildren(...select(statuses.map(k=>[k,t[k]])).children);
    const render=()=>{if(!root.isConnected)return;const s=read(c.project_id);pick.disabled=s.bad;pick.value=s.state.marks[page.id]?.status||"unmarked";message(s,t,msg);if(effectiveStatus(page,s.state.marks)==="recheck")msg.textContent+=" "+t.recheck;};
    pick.addEventListener("change",()=>update(c.project_id,s=>{s.marks[page.id]={status:pick.value,content_hash:page.content_hash};}));
    session(c.project_id).listeners.add(render);render();
  }
  function center(root,c,base,t) {
    root.replaceChildren();const notice=make("p",undefined,"reader-warning");notice.setAttribute("aria-live","polite");
    const actions=make("div",undefined,"reader-actions"),ack=make("button"),backup=make("button",t.export),reset=make("button",t.reset);
    for(const b of [ack,backup,reset]){b.type="button";actions.append(b);}
    const persistence=make("p");persistence.setAttribute("aria-live","polite");
    const controls=make("div",undefined,"reader-controls");
    const view=select([["all",t.all],["changed",t.changedOnly]]),status=select([["any",t.any],...statuses.map(k=>[k,t[k]]),["recheck",t.recheck]]),search=make("input");search.type="search";
    for(const [name,e] of [[t.view,view],[t.status,status],[t.search,search]]){const l=make("label",name);l.append(e);controls.append(l);}
    const count=make("p"),list=make("ul",undefined,"reader-cards"),pager=make("div",undefined,"reader-actions"),prev=make("button",t.prev),next=make("button",t.next);
    prev.type=next.type="button";pager.append(prev,next);root.append(notice,actions,persistence,controls,count,list,pager);
    let number=0;view.value=read(c.project_id).state.baseline?"changed":"all";
    function render(){
      if(!root.isConnected)return;const s=read(c.project_id),state=s.state,diff=changesSince(c,state.baseline);
      notice.textContent=s.bad?t.readonly:diff?`${t.changes}: ${diff.added.length} ${t.added}, ${diff.changed.length} ${t.changed}, ${diff.removed.length} ${t.removed}.`:t.first;
      message(s,t,persistence);ack.textContent=state.baseline?t.ack:t.create;ack.disabled=s.bad;
      for(const e of [view,status,search])e.disabled=s.bad;
      const types=new Map();if(diff){for(const k of ["added","changed","removed"])for(const p of diff[k])types.set(p.id,k);}
      const pages=[...c.pages,...(diff?.removed||[]).map(p=>({...p,summary:"",change_summary:"",topic:""}))];
      const term=search.value.trim().toLocaleLowerCase(root.dataset.readerLang==="tr"?"tr-TR":"en");
      const filtered=pages.filter(p=>(view.value!=="changed"||types.has(p.id))&&
        (status.value==="any"||effectiveStatus(p,state.marks)===status.value)&&
        (!term||`${p.title} ${p.id} ${p.summary}`.toLocaleLowerCase(root.dataset.readerLang==="tr"?"tr-TR":"en").includes(term)));
      number=Math.min(number,Math.max(0,Math.ceil(filtered.length/20)-1));const shown=filtered.slice(number*20,number*20+20);
      count.textContent=filtered.length?`${t.count}: ${number*20+1}–${number*20+shown.length} / ${filtered.length} ${t.pages}.`:t.empty;
      list.replaceChildren();prev.disabled=number===0;next.disabled=(number+1)*20>=filtered.length;
      for(const page of shown){
        const li=make("li",undefined,"reader-card"),heading=make("h3");
        if(types.get(page.id)==="removed")heading.textContent=page.title;
        else{const a=make("a",page.title);a.href=pageLink(page,base);heading.append(a);}
        li.append(heading,make("span",t[diff?(types.get(page.id)||"unchanged"):"uncompared"],"reader-tag"),make("span",t[effectiveStatus(page,state.marks)],"reader-tag"));
        if(types.get(page.id)==="removed")li.append(make("p",t.removedNote));
        else{
          if(page.change_summary)li.append(make("p",t.changeNote+page.change_summary));
          if(page.summary)li.append(make("p",t.explanation+page.summary));
          const label=make("label",t.status),pick=select(statuses.map(k=>[k,t[k]]));pick.value=state.marks[page.id]?.status||"unmarked";pick.disabled=s.bad;
          pick.addEventListener("change",()=>update(c.project_id,x=>{x.marks[page.id]={status:pick.value,content_hash:page.content_hash};}));label.append(pick);li.append(label);
        }
        li.append(make("p",page.id));list.append(li);
      }
    }
    ack.addEventListener("click",()=>update(c.project_id,s=>{s.baseline=baselineFor(c);}));backup.addEventListener("click",()=>download(c.project_id));
    reset.addEventListener("click",()=>{if(window.confirm(t.confirm))update(c.project_id,()=>{},true);});
    for(const e of [view,status])e.addEventListener("change",()=>{number=0;render();});search.addEventListener("input",()=>{number=0;render();});
    prev.addEventListener("click",()=>{number--;render();});next.addEventListener("click",()=>{number++;render();});
    session(c.project_id).listeners.add(render);render();
  }
  async function initRoot(root) {
    if(root.dataset.readerReady)return;root.dataset.readerReady="true";
    const t=labels[root.dataset.readerLang]||labels.en;
    let url;
    try{
      const base=new URL(root.dataset.readerRoot,location.href);url=new URL(root.dataset.readerCatalog,location.href);
      if(url.origin!==location.origin||!url.pathname.startsWith(base.pathname))throw new Error("Non-local catalog");
      if(!catalogs.has(url.href))catalogs.set(url.href,fetch(url).then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json();}).then(validateCatalog));
      const c=await catalogs.get(url.href);if(!root.isConnected)return;
      if(root.hasAttribute("data-reader-center"))center(root,c,base,t);else toolbar(root,c,base,t);
    }catch(error){
      if(url)catalogs.delete(url.href);
      if(root.hasAttribute('data-reader-center'))root.replaceChildren();
      const p=make("p",`${t.loadError} (${error.message})`);p.setAttribute("role","alert");
      const retry=make("button",t.retry);retry.type="button";retry.addEventListener("click",()=>{p.remove();retry.remove();delete root.dataset.readerReady;initRoot(root);});root.append(p,retry);
    }
  }
  const init=()=>document.querySelectorAll('[data-reader-toolbar],[data-reader-center]').forEach(initRoot);
  window.addEventListener("storage",event=>{for(const [projectId,s] of sessions)if(event.key===keyFor(projectId))for(const render of s.listeners)render();});
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
  if(typeof document$!=="undefined")document$.subscribe(init);
})(typeof globalThis!=="undefined"?globalThis:this);
