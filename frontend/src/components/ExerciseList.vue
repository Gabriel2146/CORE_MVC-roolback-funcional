<template>
  <div class="exercise-list">
    <h2>Catálogo de Ejercicios</h2>
    <button @click="showAddForm = true">Agregar Ejercicio</button>

    <div v-if="showAddForm">
      <h3>Nuevo Ejercicio</h3>
      <form @submit.prevent="addExercise">
        <div>
          <label>Nombre:</label>
          <input v-model="newExercise.name" required />
        </div>
        <div>
          <label>Categoría:</label>
          <input v-model="newExercise.category" />
        </div>
        <div>
          <label>Grupo Muscular:</label>
          <input v-model="newExercise.muscle_group" />
        </div>
        <div>
          <label>Dificultad:</label>
          <input v-model="newExercise.difficulty" />
        </div>
        <div>
          <label>Equipamiento:</label>
          <input v-model="newExercise.equipment" />
        </div>
        <button type="submit">Guardar</button>
        <button type="button" @click="cancelAdd">Cancelar</button>
      </form>
    </div>

    <ul>
      <li v-for="exercise in exercises" :key="exercise.id">
        <strong>{{ exercise.name }}</strong> - {{ exercise.category }} - {{ exercise.muscle_group }}
        <button @click="editExercise(exercise)">Editar</button>
        <button @click="deleteExercise(exercise.id)">Eliminar</button>
      </li>
    </ul>

    <div v-if="showEditForm">
      <h3>Editar Ejercicio</h3>
      <form @submit.prevent="updateExercise">
        <div>
          <label>Nombre:</label>
          <input v-model="editExerciseData.name" required />
        </div>
        <div>
          <label>Categoría:</label>
          <input v-model="editExerciseData.category" />
        </div>
        <div>
          <label>Grupo Muscular:</label>
          <input v-model="editExerciseData.muscle_group" />
        </div>
        <div>
          <label>Dificultad:</label>
          <input v-model="editExerciseData.difficulty" />
        </div>
        <div>
          <label>Equipamiento:</label>
          <input v-model="editExerciseData.equipment" />
        </div>
        <button type="submit">Actualizar</button>
        <button type="button" @click="cancelEdit">Cancelar</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ExerciseList',
  data() {
    return {
      exercises: [],
      showAddForm: false,
      showEditForm: false,
      newExercise: {
        name: '',
        category: '',
        muscle_group: '',
        difficulty: '',
        equipment: ''
      },
      editExerciseData: null
    }
  },
  methods: {
    async fetchExercises() {
      try {
        const response = await axios.get('http://localhost:8000/api/exercises/')
        this.exercises = response.data
      } catch (error) {
        console.error('Error fetching exercises:', error)
      }
    },
    async addExercise() {
      try {
        const response = await axios.post('http://localhost:8000/api/exercises/', this.newExercise)
        this.exercises.push(response.data)
        this.showAddForm = false
        this.resetNewExercise()
      } catch (error) {
        console.error('Error adding exercise:', error)
      }
    },
    editExercise(exercise) {
      this.editExerciseData = { ...exercise }
      this.showEditForm = true
    },
    async updateExercise() {
      try {
        const response = await axios.put(`http://localhost:8000/api/exercises/${this.editExerciseData.id}/`, this.editExerciseData)
        const index = this.exercises.findIndex(e => e.id === this.editExerciseData.id)
        if (index !== -1) {
          this.exercises.splice(index, 1, response.data)
        }
        this.showEditForm = false
        this.editExerciseData = null
      } catch (error) {
        console.error('Error updating exercise:', error)
      }
    },
    async deleteExercise(id) {
      try {
        await axios.delete(`http://localhost:8000/api/exercises/${id}/`)
        this.exercises = this.exercises.filter(e => e.id !== id)
      } catch (error) {
        console.error('Error deleting exercise:', error)
      }
    },
    cancelAdd() {
      this.showAddForm = false
      this.resetNewExercise()
    },
    cancelEdit() {
      this.showEditForm = false
      this.editExerciseData = null
    },
    resetNewExercise() {
      this.newExercise = {
        name: '',
        category: '',
        muscle_group: '',
        difficulty: '',
        equipment: ''
      }
    }
  },
  mounted() {
    this.fetchExercises()
  }
}
</script>

<style scoped>
.exercise-list {
  max-width: 600px;
  margin: 1rem auto;
}
.exercise-list ul {
  list-style: none;
  padding: 0;
}
.exercise-list li {
  margin: 0.5rem 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.exercise-list button {
  margin-left: 0.5rem;
}
form div {
  margin-bottom: 0.5rem;
}
</style>
