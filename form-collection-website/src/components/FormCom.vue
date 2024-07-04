<!-- src/components/Form.vue -->
<template>
  <div>
    <h1>Submit Form</h1>
    <form @submit.prevent="submitForm">
      <div>
        <label for="text">Text:</label>
        <input type="text" id="text" v-model="text" required>
      </div>
      <div>
        <label for="photo">Photo:</label>
        <input type="file" id="photo" @change="onFileChange">
      </div>
      <div>
        <label for="signature">Signature:</label>
        <input type="file" id="signature" @change="onFileChange">
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'FormCom',
  data() {
    return {
      text: '',
      photo: null,
      signature: null
    };
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0];
      if (event.target.id === 'photo') {
        this.photo = file;
      } else if (event.target.id === 'signature') {
        this.signature = file;
      }
    },
    async submitForm() {
      const formData = new FormData();
      formData.append('text', this.text);
      formData.append('photo', this.photo);
      formData.append('signature', this.signature);

      try {
        const response = await axios.post('http://192.168.20.170:5000/submit', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        if (response.data.success) {
          alert('Form submitted successfully');
        } else {
          alert('Form submission failed');
        }
      } catch (error) {
        console.error('Error during form submission:', error);
      }
    }
  }
};
</script>
