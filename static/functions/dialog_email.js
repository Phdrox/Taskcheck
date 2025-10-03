var buttondialog = document.querySelector('#button-dialog-pass');
var dialog = document.querySelector("#dialog-pass");
var validateEmail = dialog.querySelector("#email-validate");
var input=dialog.querySelector('#dialog-email-input')
var openDialog = () => {
  if (!dialog.open) dialog.showModal();
}

var closeDialog = (e) => {
  dialog.close();
}

buttondialog.addEventListener('click', openDialog);

if (input.ariaValueMax.length>1){
  validateEmail?.addEventListener('click', closeDialog);
}

