<template>
  <div class="analysis-dashboard">
    <h1>Panel de Análisis de Progreso</h1>
    <div class="filters">
      <label for="athleteFilter">Filtrar por Deportista:</label>
      <select id="athleteFilter" v-model="selectedAthlete" @change="fetchProgressData">
        <option v-for="athlete in athletes" :key="athlete.id" :value="athlete.id">
          {{ athlete.username }}
        </option>
      </select>
    </div>
    <div class="charts">
      <canvas id="progressChart"></canvas>
      <canvas id="comparisonChart"></canvas>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'
import axios from 'axios'

export default {
  name: 'AnalysisDashboard',
  setup() {
    const athletes = ref([])
    const selectedAthlete = ref(null)
    let progressChart = null
    let comparisonChart = null

    const fetchAthletes = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/users/')
        athletes.value = response.data
        if (athletes.value.length > 0) {
          selectedAthlete.value = athletes.value[0].id
          fetchProgressData()
        }
      } catch (error) {
        console.error('Error fetching athletes:', error)
      }
    }

    const fetchProgressData = async () => {
      if (!selectedAthlete.value) return
      try {
        // Fetch progress data for selected athlete
        const response = await axios.get(`http://localhost:8000/api/training-plans/?user=${selectedAthlete.value}`)
        const plans = response.data

        // Prepare data for charts (example: sessions count over time)
        const labels = []
        const dataPoints = []

        plans.forEach(plan => {
          plan.sessions.forEach(session => {
            labels.push(session.date)
            dataPoints.push(session.exercise_entries.length)
          })
        })

        renderProgressChart(labels, dataPoints)
        renderComparisonChart()
      } catch (error) {
        console.error('Error fetching progress data:', error)
      }
    }

    const renderProgressChart = (labels, dataPoints) => {
      if (progressChart) {
        progressChart.destroy()
      }
      const ctx = document.getElementById('progressChart').getContext('2d')
      progressChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Número de ejercicios por sesión',
            data: dataPoints,
            borderColor: 'rgba(75, 192, 192, 1)',
            fill: false,
          }]
        },
        options: {
          responsive: true,
          scales: {
            x: {
              type: 'time',
              time: {
                unit: 'day'
              }
            },
            y: {
              beginAtZero: true
            }
          }
        }
      })
    }

    const renderComparisonChart = () => {
      if (comparisonChart) {
        comparisonChart.destroy()
      }
      const ctx = document.getElementById('comparisonChart').getContext('2d')
      // Example static data for comparison
      comparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Deportista A', 'Deportista B', 'Deportista C'],
          datasets: [{
            label: 'Progreso promedio',
            data: [65, 59, 80],
            backgroundColor: [
              'rgba(255, 99, 132, 0.5)',
              'rgba(54, 162, 235, 0.5)',
              'rgba(255, 206, 86, 0.5)'
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      })
    }

    onMounted(() => {
      fetchAthletes()
    })

    watch(selectedAthlete, () => {
      fetchProgressData()
    })

    return {
      athletes,
      selectedAthlete
    }
  }
}
</script>

<style scoped>
.analysis-dashboard {
  padding: 20px;
}

.filters {
  margin-bottom: 20px;
}

.charts {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

canvas {
  max-width: 100%;
  height: 300px;
  flex: 1 1 45%;
}
</style>
