import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-app.js";
 import {getAuth, onAuthStateChanged, signOut} from "https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js";
 import{getFirestore, getDoc, doc} from "https://www.gstatic.com/firebasejs/11.0.2/firebase-firestore.js"

 
  const firebaseConfig = {
    apiKey: "AIzaSyBsJuhZqpQGzIiBb5borCa9odEfVSI9xmY",
    authDomain: "krishi-7a663.firebaseapp.com",
    projectId: "krishi-7a663",
    storageBucket: "krishi-7a663.firebasestorage.app",
    messagingSenderId: "590543476308",
    appId: "1:590543476308:web:54765f31969d31f0c33fc1",
    measurementId: "G-YGTBCB4TSR"
  };
  // Initialize Firebase
  const app = initializeApp(firebaseConfig);

  const auth=getAuth();
  const db=getFirestore();

  onAuthStateChanged(auth, (user)=>{
    const loggedInUserId=localStorage.getItem('loggedInUserId');
    if(loggedInUserId){
        console.log(user);
        const docRef = doc(db, "users", loggedInUserId);
        getDoc(docRef)
        .then((docSnap)=>{
            if(docSnap.exists()){
                const userData=docSnap.data();
                document.getElementById('loggedUserFName').innerText=userData.firstName;
                document.getElementById('loggedUserEmail').innerText=userData.email;
                document.getElementById('loggedUserLName').innerText=userData.lastName;

            }
            else{
                console.log("no document found matching id")
            }
        })
        .catch((error)=>{
            console.log("Error getting document");
        })
    }
    else{
        console.log("User Id not Found in Local storage")
    }
  })

  const logoutButton=document.getElementById('logout');

  logoutButton.addEventListener('click',()=>{
    localStorage.removeItem('loggedInUserId');
    signOut(auth)
    .then(()=>{
        window.location.href='/login';
    })
    .catch((error)=>{
        console.error('Error Signing out:', error);
    })
  })