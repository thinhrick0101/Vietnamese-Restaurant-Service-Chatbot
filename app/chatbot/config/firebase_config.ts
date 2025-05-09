import { initializeApp } from 'firebase/app';
import { getDatabase } from 'firebase/database';


const firebaseConfig = {
  apiKey: "AIzaSyDAp7tO6-D8qLLC5Myqby9LSktfXsJUau0",
  authDomain: "chatbot-service-ba6d2.firebaseapp.com",
  databaseURL: "https://chatbot-service-ba6d2-default-rtdb.firebaseio.com",
  projectId: "chatbot-service-ba6d2",
  storageBucket: "chatbot-service-ba6d2.firebasestorage.app",
  messagingSenderId: "149259511455",
  appId: "1:149259511455:web:2d375b003a2198c958e4aa",
  measurementId: "G-9WMZV6NHQZ"
}

  const app = initializeApp(firebaseConfig);
  const fireBaseDB = getDatabase(app);

  export { fireBaseDB };