import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './login.js';
import Register from './register.js';
import Chat from './chat.js';
import { useNavigate } from 'react-router-dom';

const root = document.getElementById('root');

// decided to use a react router after knowing how convinient it makes redirection and references, 
// rather than using a redirect component
// the application is also single page, as in dynamically rewriting the current web page with new data from the web server,
// which makes loading quicker. 

ReactDOM.createRoot(root).render(
  <Router>
    <Routes>
      <Route path="/chat/:chatId" element={<Chat />} />
      <Route path="/" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/chat" element={<Chat />} />
    </Routes>
  </Router>
);