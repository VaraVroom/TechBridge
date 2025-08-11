<template>
    <div class="resume-upload">
    <input type="file" @change="handleFileChange"/>
    <button @click="uploadResume">Get Recommendations</button>

    <table v-if="recommendations.length">
      <tbody>
      <tr>
        <th>Position</th>
        <th>Company</th>
        <th>Average Salary</th>
        <th>Location</th>
        <th>Job_Description</th>
      </tr>

      <tr v-for="(job,index) in recommendations" :key="index">
        <td>{{ job["Job Title"] }}</td>
        <td>{{ job["Company Name"] }}</td>
        <td>{{ job["Average Salary"] }}$</td>
        <td>{{ job["Location"] }}</td>
        <td>{{ job["Processed_JD"] }}</td>
      </tr>

      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const file = ref(null)
const recommendations = ref([])

const handleFileChange = (e) => {
  file.value = e.target.files[0]
}

const uploadResume = async () => {
  if (!file.value) {
    alert('Please select a PDF file.')
    return
  }

  const formData = new FormData()
  formData.append('resume', file.value)

  try {
    const response = await axios.post('http://127.0.0.1:5000/jobs', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    recommendations.value = response.data.recommendations
    console.log("file posted")
  } catch (err) {
    console.error(err)
    alert('Error uploading file or getting recommendations.')
  }
}
</script>

<style scoped>
.resume-upload {
  max-width: 1000px;
  margin: 40px auto;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.resume-upload input[type="file"] {
  display: block;
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  width: 100%;
  box-sizing: border-box;
  background-color: #fff;
  transition: border-color 0.3s;
}

.resume-upload input[type="file"]:hover {
  border-color: #888;
}

.resume-upload button {
  display: inline-block;
  padding: 0.6rem 1.2rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.resume-upload button:hover {
  background-color: #4338ca;
}

table {
  width: 100%;
  margin-top: 2rem;
  border-collapse: collapse;
  background-color: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f3f4f6;
  font-weight: 600;
  color: #374151;
}

td {
  color: #4b5563;
  border-top: 1px solid #afc5ef;
  border-bottom: 1px solid #afc5ef;
}

tr:hover {
  background-color: #f9fafb;
  transition: background-color 0.2s ease-in-out;
}
</style>
