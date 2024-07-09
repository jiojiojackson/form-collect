<template>
  <div>
    <Navbar />
    <h1>Submitted Records</h1>
    <div v-if="records.length">
      <div v-for="record in records" :key="record.id" class="record">
        <p>Text: {{ record.text }}</p>
        <p>photo:</p>
        <img :src=getPhotoUrl(record.photoUuid) alt="Photo" class="thumbnail" @click="previewImage(record.photoUuid)">
        <p>Signature:</p>
        <img :src=getPhotoUrl(record.signUuid) alt="Photo" class="thumbnail" @click="previewImage(record.signUuid)">
        <button @click="deleteRecord(record.id)">Delete</button>
      </div>
    </div>
    <div v-else>
      <p>No records found.</p>
    </div>

    <div v-if="preview">
      <div class="preview-overlay" @click="preview = ''">
        <img :src="preview" class="preview-image">
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from './NavBar.vue';

export default {
  name: 'RecordsPage',
  components: { Navbar },
  data() {
    return {
      records: [],
      preview: '',
      backend_host: process.env.VUE_APP_BACKEND_HOST
    };
  },
  async mounted() {
    await this.fetchRecords();
  },
  computed: {
    getPhotoUrl() {
      return (uuid) => {
        return `http://${this.backend_host}:5000/uploads/${uuid}`;
      }
    }
  },
  methods: {
    async fetchRecords() {
      try {
        const response = await axios.get(`http://${this.backend_host}:5000/records/${localStorage.getItem('username')}`);
        this.records = response.data.records;
      } catch (error) {
        console.error('Error fetching records:', error);
      }
    },
    async deleteRecord(id) {
      try {
        const response = await axios.delete(`http://${this.backend_host}:5000/records/${id}`);
        if (response.data.success) {
          this.records = this.records.filter(record => record.id !== id);
        } else {
          alert('Failed to delete the record');
        }
      } catch (error) {
        console.error('Error deleting record:', error);
      }
    },
    previewImage(photo) {
      this.preview = `http://${this.backend_host}:5000/uploads/${photo}`;
    }
  }
};
</script>

<style>
.record {
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px 0;
}

.thumbnail {
  width: 100px;
  cursor: pointer;
}

.signature {
  width: 200px;
  height: auto;
}

.preview-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.preview-image {
  max-width: 90%;
  max-height: 90%;
}
</style>
