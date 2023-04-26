import './Assets/Styles/App.css';
import React from 'react';
import { RouterProvider } from 'react-router-dom';
import router from './Routes';
import axios from 'axios';

function App() {
  axios.defaults.baseURL = 'http://localhost:5000';

  return (
    <div className="App">
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
