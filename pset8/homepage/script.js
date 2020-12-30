let btn = document.querySelector('#btn');

btn.addEventListener('click', function (){
    btn.classList.add('btn', 'btn-success');
    btn.value = 'submitted';
})