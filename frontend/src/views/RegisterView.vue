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
  <main class="auth-page">
    <section class="auth-panel">
      <div class="auth-header">
        <RouterLink class="auth-brand" to="/">KouOJ</RouterLink>
        <h1>创建账号</h1>
        <p>又骗进来一个</p>
      </div>

      <form class="auth-form" @submit.prevent="handleRegister">
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
          <span>邮箱</span>
          <input
            v-model="email"
            type="email"
            autocomplete="email"
            placeholder="请输入邮箱"
            required
          />
        </label>

        <label>
          <span>密码</span>
          <input
            v-model="password"
            type="password"
            autocomplete="new-password"
            placeholder="至少 6 个字符"
            minlength="6"
            required
          />
        </label>

        <p v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </p>

        <button class="primary-button submit-button" type="submit" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>

      <p class="auth-switch">
        已有账号？
        <RouterLink to="/login">返回登录</RouterLink>
      </p>
    </section>
  </main>
</template>