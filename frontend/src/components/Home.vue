<template>
  <div>
    <h1>Bienvenido a la Plataforma de Entrenamiento</h1>
    <button @click="logout">Cerrar Sesión</button>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'Home',
  setup() {
    const router = useRouter()

    const logout = () => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_role')
      router.push('/login')
    }

    return { logout }
  }
}
</script>

<style scoped>
button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #c0392b;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #e74c3c;
}
</style>
