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

async function refresh(q){
  const data = await api("/books"+(q?("?q="+encodeURIComponent(q)):"" ));
  const list = clearList();
  data.items.forEach(book=>{
    const item=el("li"); item.appendChild(el("span", book.title+" — "+book.author+" ("+book.year+")")); list.appendChild(item);
  });
  setStatus(data.total+" book(s)");
}
$("form").addEventListener("submit", async (e)=>{
  e.preventDefault();
  try{ await api("/books",{method:"POST",body:JSON.stringify({title:$("title").value,author:$("author").value,year:Number($("year").value)})}); $("form").reset(); refresh($("q").value); }
  catch(err){ setStatus(err.message,true); }
});
$("search").addEventListener("submit", (e)=>{ e.preventDefault(); refresh($("q").value); });
refresh("");
