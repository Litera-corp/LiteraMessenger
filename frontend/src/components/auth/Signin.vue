<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const emit = defineEmits(['submit']) // компонент отдаёт payload наружу

const router = useRouter()

const email = ref('')
const password = ref('')
const password_confirm = ref('')

const touched = ref({
  email: false,
  password: false,
  password_confirm: false,
})

function mark(name) {
  touched.value[name] = true
}

const errors = computed(() => {
  const e = {}
  if (!email.value) e.email = 'Обязательное поле'
  else if (!/^\S+@\S+\.\S+$/.test(email.value)) e.email = 'Неверный email'

  if (!password.value) e.password = 'Обязательное поле'
  else if (password.value.length < 6) e.password = 'Минимум 6 символов'

  if (!password.value) e.password_confirm = 'Подтвердите пароль'
  else if (password.value !== password_confirm.value) e.password_confirm = 'Пароли не совпадают'

  return e
})

const isValid = computed(() => Object.keys(errors.value).length === 0)

function onSubmit(e) {
  e.preventDefault()
  mark('email'); mark('password'); mark('password_confirm')

  if (!isValid.value) return

  const payload = {
    email: email.value.trim(),
    password: password.value,
  }

}
</script>

<template>
  <div class="signup-page">
    <form class="card" novalidate @submit="onSubmit">
      <h1 class="form-title">Авторизация</h1>

      <label class="field">
        <span>Электронная почта *</span>
        <input
          v-model="email"
          type="email"
          autocomplete="email"
          required
          @blur="mark('email')"
        />
        <small v-if="touched.email && errors.email" class="err">{{ errors.email }}</small>
      </label>

      <label class="field">
        <span>Пароль *</span>
        <input
          v-model="password"
          type="password"
          autocomplete="new-password"
          required
          @blur="mark('password')"
        />
        <small v-if="touched.password && errors.password" class="err">{{ errors.password }}</small>
      </label>

      <label class="field">
        <span>Повторите пароль *</span>
        <input
          v-model="password_confirm"
          type="password"
          autocomplete="new-password"
          required
          @blur="mark('password_confirm')"
          
        />
        <small v-if="touched.password_confirm && errors.password_confirm" class="err">{{ errors.password_confirm }}</small>
      </label>

      <div class="row">
        <button class="btn" :disabled="!isValid" type="submit">Авторизоваться</button>
      </div>
      <a class="switch-link" @click.prevent="router.push('/auth/signup')">Уже есть аккаунт?</a>
    </form>
  </div>
</template>

<style lang="scss">
.switch-link {
  margin-top: 10px;
  display: block;
}
</style>

