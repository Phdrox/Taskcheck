modal=document.querySelector('#dialog-register')
buttonShow =document.querySelector('#buttonModal')
buttonClose =document.querySelector('#buttonClose')

//mostar modal de registro 
buttonShow.onclick=function(){
    modal.showModal();
}
//fechar botão de registro 
buttonClose.onclick=function(){
    modal.close();
}


