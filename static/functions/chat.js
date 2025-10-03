import cardMatter from "./components/card.js";

const buttonChat=document.querySelector('.button-chat');
const chathistory=document.querySelector('.chat-history');
const inputchat=document.querySelector('#inputchat');
const buttontrash=document.querySelector(".buttontrash");

export function fetchAPI(url){
    const requisition=fetch(url);
    const responseJson=requisition.then(res=>res.json());
    return responseJson;
}

buttontrash.addEventListener('click',(event)=>{
  event.preventDefault();
   var urlBase="/cleanchat";
   fetch(urlBase,{method:'POST'}).then(res=>{location.reload()})
})

fetchAPI('/allchat').then(
   res=>{
      res.forEach(item=>{
        if(item.response && item.name=='Gemini'){
          inputchat.disabled=false
          buttonChat.disabled=false
          var div=document.createElement('div');
          div.classList.add('chatcard');
          div.innerHTML=`<h4>${item.name}</h4><p>${item.response}</p>`;
          chathistory.appendChild(div)
        }
        else if(item.question && item.name=='You') {
          var div=document.createElement('div');
          div.classList.add('chatcarduser');
          div.innerHTML=`<h4>${item.name}</h4><p>${item.question}</p>`;
          chathistory.appendChild(div)
          inputchat.value=''
        }})

    }).catch(res=>{
          var div=document.createElement('div');
          div.innerHTML=`<p id="chatText">Nenhuma conversa</p>`;
          chathistory.appendChild(div)
    })
 

buttonChat.addEventListener('click',(event)=>{
  event.preventDefault();
  const requisition=fetch('/chat',{
    method:'POST',
    headers:{
      "Content-Type":"application/json",
    },
    body:JSON.stringify({data:inputchat.value}),
  });
  requisition.then(()=>location.reload());
  inputchat.disabled=true
  buttonChat.disabled=true
})