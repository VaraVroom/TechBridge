<script setup>
import { useRoute, useRouter } from 'vue-router';
const router = useRouter();
const route = useRoute();
function go(source) {
    router.push(source);
}
</script>
<template>
  <div class="homeContent">
    <div class="homeText">
      <p>
      <span class="tagline">Connecting talent with jobs</span>
      through personalized skill-building and career insights.
      </p>
      <div class="buttons">
      <button class="toResume" @click="go('/jobs')">Analyse Resume</button>
      <button class="toAssessment" @click="go('/assessment')">Test Skills</button>
      </div>
    </div>
    <img src="../icons/jobsearch.svg">
  </div>
</template>
<style>
img{
  height: 400px;
  width: 400px;
  margin-top: 10px;
}
.homeContent{
  margin:auto;
  margin-top:80px;
  width:90%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content:center;
  gap:90px;
}
.homeText{
width:50%;
}
.tagline{
  font-size: 3rem;
  font-weight: 800;
  color:#4c5a68;
}
.homeText p{
  font-size: 1.3rem;
  color: #4c5a68;
}
.buttons{
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 40px;
}
.buttons button{
  border:none;
  background-color: #BCCCDC;
  height: 40px;
  padding:0 10px;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 600;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  color:#4c5a68;
  cursor: pointer;
}
.buttons button:hover{
  color:#BCCCDC;
  background-color: #4c5a68;
}
</style>