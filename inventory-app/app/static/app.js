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
  const products = await api("/products");
  const list = clearList();
  products.forEach(p=>{
    const item=el("li");
    item.appendChild(el("span", p.name+" — stock "+p.stock));
    const btn=el("button","Sell 1"); btn.className="secondary";
    btn.addEventListener("click", async()=>{ try{ await api("/products/"+p.id+"/sell",{method:"POST",body:JSON.stringify({quantity:1})}); setStatus("Sold"); refresh(); }catch(err){ setStatus(err.message,true);} });
    item.appendChild(btn); list.appendChild(item);
  });
}
$("form").addEventListener("submit", async (e)=>{
  e.preventDefault();
  try{ await api("/products",{method:"POST",body:JSON.stringify({name:$("name").value,stock:Number($("stock").value),price_cents:Number($("price_cents").value)})}); refresh(); }
  catch(err){ setStatus(err.message,true); }
});
refresh();
