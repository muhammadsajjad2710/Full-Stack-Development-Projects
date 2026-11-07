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
  const posts = await api("/posts");
  const list = clearList();
  posts.forEach(post=>{
    const item=el("li");
    const wrap=el("div"); wrap.appendChild(el("strong", post.title)); wrap.appendChild(el("p", post.body));
    post.comments.forEach(c=> wrap.appendChild(el("p", c.author+": "+c.body)));
    const row=el("div"); row.className="row";
    const author=el("input"); author.placeholder="Name";
    const body=el("input"); body.placeholder="Comment";
    const btn=el("button","Comment");
    btn.addEventListener("click", async()=>{
      await api("/posts/"+post.id+"/comments",{method:"POST",body:JSON.stringify({author:author.value,body:body.value})});
      refresh();
    });
    row.appendChild(author); row.appendChild(body); row.appendChild(btn);
    wrap.appendChild(row); item.appendChild(wrap); list.appendChild(item);
  });
}
$("form").addEventListener("submit", async (e)=>{
  e.preventDefault();
  try{ await api("/posts",{method:"POST",body:JSON.stringify({title:$("title").value,body:$("body").value})}); $("form").reset(); setStatus("Published"); refresh(); }
  catch(err){ setStatus(err.message,true); }
});
refresh();
