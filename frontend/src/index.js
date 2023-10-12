import React from 'react';
import ReactDOM from 'react-dom/client';
import "./assets/css/index.css"
import Homepage from './pages/Homepage';

import 'bootstrap/dist/css/bootstrap.min.css';
import { createBrowserRouter, RouterProvider, Link } from 'react-router-dom';

const root = ReactDOM.createRoot(document.getElementById('root'));

const router = createBrowserRouter([
  {
    path: '/',
    element: <Homepage />
  }
])

root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);