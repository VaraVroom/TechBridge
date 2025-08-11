<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios'



const router = useRouter();
const route = useRoute();
function go(source) {
    router.push(source);
}

const questions=ref([]);
const currentQuestionIndex=ref(0);
const selectedOption=ref('');
const options=['Python','Java'];
const startTest=ref(false);
const userAnswers=ref({});
var skill = ref(selectedOption)
var level = ref(null)
const recommendations = ref([])
function startAssessment(skill){
  if(skill!=''){
  startTest.value=true;
  const path="https://varavroom.github.io/questions/"+selectedOption.value+"QB.json";
  console.log(path);
  fetch(path)
  .then(response => {
    console.log("response",response);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json(); // Parse JSON
  })
  .then(data => {
    const beginnerQuestions = getRandomQuestions(data, "Beginner", 2);
    const intermediateQuestions = getRandomQuestions(data, "Intermediate", 2);
    const advancedQuestions = getRandomQuestions(data, "Advanced", 1);

    /*console.log("Beginner Questions:", beginnerQuestions);
    console.log("Intermediate Questions:", intermediateQuestions);
    console.log("Advanced Questions:", advancedQuestions);*/
    questions.value=[...beginnerQuestions,...advancedQuestions,...intermediateQuestions];
    
    console.log(questions.value);
  })
  .catch(error => {
    console.error("Error fetching questions:", error);
  });
  }
  else{
    alert("Please select a skill.")
  }
}

// Function to filter and get random questions
function getRandomQuestions(data, difficulty, count) {
  const filteredQuestions = data.filter(
    question => question.difficulty === difficulty
  );
  return filteredQuestions.sort(() => 0.5 - Math.random()).slice(0, count);
}
const nextQuestion = () => {
  currentQuestionIndex.value++;
  console.log(userAnswers.value);
  console.log(questions[currentQuestionIndex].option);
};
const calculateScore = () => {
  let score = {'Beginner':0,'Intermediate':0,'Advanced':0};
  questions.value.forEach((question, index) => {
    if (userAnswers.value[index] == true) {
      score[question.difficulty]++;
    }
  });
  if(score.Beginner<7) level.value="Beginner"
  else if(score.Intermediate<7) level.value="Intermediate"
  else if(score.Advanced<7) level.value="Advanced"
  else level=""
  return score;
};

const recommendCourse = async () =>{
  try{
  const response = await axios.post('http://127.0.0.1:5000/courses',{"keyword":skill.value+" "+level.value},
    {
      headers: {
          'Content-Type': 'application/json'
        }
    }
  )
    recommendations.value = response.data.recommendations
  }
  catch(err){
    console.error(err)
  }
}
</script>

<template>
  <div class="assessment" v-if="!startTest">
    <h2>Skill assessment</h2>
    <p>Assess your technical skills and pinpoint areas for growth.</p>
    <div class="dropdown">
    <select v-model="selectedOption">
      <option value="" disabled selected>Select a skill</option>
      <option v-for="option in options" :key="option" :value="option">
        {{ option }}
      </option>
    </select>
    <button class="go" @click="startAssessment(selectedOption)">Go</button>
    </div>
  </div>
  <div class="skillTest" v-else>
    <p class="testHead">{{ selectedOption }} Assessment</p>
    <div v-if="currentQuestionIndex < 5" class="questionIndex">
        <p class="question">
          Q{{ currentQuestionIndex + 1 }}: {{ questions[currentQuestionIndex].question_text }}
        </p>
        <div v-for="(option, index) in questions[currentQuestionIndex].options" :key="index" class="optionDiv">
          <label>
            <input
              type="radio"
              :name="'question' + currentQuestionIndex"
              :value="option.is_correct"
              v-model="userAnswers[currentQuestionIndex]"
            />
            {{ option.option_text }}
          </label>
        </div>

        <button @click="nextQuestion" :disabled="userAnswers[currentQuestionIndex] === undefined" class="next">
          Next
        </button>
    </div>
    <div v-else class="score">
    <p id="scores">Scores </p>
    <p>Beginner: {{calculateScore().Beginner}}</p>
    <p>Intermediate: {{ calculateScore().Intermediate }}</p>
    <p>Advanced: {{calculateScore().Advanced}}</p>

    <div class="results">
      <div v-if="calculateScore().Beginner<7" class="level">
        <p>You currently need to improve your Basic Fundamentals.</p>
      </div>
      <div v-else-if="calculateScore().Intermediate<7" class="level">
        <p>You are currently at beginner level. You need to go to intermediate level</p>
      </div>
      <div v-else-if="calculateScore().Advanced<7" class="level">
        <p>You are currently at intermediate level. You need to go to advanced level</p>
      </div>
      <div v-else class="level">
        <p>You are at advanced level. Keep solving problems!</p>
      </div>
      <div class="courses">
        <button @click="recommendCourse" id="courseRecommend">Recommend courses</button>
        <table v-if="recommendations.length>0">
          <tbody>
            <tr>
              <th>Title</th>
              <th>URL</th>
              <th>Duration</th>
              <th>Site</th>
            </tr>
            <tr v-for="course in recommendations">
              <td>{{course["Title"]}}</td>
              <td><a :href="course['URL']" target="_blank">{{ course["URL"]}}</a></td>
              <td>{{ course["Duration"] }}</td>
              <td>{{ course["Site"] }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="buttons">
      <button class="goHome" @click="go('/')">Go Home</button>
      <button class="goTest" @click="go('/assessment')">Take test</button>
    </div>
    </div>
  </div>
</template>

<style>
.assessment{
  width:80%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: auto;
  margin-top: 150px;
}
.go{
  border:none;
  background-color: #BCCCDC;
  height: 30px;
  padding:0 10px;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 600;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  color:#4c5a68;
  cursor: pointer;
}
.go:hover{
  color:#BCCCDC;
  background-color: #4c5a68;
}
.dropdown{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap:20px;
}
.dropdown select{
  height: 30px;
  border-radius: 5px;
  border: solid #4c5a68 2px;
  color:#4c5a68;
  font-weight: 300;
  font-size: 1rem;
}
.skillTest{
  width: 80%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin: auto;
  margin-top: 50px;
}
.questionIndex{
  padding-left: 10px;
  padding-bottom: 10px;
  border:solid #4c5a68 2px;
  border-radius: 10px;
}
.next{
  margin-top: 20px;
}
.optionDiv{
  margin-top: 10px;
}
.testHead{
  font-size: 1rem;
  font-weight: 600;
}
#scores{
  font-weight: 600;
}
.score {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 20px;
  background: #f9f9f9;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  font-family: 'Segoe UI', sans-serif;
}

#scores {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.score p {
  margin: 0.5rem 0;
  color: #444;
  line-height: 1.6;
}

.results {
  margin-top: 2rem;
}

.level p {
  background-color: #eef5ff;
  padding: 1rem;
  border-left: 4px solid #3b82f6;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  color: #1e40af;
}

#courseRecommend {
  background-color: #BCCCDC;
  color: #4c5a68;
  padding: 0.7rem 1.2rem;
  border: none;
  border-radius: 8px;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 600;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  font-size: 1rem;
  cursor: pointer;
  margin-bottom: 1rem;
  transition: background-color 0.3s ease;
}

#courseRecommend:hover {
  background-color: #4c5a68;
  color:#BCCCDC;
}

.courses table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.courses td {
  padding: 0.75rem;
  border-bottom: 1px solid #e5e7eb;
  color: #333;
  font-size: 0.95rem;
}

.courses tr:hover {
  background-color: #f1f5f9;
}
</style>
