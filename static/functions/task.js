const cards_task=document.querySelector('.cards');
const dropzone = document.querySelectorAll(".week-name");
const dom_week=document.querySelector('#dom-week');
const seg_week=document.querySelector('#seg-week');
const ter_week=document.querySelector('#ter-week');
const qua_week=document.querySelector('#qua-week');
const qui_week=document.querySelector('#qui-week');
const sex_week=document.querySelector('#sex-week');
const sab_week=document.querySelector('#sab-week');



//parte da requisição
const requisition=fetch('/alltasks');
const responseJson=requisition.then(res=>res.json());
var data=responseJson

//mostrar tarefas
data.then(res=>
res.forEach(res=>{
      const task=document.createElement('div')
      task.className='card-task'
      task.id=res.id
      task.draggable = true;
      var methodTask={method:'POST',action:'/delete'}
      var updatetask={method:'POST',action:'/updatedetail'}
       var card=`
       <div>
        <h1>${res.name}</h1>
        <p id="hour-card">${res.hour}</p>
        ${dialogDetails(res,methodTask,updatetask)}
        </div>
      `
      task.innerHTML=card;
      task.addEventListener("dragstart",dragStart);
      task.addEventListener("click",openDetailsTasks);
      const buttonCloseDialog=task.querySelector(".exit-details");
      buttonCloseDialog.addEventListener('click',closeModal);
      
      const buttonEdit=task.querySelector(".buttonEdit");
      buttonEdit.addEventListener('click',updateTask)
      
      addTaskWeek(res.week,task,res.id);
   })
);

//pegar tarefa
function dragStart(e){
  e.dataTransfer.setData("text",e.target.id);
}

//execução de soltar a tarefa em outra semana
dropzone.forEach((e)=>{
  e.addEventListener("drop",(e)=>{
    e.preventDefault();
    var data=e.dataTransfer.getData("text")
    var nameWeek=e.currentTarget.dataset.name;
    e.currentTarget.appendChild(document.getElementById(data));
    fetch('/updatetask',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({value:nameWeek,id:data})})
  })
  e.addEventListener("dragover",(e)=>e.preventDefault());
})

// função de adicionar tarefa
function addTaskWeek(week,task,id){
   switch (week){
    case "Dom":
       
       dom_week.appendChild(task)
       dom_week.dataset.id=id
    break;
    case "Seg":
       
       seg_week.appendChild(task)
       seg_week.dataset.id=id
    break;
    case "Ter":
       
       ter_week.appendChild(task)
       ter_week.dataset.id=id
    break;
    case "Qua":
       
       qua_week.appendChild(task)
       qua_week.dataset.id=id
    break;
    case "Qui":
       
       qui_week.appendChild(task)
       qui_week.dataset.id=id
    break;
    case "Sex":
       
       sex_week.appendChild(task)
       sex_week.dataset.id=id
    break;
    case "Sab":
       
       sab_week.appendChild(task)
       sab_week.dataset.id=id
    break;
  }
}

//abrir modal de detalhes
function openDetailsTasks(e){
   const dialog=e.currentTarget.querySelector(".dialog-details")
   dialog.showModal()
}

//botão de fechar do modal
function closeModal(e){
   e.preventDefault();
   e.stopPropagation();
   const dialog = e.currentTarget.closest("dialog");
   const spanEdit = dialog.querySelector('#span-edit');
   const checkedHidden = spanEdit.querySelector('.button-check');
   const inputEdit=dialog.querySelector('#hour');
   const textArea=dialog.querySelector('#textarea-edit')
   inputEdit.disabled=true
   textArea.disabled=true
   if(checkedHidden){
      checkedHidden.remove(); 
   }
   dialog.close();
}

//função para atualizar no back-end
function sendUpdate(id,hour,description){
  
fetch('/updatedetail', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      id: id,
      hour: hour,
      description: description
    })
  }).then(()=>location.reload())
}

//atualizar atividade e mudanças na configuração do modal para atualizar
function updateTask(e){
   e.preventDefault()
   const dialog = e.currentTarget.closest("dialog");
   var buttonCheck=document.createElement('button');
   const inputEdit=dialog.querySelector('#hour');
   const textArea=dialog.querySelector('#textarea-edit');
   const spanEdit=dialog.querySelector("#span-edit");
   textArea.disabled=false
   inputEdit.disabled=false;
   buttonCheck.innerHTML="&#10003;";
   buttonCheck.style.color="#FEFEFE";
   buttonCheck.style.background="#2C856B";
   buttonCheck.style.height="4.5vh";
   buttonCheck.style.width="3vw"
   buttonCheck.style.fontSize="1.5em"
   buttonCheck.type="submit";
   buttonCheck.style.display="flex";
   buttonCheck.style.justifyContent="center";
   buttonCheck.style.alignContent="center";
   buttonCheck.style.marginLeft="0.5rem"
   buttonCheck.classList.add("button-check")

   if (!spanEdit.querySelector('.button-check')) {
   spanEdit.appendChild(buttonCheck);
   }
   
//formação da função checkbox
   const checkedButton=(e)=>{
     e.currentTarget.remove(); 
     inputEdit.disabled=true
     textArea.disabled=true
     const id = dialog.querySelector('input[name="id_editcard"]').value;
     const hour = inputEdit.value;
     const description = textArea.value;
     sendUpdate(id,hour,description)
   }
   buttonCheck.addEventListener('click',checkedButton)
}

// modal de detalhes
function dialogDetails(res,methodTask,updatetask){

   return`
   <dialog class="dialog-details">
      <div class="header-details">
         <h1>${res.name}</h1>
         <form action="${methodTask.action}" method="${methodTask.method}">
             
             <input name="id_card" value="${res.id}" hidden="true" >
             <button id="delete-task">Delete</button>
         </form>
         <button class='exit-details'>X</button>
      </div>
      <form action="${updatetask.action}" method="${updatetask.method}" class="details-description">
      <input value="${res.id}" name="id_editcard" hidden="true"/>
         <span id="span-edit"><button type="button" id="buttonEdit" class="buttonEdit">&#x270E;</button></span>
         <span><input type="time" class='hour-details' id="hour" name="hour" value="${res.hour}" disabled ></span>
         <textarea disabled name="textarea_details" id="textarea-edit">${res.description}</textarea>
      </form>
   </dialog>`
}

