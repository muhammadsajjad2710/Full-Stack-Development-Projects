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
  const recipes = await api("/recipes");
  const list = clearList();
  recipes.forEach(recipe=>{
    const item=el("li");
    const wrap=el("div");
    wrap.appendChild(el("strong", recipe.title));
    wrap.appendChild(el("p", recipe.ingredients));
    wrap.appendChild(el("p", recipe.steps));
    item.appendChild(wrap); list.appendChild(item);
  });
}
$("form").addEventListener("submit", async (e)=>{
  e.preventDefault();
  try{ await api("/recipes",{method:"POST",body:JSON.stringify({title:$("title").value,ingredients:$("ingredients").value,steps:$("steps").value})}); $("form").reset(); setStatus("Saved"); refresh(); }
  catch(err){ setStatus(err.message,true); }
});
refresh();
