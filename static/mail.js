
const firebaseConfig = {
  apiKey: "AIzaSyBsJuhZqpQGzIiBb5borCa9odEfVSI9xmY",
  authDomain: "krishi-7a663.firebaseapp.com",
  projectId: "krishi-7a663",
  storageBucket: "krishi-7a663.firebasestorage.app",
  messagingSenderId: "590543476308",
  appId: "1:590543476308:web:54765f31969d31f0c33fc1",
  measurementId: "G-YGTBCB4TSR"
};
  firebase.initializeApp(firebaseConfig);

  var contactFormDB = firebase.database().ref("message");
  document.getElementById("contactForm").addEventListener("submit", submitForm);

  function submitForm(e) {
    e.preventDefault();
  
    var name = getElementVal("name");
    var emailid = getElementVal("emailid");
    var msgContent = getElementVal("msgContent");
  
    saveMessages(name, emailid, msgContent);
  
    //   enable alert
    document.querySelector(".alert").style.display = "block";
  
    //   remove the alert
    setTimeout(() => {
      document.querySelector(".alert").style.display = "none";
    }, 3000);
  
    //   reset the form
    document.getElementById("contactForm").reset();
  } 

  const saveMessages = (name, emailid, msgContent) => {
    var newContactForm = contactFormDB.push();
  
    newContactForm.set({
      name: name,
      emailid: emailid,
      msgContent: msgContent,
    });
  };
  const getElementVal = (id) => {
    return document.getElementById(id).value;
  };
