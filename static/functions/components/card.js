export default function cardMatter(res){
    function fetchAPI(url){
    const requisition=fetch(url);
    const responseJson=requisition.then(res=>res.json());
    return responseJson;
    }


    const dialog=()=>{
        var dialog=document.createElement('dialog')
        dialog.classList.add(`dialog-card-matter-${res.id}`);
    
        var listWeek=["segunda","terca","quarta","quinta","sexta","sabado","domingo"];
        var checkboxes=listWeek.map(value=>`<input type="checkbox" name="days" value="${value}"/>${value}<br/>`).join("");
        
        var content=`
            <div style="display:flex;gap:0.3rem;justify-content:end"><button class='delete-matter'>Delete</button> <button class='close-dialog'>✖</button></div>
            <form class='form-dialog-matter' action="/createdatestudy" method="POST">
                <input name='id_matter' value='${res.id}' hidden>
                <div class='dates-checkbox'>${checkboxes}</div>
                <button type="submit">Adicionar</button>
            </form>
        `;
        dialog.innerHTML=content;
        return dialog;
    }
    

    var li=document.createElement('li');
    li.classList.add('card-matters');
    const dialogElement=dialog();
    
    const button=document.createElement('button');
    button.classList.add(`button-matter-${res.name}`); 
    button.textContent=res.name
    const closeDialog=dialogElement.querySelector('.close-dialog');
    closeDialog.addEventListener('click',()=>{dialogElement.close()});
    button.addEventListener('click',()=>{dialogElement.showModal()});
    const deleteMatter=dialogElement.querySelector('.delete-matter');
    deleteMatter.addEventListener('click',(event)=>{
        event.preventDefault();
        fetch('/deletematter', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({id:res.id})
        }).then(()=>location.reload())
    })

   li.appendChild(dialogElement);
   li.appendChild(button);
   
   return li 
}