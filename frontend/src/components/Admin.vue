<template>
  <div>
    <h1>Panel de Administrador</h1>
    <LogoutButton />
    <p>Bienvenido, administrador. Aquí puedes gestionar la plataforma y el catálogo de ejercicios.</p>
    <ExerciseList />
  </div>
</template>

<script>
import LogoutButton from './LogoutButton.vue'
import ExerciseList from './ExerciseList.vue'

export default {
  name: 'Admin',
  components: {
    LogoutButton,
    ExerciseList
  }
}
</script>

<style scoped>
h1 {
  color: #2c3e50;
}
</style>
