<template>
  <div>
    <h2>Crear Nuevo Plan de Entrenamiento</h2>
    <form @submit.prevent="submitPlan">
      <div>
        <label for="name">Nombre del Plan:</label>
        <input id="name" v-model="name" required />
      </div>
      <div>
        <label for="goals">Objetivos:</label>
        <textarea id="goals" v-model="goals"></textarea>
      </div>
      <button type="submit">Crear Plan</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'TrainingPlanCreate',
  setup() {
    const name = ref('')
    const goals = ref('')
    const error = ref('')
    const router = useRouter()

    const submitPlan = async () => {
      try {
        const response = await axios.post('http://localhost:8000/api/training-plans/', {
          name: name.value,
          goals: goals.value
        }, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        router.push(`/training-plan/${response.data.id}`)
      } catch (err) {
        error.value = 'Error al crear el plan'
      }
    }

    return { name, goals, error, submitPlan }
  }
}
</script>

<style scoped>
.error {
  color: red;
  margin-top: 1rem;
}
</style>
