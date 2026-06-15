
<script setup lang="ts">
  import { onMounted } from 'vue';
  import { RouterLink, RouterView, useRouter } from 'vue-router';
  import { useAuthStore } from './stores/auth';
  
  // 获取pinia的登陆状态仓库
  const authStore = useAuthStore() 
  // 拿到路由控制器，用于后面主动跳转页面
  const router = useRouter()

  // 控制登出
  function handleLogout()
  {
    authStore.logout()
    router.push('/login')
  }

  /**
   * 页面刷新后恢复用户信息
   * 刷新以后pinia中的user会丢掉，所以要从localStorage中拿取token
   * 当App启动时，如果发现有token，就请求GET api/auth/me
   */
  onMounted(()=>
  {
    if (authStore.isLoggedIn && !authStore.user)
    {
      authStore.loadMe().catch(()=>{authStore.logout()})
    }
  })

</script>

<!-- 导航栏 -->
<template>
  <div>
    <header>
      <nav>
        <div class="logo"><router-link to="/">KouOJ</router-link></div>
        <router-link to="/problems">题目</router-link>
        <router-link to="/submissions">提交记录</router-link>
        <span v-if="authStore.user">
          <router-link to='/profile'>{{ authStore.user.nickname || authStore.user.username }}</router-link>
        </span>

        <button v-if="authStore.isLoggedIn" type="button" @click="handleLogout">
          登出
        </button>
        <div v-else>
          <router-link to="/login">登录 </router-link>
          <router-link to="/register">注册</router-link>
        </div>
      </nav>
    </header>
  </div>
  <router-view />
</template>

<!-- 导航栏样式 -->
<style scoped>
header
{
  border-bottom: 1px solid #ddd;
  padding: 12px 16px;
}
nav
{
  display: flex;
  align-items: center;
  gap: 16px;
}
a
{
  color: #333;
  text-decoration: none;
}
a.router-link-active
{
  color: #409eff;
  font-weight: 600;
}
button
{
  cursor: pointer;
}

</style>
