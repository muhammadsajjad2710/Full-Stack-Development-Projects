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
  const issues = await api("/issues");
  const list = clearList();
  issues.forEach(issue=>{
    const item=el("li");
    item.appendChild(el("span", issue.title+" — "+(issue.open?"open":"closed")));
    if(issue.open){
      const btn=el("button","Close"); btn.className="secondary";
      btn.addEventListener("click", async()=>{ await api("/issues/"+issue.id+"/close",{method:"POST"}); refresh(); });
      item.appendChild(btn);
    }
    list.appendChild(item);
  });
}
$("form").addEventListener("submit", async (e)=>{
  e.preventDefault();
  try{ await api("/issues",{method:"POST",body:JSON.stringify({title:$("title").value,description:$("description").value})}); $("form").reset(); refresh(); }
  catch(err){ setStatus(err.message,true); }
});
refresh();
