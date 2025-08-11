<script setup>
import { RouterView } from 'vue-router'
import HomeView from './views/HomeView.vue';
import NavBar from '@/components/NavBar.vue';
</script>

<template>
  <NavBar/>
  <RouterView />
</template>
<style>
body{
  background: #e2eefc;
  margin:0;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
}
</style>
