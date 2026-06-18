<script setup lang="ts">
  import { ref } from 'vue'
  import { useRouter, useRoute, RouterLink } from 'vue-router'
  import { useAuthStore } from '../stores/auth'

  const router = useRouter()
  const route = useRoute()
  const authStore = useAuthStore()

  const username = ref('')
  const password = ref('')
  const loading = ref(false)
  const errorMessage = ref('')

  // 处理登录逻辑
  async function handleLogin() {
    loading.value = true
    errorMessage.value = ''

    try
    {
      await authStore.login(username.value, password.value)
      // 跳转到problems或原页面
      const redirect = route.query.redirect as string
      router.push(redirect||'/problems')
    }
    catch(error)
    {
      errorMessage.value = '用户名或密码错误'

    }
    finally
    {
      loading.value = false;
    }
  }

</script>
<template>
  <main class="auth-page">
    <section class="auth-panel">
      <div class="auth-header">
        <RouterLink class="auth-brand" to="/">KouOJ</RouterLink>
        <h1>欢迎回来</h1>
        <p>是先刷题, 先刷题, 还是先刷题?</p>
      </div>

      <form class="auth-form" @submit.prevent="handleLogin">
        <label>
          <span>用户名</span>
          <input
            v-model="username"
            type="text"
            autocomplete="username"
            placeholder="请输入用户名"
            required
          />
        </label>

        <label>
          <span>密码</span>
          <input
            v-model="password"
            type="password"
            autocomplete="current-password"
            placeholder="请输入密码"
            required
          />
        </label>

        <p v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </p>

        <button class="primary-button submit-button" type="submit" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>

      <p class="auth-switch">
        还没有账号？
        <RouterLink to="/register">立即注册</RouterLink>
      </p>
    </section>
  </main>
</template>
