<script setup>
import { useRoute, useRouter } from 'vue-router';
const router = useRouter();
const route = useRoute();
function go(source) {
    router.push(source);
}
</script>
<template>
    <div class="navbar">
        <div class="title">
            <h2>TechBridge</h2>
        </div>
        <div class="navMenu">
            <ul>
                <li @click="go('/')">Home</li>
                <li @click="go('/jobs')">Jobs</li>
                <li @click="go('/assessment')">Assessment</li>
                <li @click="go('/jobs')">Courses</li>
                <li @click="go('/jobs')">Profile</li>
            </ul>
        </div>
    </div>
</template>
<style>
.title{
    margin-left: 50px;
}
.navbar{
    width:100%;
    height: 20%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    font-family:Verdana, Geneva, Tahoma, sans-serif;
    font-size: 1rem;
    color: #4c5a68;
    box-shadow: 0 4px 5px -1px rgba(0, 0, 0, 0.1);
    margin:0;
}

.navMenu ul{
    list-style: none;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content:center;
    gap:40px;
    margin-right: 50px;
    padding-top: 5px;
    height: 100%;
}
.navMenu li{
    padding:5px;
}
.navMenu li:hover{
    background-color: #4c5a68;
    color:#F8FAFC;
    border-radius: 5px;
    cursor: pointer;
}
</style>