const userName = document.getElementById("userName");
const welcomeMessage = document.getElementById("welcomeMessage")

function name() {
  let name = "";
  if (localStorage.length == 0) {
    name = prompt("Hi! What's your name?");
    if (name === null || name === ""){
      userName.innerText = "Stranger"
    } else {
      userName.innerText = name;
      localStorage.setItem('userName', name)
    }
  } else {
    name = localStorage.getItem('userName')
    welcomeMessage.innerHTML = `Welcome back <span id="userName">${name}</span>` 
  }
}

name()