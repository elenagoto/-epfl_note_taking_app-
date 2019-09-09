// === HTML ELEMENTS ===
// Gets element that contains the welcome message
const welcomeMessage = document.getElementById("welcomeMessage");
// Gets element inside the welcome message that has the user name
const userWelcome = document.getElementById("userWelcome");
// Gets span to add "back" word to welcome message
const userBack = document.getElementById("userBack");
// Gets the input with the user name
const userName = document.getElementById("userName");
// Get button to login
const loginButton = document.getElementById("loginButton")
// Gets the login form to add the hidden class later
const loginForm = document.getElementById("loginForm");
// Gets the other forms to erase the hidden class later
const forms = document.getElementById("forms");
// Gets create note button
const createButton = document.getElementById("createButton");


// === FUNCTIONS ===
// This sets the userName item if it doesn't exists so there are no conflicts later while adding the user name. To be called when the page is open
function openPage() {
  if (localStorage.length == 0) {
    localStorage.setItem("userName", "")
  } 
}

// This will get the user name from the input 
function getName() {
   // Get user name from form 
  let name = userName.value;
  // Add user name to the existing item in localStorage
  localStorage.userName = name;
  // restore text area to 0 content
  userName.value = "";
  
  return name;
}

// Function to modify classes for hidden elements
function changeHidden() {
  // Hide the login form
  loginForm.classList.add("hidden");
  // make Welcome message and forms visible
  welcomeMessage.classList.remove("hidden")
  forms.classList.remove("hidden");
}

// This function will set the user name in the welcome message
function setName() {
  // if there is no user name in localStorage
  if (localStorage.userName == "") {
    userWelcome.innerText = getName();
  } else {
    // If there is an user name in localStorage
    userWelcome.innerText = localStorage.userName;
  }
}

// This function uses all the previous 3 functions to perform the login of the app
// To be activated below with an EventListener
function logIn() {
  // Only works if there is text in the input element!
  if (userName.value != ""){
    setName();
    changeHidden();
  }
}


// This function is to be called when opening the page so the user doesn't need to log again
function rememberUser() {
  if (localStorage.userName != "") {
    changeHidden();
    userBack.innerText = "back";
    userWelcome.innerText = localStorage.userName;
  } 

}

// This function erases the welcome message once we are in the addnote page. to be called right when the page is opened
function eraseMessage() {
  if (window.location.pathname == "/addnote") {
    welcomeMessage.classList.add("hidden");
  }
}

// === CALLING FUNCTIONS ===
openPage();
rememberUser();
eraseMessage();



// === EVENTS LISTENERS ===
loginButton.addEventListener("click", logIn);
// If the user uses Enter instead of clicking on the button
userName.addEventListener("keyup", () => {
  if(event.key == "Enter") { 
    document.getElementById("loginButton").click();
  }
});