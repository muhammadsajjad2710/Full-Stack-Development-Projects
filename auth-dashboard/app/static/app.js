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

let token = "";
async function showMe(){
  if(!token){ $("profile").textContent="Not signed in"; return; }
  const me = await fetch("/me",{headers:{Authorization:"Bearer "+token}}).then(r=>r.json());
  $("profile").textContent = "Signed in as "+me.username;
}
$("form").addEventListener("submit", async (e)=>{
  e.preventDefault();
  try{
    const data = await api("/login",{method:"POST",body:JSON.stringify({username:$("username").value,password:$("password").value})});
    token = data.access_token; setStatus("Logged in"); showMe();
  }catch(err){ setStatus(err.message,true); }
});
$("register").addEventListener("click", async()=>{
  try{ await api("/register",{method:"POST",body:JSON.stringify({username:$("username").value,password:$("password").value})}); setStatus("Registered, now log in"); }
  catch(err){ setStatus(err.message,true); }
});
showMe();
