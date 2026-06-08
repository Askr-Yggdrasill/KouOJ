<script setup lang="ts">
  import { ref } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
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
  <main>
    <h1>登录</h1>
    <form @submit.prevent=""handleLogin>
      <div>
        <label>用户名</label>
        <input v-model="username">
      </div>

      <div>
        <label>密码</label>
        <input type="password" v-model="password">
      </div>

      <p v-if="errorMessage">{{ errorMessage }}</p>
      
      <button type="submit" :disabled="loading" v-on:click="handleLogin()">
        {{ loading?'登录中...': '登录' }}
      </button>
    </form>
    <p>
      没有账号?
      <router-link to="/register">去注册</router-link>
    </p>
  </main>
</template>
