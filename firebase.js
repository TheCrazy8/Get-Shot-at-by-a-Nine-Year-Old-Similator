// Import and configure Firebase
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.2/firebase-app.js";
import { getDatabase, ref, set, get, onValue } from "https://www.gstatic.com/firebasejs/10.7.2/firebase-database.js";

// Your Firebase configuration (replace with your project’s settings!)
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  databaseURL: "https://YOUR_PROJECT_ID.firebaseio.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

// Example: Set a cloud variable
export function setCloudVariable(name, value) {
  set(ref(db, 'variables/' + name), value);
}

// Example: Get a cloud variable (callback receives value)
export function getCloudVariable(name, callback) {
  const variableRef = ref(db, 'variables/' + name);
  onValue(variableRef, (snapshot) => {
    callback(snapshot.val());
  });
}

// Example usage:
// setCloudVariable("highscore", 12345);
// getCloudVariable("highscore", (value) => console.log("Highscore:", value));