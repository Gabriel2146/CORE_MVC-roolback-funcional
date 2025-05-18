<template>
  <div>
    <h2>Panel de Invitado</h2>
    <LogoutButton />
    <!-- contenido del panel -->
  </div>
</template>

<script>
import LogoutButton from './LogoutButton.vue'

export default {
  components: {
    LogoutButton
  }
}
</script>

<style scoped>
h2 {
  color: #7f8c8d;
}
</style>
