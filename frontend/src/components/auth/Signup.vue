<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const emit = defineEmits(['submit']) // компонент отдаёт payload наружу

const router = useRouter()

const email = ref('')
const password = ref('')
const password2 = ref('')
const username = ref('') // optional
const displayName = ref('') // optional

const touched = ref({
  email: false,
  password: false,
  password2: false,
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

  if (!password2.value) e.password2 = 'Подтвердите пароль'
  else if (password.value !== password2.value) e.password2 = 'Пароли не совпадают'

  return e
})

const isValid = computed(() => Object.keys(errors.value).length === 0)

function onSubmit(e) {
  e.preventDefault()
  // помечаем поля как touched чтобы показать ошибки
  mark('email'); mark('password'); mark('password2')

  if (!isValid.value) return

  const payload = {
    email: email.value.trim(),
    password: password.value,
    username: username.value.trim() || null,
    displayName: displayName.value.trim() || null,
  }

  // emit payload -> outer code может выполнить запрос (или сделай fetch тут)
  emit('submit', payload)

  // временно — просто редирект на логин (можешь убрать)
  // router.push('/auth/login')
}
</script>

<template>
  <div class="signup-page">
    <form class="card" @submit="onSubmit" novalidate>
      <h1 class="form-title">Регистрация</h1>

      <label class="field">
        <span>Электронная почта *</span>
        <input
          v-model="email"
          @blur="mark('email')"
          type="email"
          autocomplete="email"
          required
        />
        <small v-if="touched.email && errors.email" class="err">{{ errors.email }}</small>
      </label>

      <label class="field">
        <span>Пароль *</span>
        <input
          v-model="password"
          @blur="mark('password')"
          type="password"
          autocomplete="new-password"
          required
        />
        <small v-if="touched.password && errors.password" class="err">{{ errors.password }}</small>
      </label>

      <label class="field">
        <span>Повторите пароль *</span>
        <input
          v-model="password2"
          @blur="mark('password2')"
          type="password"
          autocomplete="new-password"
          required
        />
        <small v-if="touched.password2 && errors.password2" class="err">{{ errors.password2 }}</small>
      </label>

      <label class="field">
        <span>Имя пользователя (опционально)</span>
        <input v-model="username" type="text" autocomplete="username" />
      </label>

      <label class="field">
        <span>Отоброжаемое имя (опционально)</span>
        <input v-model="displayName" type="text" />
      </label>

      <div class="row">
        <button class="btn" :disabled="!isValid" type="submit">Создать аккаунт</button>
      </div>
    </form>
  </div>
</template>

