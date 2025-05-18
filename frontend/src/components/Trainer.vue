<template>
  <div>
    <h1>Panel de Entrenador</h1>
    <LogoutButton />
    <p>Bienvenido, entrenador. Aquí puedes diseñar planes y monitorear el progreso de tus deportistas.</p>
    <button @click="generatePlan">Generar Plan de Entrenamiento</button>
    <div v-if="plan">
      <h2>Plan Generado:</h2>
      <div v-for="(session, index) in plan.sessions" :key="index">
        <h3>Sesión {{ index + 1 }} - {{ session.date }}</h3>
        <ul>
          <li v-for="(exercise, idx) in session.exercises" :key="idx">
            {{ exercise.name }} - Sets: {{ exercise.sets }}, Reps: {{ exercise.reps }}
          </li>
        </ul>
      </div>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios'
import LogoutButton from './LogoutButton.vue'

export default {
  name: 'Trainer',
  components: {
    LogoutButton
  },
  data() {
    return {
      plan: null,
      error: ''
    }
  },
  methods: {
    async generatePlan() {
      this.error = ''
      try {
        const accessToken = localStorage.getItem('access_token')
        const response = await axios.post('http://localhost:8000/api/training-plans/generate/', {
          user_profile: {
            physical_info: 'average',
            condition_level: 'intermediate',
            restrictions: [],
            availability: ['Monday', 'Wednesday', 'Friday']
          },
          training_history: [],
          objectives: {
            type: 'strength',
            timeframe: '3 months',
            intensity: 'medium'
          }
        }, {
          headers: {
            Authorization: 'Bearer ' + accessToken
          }
        })
        this.plan = response.data.plan
      } catch (err) {
        this.error = 'Error al generar el plan de entrenamiento.'
      }
    }
  }
}
</script>

<style scoped>
h1 {
  color: #34495e;
}
.error {
  color: red;
  margin-top: 1rem;
}
</style>
