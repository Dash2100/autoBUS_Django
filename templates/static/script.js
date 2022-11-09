function on(){
    let response = fetch('/on');
    document.getElementById('on').style.backgroundColor = 'green';
    document.getElementById('off').style.backgroundColor = 'gray';
}

function off(){
    let response = fetch('/off');
    document.getElementById('on').style.backgroundColor = 'gray';
    document.getElementById('off').style.backgroundColor = 'green';
}