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
  const tasks = await api("/tasks");
  const list = clearList();
  tasks.forEach(task=>{
    const item=el("li");
    item.appendChild(el("span", task.done ? task.title+" (done)" : task.title));
    const btn=el("button", "Toggle"); btn.className="secondary";
    btn.addEventListener("click", async()=>{ await api("/tasks/"+task.id+"/toggle",{method:"POST"}); refresh(); });
    item.appendChild(btn); list.appendChild(item);
  });
}
$("form").addEventListener("submit", async (e)=>{
  e.preventDefault();
  try{ await api("/tasks",{method:"POST",body:JSON.stringify({title:$("title").value})}); $("title").value=""; setStatus("Saved"); refresh(); }
  catch(err){ setStatus(err.message,true); }
});
refresh();
