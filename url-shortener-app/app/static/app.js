function $(id){return document.getElementById(id)}
function el(tag, text){const n=document.createElement(tag); if(text!==undefined) n.textContent=text; return n}
function setStatus(text, isError){const s=$("status"); s.textContent=text||""; s.className=isError?"status error":"status"}
async function api(url, options){
  const res = await fetch(url, Object.assign({headers:{"Content-Type":"application/json"}}, options||{}));
  if(res.status===204) return null;
  const data = await res.json().catch(()=>({}));
  if(!res.ok) throw new Error(data.detail || data.error || res.statusText);
  return data;
}
function clearList(){const list=$("list"); while(list.firstChild) list.removeChild(list.firstChild); return list}

async function refresh(){
  const links = await api("/links");
  const list = clearList();
  links.forEach(link=>{
    const item=el("li");
    const a=el("a", "/"+link.code); a.href="/"+link.code; a.target="_blank"; a.rel="noopener";
    item.appendChild(el("span", link.url+" → ")); item.appendChild(a); list.appendChild(item);
  });
}
$("form").addEventListener("submit", async (e)=>{
  e.preventDefault();
  try{ await api("/shorten",{method:"POST",body:JSON.stringify({url:$("url").value})}); $("url").value=""; setStatus("Created"); refresh(); }
  catch(err){ setStatus(err.message,true); }
});
refresh();
