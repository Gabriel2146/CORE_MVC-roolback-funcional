<template>
  <div class="register-container">
    <h2>Registro de Usuario</h2>
    <form @submit.prevent="register">
      <div>
        <label for="username">Usuario:</label>
        <input id="username" v-model="username" required />
      </div>
      <div>
        <label for="email">Correo Electrónico:</label>
        <input id="email" type="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Contraseña:</label>
        <input id="password" type="password" v-model="password" required />
      </div>
      <div>
        <label for="password2">Confirmar Contraseña:</label>
        <input id="password2" type="password" v-model="password2" required />
      </div>
      <div>
        <label for="role">Rol:</label>
        <select id="role" v-model="role" required>
          <option value="guest">Invitado</option>
          <option value="athlete">Deportista</option>
          <option value="trainer">Entrenador</option>
        </select>
      </div>
      <button type="submit">Registrar</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>
  </div>
</template>

<script>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const username = ref('')
    const email = ref('')
    const password = ref('')
    const password2 = ref('')
    const role = ref('guest')
    const error = ref('')
    const success = ref('')

    const register = async () => {
      error.value = ''
      success.value = ''
      if (password.value !== password2.value) {
        error.value = 'Las contraseñas no coinciden.'
        return
      }
      try {
        await axios.post('http://localhost:8000/api/users/register/', {
          username: username.value,
          email: email.value,
          password: password.value,
          password2: password2.value,
          role: role.value
        })
        success.value = 'Registro exitoso. Redirigiendo a inicio de sesión...'
        setTimeout(() => {
          router.push('/login')
        }, 2000)
      } catch (err) {
        if (err.response && err.response.data) {
          error.value = JSON.stringify(err.response.data)
        } else {
          error.value = 'Error en el registro.'
        }
      }
    }

    return {
      username,
      email,
      password,
      password2,
      role,
      error,
      success,
      register
    }
  }
}
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.error {
  color: red;
  margin-top: 1rem;
}
.success {
  color: green;
  margin-top: 1rem;
}
</style>
