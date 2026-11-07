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

let socket = null;
function connect(room){
  if(socket) socket.close();
  socket = new WebSocket((location.protocol==="https:"?"wss":"ws")+"://"+location.host+"/ws/"+encodeURIComponent(room));
  socket.addEventListener("message", (event)=>{
    const data = JSON.parse(event.data);
    const item=el("li"); item.appendChild(el("span", data.message)); $("list").appendChild(item);
  });
}
async function loadHistory(room){
  const data = await api("/rooms/"+encodeURIComponent(room)+"/history");
  const list = clearList();
  data.messages.forEach(msg=>{ const item=el("li"); item.appendChild(el("span", msg)); list.appendChild(item); });
}
$("form").addEventListener("submit", async (e)=>{
  e.preventDefault();
  const room = $("room").value || "lobby";
  if(!socket || socket.readyState!==1){ connect(room); await loadHistory(room); }
  socket.addEventListener("open", ()=> socket.send($("message").value), {once:true});
  if(socket.readyState===1) socket.send($("message").value);
  $("message").value="";
});
connect("lobby"); loadHistory("lobby");
