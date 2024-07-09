<template>
    <div>
      <h1>Submitted Forms</h1>
      <div v-for="form in forms" :key="form.id" class="form-item">
        <p>Text: {{ form.text }}</p>
        <div v-if="form.photo">
          <img :src="form.photo" @click="toggleImageSize(form)" :class="{ enlarged: form.isEnlarged }">
        </div>
        <div v-if="form.signature">
          <img :src="form.signature" alt="Signature" class="signature-thumbnail">
        </div>
        <button @click="previewForm(form)">Preview</button>
        <button @click="deleteForm(form.id)">Delete</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'SubmittedForms',
    data() {
      return {
        forms: []
      };
    },
    created() {
      this.fetchForms();
    },
    methods: {
      async fetchForms() {
        try {
          const response = await axios.get('http://192.168.20.170:5000/forms');
          this.forms = response.data.forms.map(form => ({
            ...form,
            isEnlarged: false
          }));
        } catch (error) {
          console.error('Error fetching forms:', error);
        }
      },
      toggleImageSize(form) {
        form.isEnlarged = !form.isEnlarged;
      },
      async previewForm() {
        // Logic to preview the form
        alert('Preview not implemented yet.');
      },
      async deleteForm(formId) {
        try {
          const response = await axios.delete(`http://192.168.20.170:5000/forms/${formId}`);
          if (response.data.success) {
            this.forms = this.forms.filter(form => form.id !== formId);
          } else {
            alert('Form deletion failed');
          }
        } catch (error) {
          console.error('Error deleting form:', error);
        }
      }
    }
  };
  </script>
  
  <style>
  .form-item {
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
    position: relative; /* Ensure the enlarged image stays within bounds */
  }
  
  .form-item img {
    width: 100px;
    height: auto;
    cursor: pointer;
    transition: transform 0.3s ease;
  }
  
  .form-item img.enlarged {
    transform: scale(5);
    z-index: 100;
    position: absolute;
    background: white;
    border: 2px solid #ccc;
    left: 0; /* Adjust positioning as necessary */
    top: 0;  /* Adjust positioning as necessary */
  }
  
  .signature-thumbnail {
    width: 200px;
    height: auto;
  }
  
  button {
    margin-top: 10px;
  }
  </style>
  