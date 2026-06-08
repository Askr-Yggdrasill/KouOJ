<script setup lang="ts">
  import { onMounted, ref } from 'vue';
  import { RouterLink, useRouter, useRoute } from 'vue-router';
  import { getProblems, getTags } from '../api/problems';
  import type { ProblemListItem, Tag } from '../types/api';
  import { getDifficultyClass, getDifficultyText } from '../utils/problem';

  const problems = ref<ProblemListItem[]>([])
  const loading = ref(false)
  const errorMessage = ref('')
  // 搜索与筛选相关
  const search = ref('')
  const difficulty = ref<'easy'|'medium'|'hard'|''>('')
  const tags = ref<Tag[]>([])
  const selectedTag = ref<number|''>('')
  const router = useRouter()
  const route = useRoute()

  // 分页相关
  const currentPage = ref(1)
  const totalCount = ref(0)
  const hasNext = ref(false)
  const hasPrevious = ref(false)

  // 创建query
  function syncQuery(page:number)
  {
    router.replace(
      {
        path: '/problems',
        query: 
        {
          page: String(page),
          search: search.value||undefined,
          tags: selectedTag.value||undefined,
          difficulty: difficulty.value||undefined,
        },
      
      }
    )

  }
  async function loadProblems(page = currentPage.value){
    loading.value = true;
    errorMessage.value = ''

    syncQuery(page)
    try{
      const response = await getProblems(
        {
          search: search.value || undefined,
          difficulty: difficulty.value || undefined,
          tags: selectedTag.value || undefined,
          page,
        }
      )
      problems.value = response.data.results
      // 分页相关
      totalCount.value = response.data.count
      hasNext.value = Boolean(response.data.next)
      hasPrevious.value = Boolean(response.data.previous)
      currentPage.value = page
    }
    catch(error)
    {
      errorMessage.value = '题目列表加载失败'
    } 
    finally
    {
      loading.value = false
    }
  }

  async function loadTags()
  {
    const response = await getTags()
    tags.value = response.data.results
  }

  // 跳转到上一页
  function goPreviousPage()
  {
    if (hasPrevious.value&&currentPage.value>1)
    {
      loadProblems(currentPage.value-1)
    }
  }

  // 跳转到下一页
  function goNextPage()
  {
    if (hasNext.value)
    {
      loadProblems(currentPage.value+1)
    }
  }

  onMounted(()=>{
    const searchQuery = route.query.search
    const tagsQuery = route.query.tags
    const difficultyQuery = route.query.difficulty
    const pageQuery = route.query.page
    if (typeof searchQuery==='string')
    {
      search.value = searchQuery
    }
    if (typeof difficultyQuery==='string')
    {
      if (difficultyQuery==='easy'||difficultyQuery==='medium'||difficultyQuery==='hard')
      {
        difficulty.value = difficultyQuery
      }
    }
    if (typeof tagsQuery==='string')
    {
      selectedTag.value = Number(tagsQuery)
    }
    const page = typeof pageQuery==='string'?Number(pageQuery):1
    loadProblems(Number.isNaN(page)?1:page)
    loadTags()
  })
</script>
<template>
  <main>
    <h1>ProblemList</h1>
    <!-- 搜索+筛选 -->
    <form @submit.prevent="loadProblems(1)">
      <input v-model="search" placeholder="搜索...">
      <select v-model="difficulty">
        <option value="">全部难度</option>
        <option value="easy">简单</option>
        <option value="medium">中等</option>
        <option value="hard">困难</option>
      </select>

      <select v-model="selectedTag">
        <option value="">全部标签</option>
        <option value=""></option>
      </select>

      <button type="submit">搜索</button>
      <button type="button" @click="search=''; difficulty=''; loadProblems(1)">重置</button>
    </form>
    <p v-if="loading">加载中...</p>
    <p v-else-if="errorMessage">{{errorMessage}}</p>

    <ul v-else>
      <li v-for="problem in problems" :key="problem.id">
        <router-link :to="`/problems/${problem.id}`">
          {{problem.id}}. {{ problem.title }}
        </router-link>
        <span :class="getDifficultyClass(problem.difficulty)">
          {{ getDifficultyText(problem.difficulty) }}
        </span>
      </li>
    </ul>

    <div class="pagination">
      <button type="button" :disabled="!hasPrevious" @click="goPreviousPage">
        上一页
      </button>
      <span>第{{ currentPage }}页</span>
      <span>共{{ totalCount }}页</span>
      <button type="button" :disabled="!hasNext" @click="goNextPage">
        下一页
      </button>
    </div>
  </main>
</template>

<style scoped>
  ul
  {
    padding-left: 0;
  }
  li
  {
    list-style: none;
    padding: 10px, 0;
    border-bottom: 1px solid #eee;
  }
  a
  {
    margin-right: 12px;
  }
  .difficulty-easy 
  {
    color: #2e7d32;
    margin-right: 8px;
  }

  .difficulty-medium 
  {
    color: #ef6c00;
    margin-right: 8px;
  }

  .difficulty-hard 
  {
    color: #c62828;
    margin-right: 8px;
  }

  .pagination 
  {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 16px;
  }

  .pagination button:disabled
  {
    cursor: not-allowed;
    opacity: 0,5;
  }

</style>