<!-- src/components/Navbar.vue -->
<template>
    <nav>
      <ul>
        <li><router-link to="/form">Form</router-link></li>
        <li><router-link to="/records">Records</router-link></li>
      </ul>
    </nav>
  </template>
  
  <style>
  nav {
    background-color: #333;
    color: white;
    padding: 10px;
  }
  
  nav ul {
    list-style: none;
    padding: 0;
    display: flex;
    justify-content: space-around;
  }
  
  nav li {
    margin: 0 10px;
  }
  
  nav a {
    color: white;
    text-decoration: none;
  }
  
  nav a.router-link-active {
    font-weight: bold;
  }
  </style>
  