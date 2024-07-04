<!-- src/components/Login.vue -->
<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginCom',
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://192.168.20.170:5000/login', {
          username: this.username,
          password: this.password
        });
        if (response.data.success) {
          localStorage.setItem('authToken', response.data.token); // 假设后端返回一个 token
          this.$router.push('/form');
        } else {
          alert('Login failed');
        }
      } catch (error) {
        console.error('Error during login:', error);
      }
    }
  }
};
</script>
