const inputFile = document.getElementById('file');
const button = document.getElementById('submit');
const message= document.getElementById('er_message')

button.disabled=true;
inputFile.addEventListener('change', function() {
  const selectedFile = inputFile.files[0];
  if (selectedFile.size > 1073741824) {
    message.classList.remove('d-none');
  }
  else {
    button.disabled=false;
    message.classList.add('d-none')
  }

});
