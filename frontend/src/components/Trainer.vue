<template>
  <div>
    <h1>Panel de Entrenador</h1>
    <LogoutButton />
    <p>Bienvenido, entrenador. Aquí puedes diseñar planes y monitorear el progreso de tus deportistas.</p>

    <div>
      <label for="athlete-select">Selecciona un deportista:</label>
      <select id="athlete-select" v-model="selectedAthlete" @change="fetchTrainingPlans">
        <option disabled value="">-- Selecciona --</option>
        <option v-for="athlete in athletes" :key="athlete.id" :value="athlete.id">
          {{ athlete.username }}
        </option>
      </select>
    </div>

    <button @click="generatePlan" :disabled="!selectedAthlete">Generar Plan de Entrenamiento</button>

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

    <div v-if="trainingPlans.length">
      <h2>Planes de Entrenamiento del Deportista</h2>
      <ul>
        <li v-for="planItem in trainingPlans" :key="planItem.id">
          {{ planItem.name }} - Creado: {{ planItem.created_at }}
        </li>
      </ul>
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
      athletes: [],
      selectedAthlete: '',
      plan: null,
      trainingPlans: [],
      error: ''
    }
  },
  created() {
    this.fetchAthletes()
  },
  methods: {
    async fetchAthletes() {
      try {
        const accessToken = localStorage.getItem('access_token')
        const response = await axios.get('http://localhost:8000/api/users/?role=athlete', {
          headers: {
            Authorization: 'Bearer ' + accessToken
          }
        })
        this.athletes = response.data
      } catch (err) {
        this.error = 'Error al obtener la lista de deportistas.'
      }
    },
    async fetchTrainingPlans() {
      if (!this.selectedAthlete) {
        this.trainingPlans = []
        return
      }
      try {
        const accessToken = localStorage.getItem('access_token')
        const response = await axios.get(`http://localhost:8000/api/training-plans/?user=${this.selectedAthlete}`, {
          headers: {
            Authorization: 'Bearer ' + accessToken
          }
        })
        this.trainingPlans = response.data
      } catch (err) {
        this.error = 'Error al obtener los planes de entrenamiento.'
      }
    },
    async generatePlan() {
      this.error = ''
      if (!this.selectedAthlete) {
        this.error = 'Por favor, seleccione un deportista.'
        return
      }
      try {
        const accessToken = localStorage.getItem('access_token')
        // For demonstration, using static user profile and objectives; ideally fetch real profile and history
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
        this.fetchTrainingPlans()
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
