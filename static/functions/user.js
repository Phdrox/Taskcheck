
const buttonDelete=document.querySelector('#button-delete');

const handleDelete=()=>{
  try{
    fetch('deleteuser',{method:'POST'})
    .then(res=>res.text())
    .then(res=>window.location.href='/')
  }
  catch(e){console.log("deu erro")}
}

buttonDelete.addEventListener('click',handleDelete)

