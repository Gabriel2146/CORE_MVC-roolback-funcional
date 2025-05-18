<template>
  <div>
    <h1>Panel de Administrador</h1>
    <LogoutButton />
    <p>Bienvenido, administrador. Aquí puedes gestionar la plataforma y el catálogo de ejercicios.</p>
  </div>
</template>

<script>
import LogoutButton from './LogoutButton.vue'

export default {
  name: 'Admin',
  components: {
    LogoutButton
  }
}
</script>

<style scoped>
h1 {
  color: #2c3e50;
}
</style>
