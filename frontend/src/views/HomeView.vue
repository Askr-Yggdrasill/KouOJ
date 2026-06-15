<script setup lang="ts">
  import { onMounted, ref } from 'vue';
  import { RouterLink } from 'vue-router';
  import { getHomeData } from '../api/home';
  import type { HomeData } from '../types/api';
  import { getDifficultyClass, getDifficultyText } from '../utils/problem';

  const homeData = ref<HomeData|null>(null)
  const loading = ref(false)
  const errorMessage = ref('')
  async function loadHomeData()
  {
    loading.value = true
    errorMessage.value = ''
    try 
    {
      const response = await getHomeData()
      homeData.value = response.data

    }
    catch (error) 
    {
      errorMessage.value = "首页加载失败"
    }
    finally 
    {
      loading.value = false;
    }
  }

  onMounted(()=>
  {
    loadHomeData()
  })

</script>

<template>
  <main>
    <p v-if="loading">加载中...</p>
    <p v-else-if="errorMessage">{{ errorMessage }}</p>

    <div v-else-if="homeData">
      <section>
        <h1>KouOJ</h1>
      </section>

      <section>
        <h2>每日一题</h2>
        <div v-if="homeData.daily_problem">
          <router-link :to="`/problems/${homeData.daily_problem.id}`" >
            {{ homeData.daily_problem.title }}
          </router-link>
          <span :class="getDifficultyClass(homeData.daily_problem.difficulty)">
            {{ getDifficultyText(homeData.daily_problem.difficulty) }}
          </span>
        </div>

        <p v-else>暂无题目</p>
      </section>
      <section>
        <h2>未解决题目</h2>
        <ul v-if="homeData.unfinished_problems.length>0">
          <li v-for="problem in homeData.unfinished_problems" :key="problem.id">
            <router-link :to="`/problems/${problem.id}`" >
              {{ problem.title }}
            </router-link>
            <span :class="getDifficultyClass(problem.difficulty)">
              {{ getDifficultyText(problem.difficulty) }}
            </span>
          </li>
        </ul>
        <p v-else>你已完成所有题目</p>
      </section>
      <section>
        <h2>公告</h2>
        <ul v-if="homeData.announcements.length>0">
          <li v-for="announcement in homeData.announcements">
            <strong v-if="announcement.is_pinned">[置顶]</strong>
            <strong>{{ announcement.title }}</strong>
            <p>{{ announcement.content }}</p>
          </li>
        </ul>
        <p v-else>暂无公告</p>
      </section>
    </div>
  </main>
</template>