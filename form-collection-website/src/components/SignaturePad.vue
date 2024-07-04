<!-- src/components/SignaturePad.vue -->
<template>
  <div>
    <h1>Submit Form with Signature</h1>
    <form @submit.prevent="submitForm">
      <div>
        <label for="text">Text:</label>
        <input type="text" id="text" v-model="text" required>
      </div>
      <div>
        <label for="photo">Photo:</label>
        <input type="file" id="photo" @change="onFileChange">
      </div>
      <div v-if="thumbnail">
        <div class="thumbnail-container">
          <img :src="thumbnail" @click="toggleImageSize" :class="{ enlarged: isEnlarged }">
          <button type="button" @click="removePhoto">Delete</button>
        </div>
      </div>
      <div>
        <label for="signature">Signature:</label>
        <div class="signature-container">
          <canvas ref="signaturePad" class="signature-pad"></canvas>
        </div>
        <button type="button" @click="clearSignature">Clear</button>
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
import SignaturePad from 'signature_pad';
import axios from 'axios';

export default {
  name: 'SignaturePad',
  data() {
    return {
      text: '',
      photo: null,
      thumbnail: null,
      isEnlarged: false,
      signaturePad: null
    };
  },
  mounted() {
    const canvas = this.$refs.signaturePad;
    this.signaturePad = new SignaturePad(canvas);
    window.addEventListener('resize', this.resizeCanvas);
    this.resizeCanvas();
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.resizeCanvas);
  },
  methods: {
    resizeCanvas() {
      const canvas = this.$refs.signaturePad;
      const ratio = Math.max(window.devicePixelRatio || 1, 1);
      canvas.width = 400 * ratio;
      canvas.height = 200 * ratio;
      canvas.getContext('2d').scale(ratio, ratio);
      this.signaturePad.clear();
    },
    clearSignature() {
      this.signaturePad.clear();
    },
    onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.photo = file;
        this.thumbnail = URL.createObjectURL(file);
      }
    },
    removePhoto() {
      this.photo = null;
      this.thumbnail = null;
      document.getElementById('photo').value = '';
    },
    toggleImageSize() {
      this.isEnlarged = !this.isEnlarged;
    },
    async submitForm() {
      if (this.signaturePad.isEmpty()) {
        alert('Please provide a signature first.');
        return;
      }

      const formData = new FormData();
      formData.append('text', this.text);
      formData.append('photo', this.photo);
      formData.append('signature', this.signaturePad.toDataURL());

      try {
        const response = await axios.post('http://192.168.20.170:5000/submit', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        if (response.data.success) {
          alert('Form submitted successfully');
          this.text = '';
          this.photo = null;
          this.thumbnail = null;
          this.signaturePad.clear();
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

<style>
.signature-container {
  position: relative;
  border: 1px solid #ccc;
  width: 400px;
  height: 200px;
  margin: 0 auto; /* Center horizontally */
  display: flex;
  justify-content: center;
  align-items: center;
}

.signature-pad {
  width: 100%;
  height: 100%;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center; /* Center the form elements */
}

button {
  margin-top: 10px;
}

.thumbnail-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10px;
}

.thumbnail-container img {
  width: 100px;
  height: auto;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.thumbnail-container img.enlarged {
  transform: scale(5);
  z-index: 100;
  position: absolute;
  background: white;
  border: 2px solid #ccc;
}

.thumbnail-container button {
  margin-top: 10px;
}
</style>
