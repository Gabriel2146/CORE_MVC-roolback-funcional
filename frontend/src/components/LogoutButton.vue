<template>
  <button @click="logout" class="logout-button">Cerrar Sesión</button>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'LogoutButton',
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
.logout-button {
  margin-top: 1rem;
  padding: 0.4rem 1rem;
  background-color: #3498db;
  color: white;
  border: 1px solid #2980b9;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
}
.logout-button:hover {
  background-color: #2980b9;
}
</style>
