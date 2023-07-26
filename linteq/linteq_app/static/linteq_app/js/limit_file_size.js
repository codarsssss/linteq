const inputFile = document.getElementById('file');
const button = document.getElementById('submit');
const message= document.getElementById('er_message')
inputFile.addEventListener('change', function() {
  const selectedFile = inputFile.files[0];
  if (selectedFile.size > 5000000) {
    console.log('File size is bigger than 5Mb');
    button.disabled=true;
    message.classList.remove('d-none');
  }
  else {
    message.classList.add('d-none')
  }

});
