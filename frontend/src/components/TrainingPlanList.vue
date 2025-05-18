<template>
  <div>
    <h2>Mis Planes de Entrenamiento</h2>
    <ul>
      <li v-for="plan in trainingPlans" :key="plan.id">
        <router-link :to="`/training-plan/${plan.id}`">{{ plan.name }}</router-link>
      </li>
    </ul>
    <button @click="createPlan">Crear Nuevo Plan</button>
  </div>
</template>

<script>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'TrainingPlanList',
  setup() {
    const trainingPlans = ref([])
    const router = useRouter()

    const fetchPlans = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/training-plans/', {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        trainingPlans.value = response.data
      } catch (error) {
        console.error('Error fetching training plans:', error)
      }
    }

    const createPlan = () => {
      router.push('/training-plan/create')
    }

    onMounted(() => {
      fetchPlans()
    })

    return { trainingPlans, createPlan }
  }
}
</script>
