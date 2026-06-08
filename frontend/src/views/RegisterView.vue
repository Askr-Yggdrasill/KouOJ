<script setup lang="ts">
  import { ref } from 'vue';
  import { RouterLink, useRouter } from 'vue-router';
  import { register } from '../api/auth';
  
  const router = useRouter()
  const username = ref('')
  const email = ref('')
  const password = ref('')
  const loading = ref(false)
  const errorMessage = ref('')
  // 处理注册逻辑
  async function handleRegister()
  {
    loading.value = true;
    errorMessage.value = ''

    try
    {
      //调用注册API
      await register(
        {
          username: username.value,
          email: email.value,
          password: password.value,
        }
      )
      // 跳转到登录页
      router.push('/login')
    }
    catch(error)
    {
      errorMessage.value = '注册失败'
    }
    finally
    {
      loading.value = false
    }
  }
</script>

<template>
  <main>
    <h1>注册</h1>
    <form @submit.prevent="handleRegister">
      <div>
        <label>用户名</label>
        <input v-model="username">
      </div>
      <div>
        <label>邮箱</label>
        <input type="email" v-model="email">
      </div>
      <div>
        <label>密码</label>
        <input type="password" v-model="password">
      </div>

      <p v-if="errorMessage">{{ errorMessage }}</p>
      <button type="submit" :disabled="loading">{{ loading?'注册中...':'注册' }}</button>
    </form>
    <p>
      已有账号?
      <router-link to="/login">去登录</router-link>
    </p>
  </main>
</template>