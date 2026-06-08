<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useRouter, useRoute, RouterLink } from 'vue-router';
  import { getSubmissions } from '../api/submission';
  import type { Submission, SubmissionStatus } from '../types/api';
  import { getStatusClass, getStatusText } from '../utils/status';

  const submissions = ref<Submission[]> ([]);
  const loading = ref(false)
  const errorMessage = ref('')
  
  // 查看某个题目的提交
  const selectedProblem = ref<number|undefined>(undefined)
  // 筛选用
  const selectedStatus = ref<SubmissionStatus|''>('')
  const route = useRoute()
  const router = useRouter()
  // 分页
  const currentPage = ref(1)
  const totalCount = ref(0)
  const hasNext = ref(false)
  const hasPrevious = ref(false)

  // 封装更新url的函数
  function syncQuery(page: number)
  {
    router.replace(
    {
      path:'/submissions',
      query:
      {
        page: String(page),
        problem: selectedProblem.value?String(selectedProblem.value):undefined,
        status: selectedStatus.value||undefined,
      },
    })
  }
  async function loadSubmissions(page = currentPage.value)
  {
    loading.value = true;
    errorMessage.value = ''

    syncQuery(page)

    try
    {
      const response = await getSubmissions({
        page,
        status: selectedStatus.value||undefined,
        problem: selectedProblem.value,
      })
      submissions.value = response.data.results
      totalCount.value = response.data.count
      hasNext.value = Boolean(response.data.next)
      hasPrevious.value = Boolean(response.data.previous)
      currentPage.value = page
    }
    catch(error)
    {
      errorMessage.value = ("提交记录页出现问题")
    }
    finally
    {
      loading.value = false;
    }
  }

  // 跳转到上一页
  function goPreviousPage()
  {
    if (hasPrevious.value&& currentPage.value>1)
    {
      loadSubmissions(currentPage.value-1)
    }
  }

  // 跳转到下一页
  function goNextPage()
  {
    if (hasNext.value)
    {
      loadSubmissions(currentPage.value+1);
    }
  }
  onMounted(()=>
  {
    // 添加查询参数
    const problemQuery = route.query.problem
    const statusQuery = route.query.status
    const pageQuery = route.query.page
    if (typeof problemQuery==='string')
    {
      selectedProblem.value = Number(problemQuery)
    }
    if (typeof statusQuery==='string')
    {
      selectedStatus.value = statusQuery as SubmissionStatus
    }
    const page = typeof pageQuery ==='string'?Number(pageQuery):1
    loadSubmissions(Number.isNaN(page)?1:page)
  })
</script>
<template>
  <main>
    <h1>提交记录</h1>
    <!-- 筛选提交记录 -->
    <form @submit.prevent="loadSubmissions(1)">
      <select v-model="selectedStatus" @change="loadSubmissions(1)">
        <option value="">全部状态</option>
        <option value="PENDING">Pending</option>
        <option value="JUDGING">Judging</option>
        <option value="ACCEPTED">Accepted</option>
        <option value="WRONG_ANSWER">Wrong Anwser</option>
        <option value="TIME_LIMIT_EXCEEDED">Time Limit Exceeded</option>
        <option value="RUNTIME_ERROR">Runtime Error</option>
        <option value="SYSTEM_ERROR">System</option>
      </select>
      <button type="button" @click="selectedStatus='';selectedProblem=undefined;loadSubmissions(1)">
        重置
      </button>
        
    </form>

    <p v-if="loading">加载中...</p>
    <p v-else-if="errorMessage">{{ errorMessage }}</p>
    <table v-else border="1" cellpadding="8">
      <thead>
        <tr>
          <th>ID</th>
          <th>题目</th>
          <th>语言</th>
          <th>状态</th>
          <th>得分</th>
          <th>耗时</th>
          <th>消耗内存</th>
          <th>提交时间</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="submission in submissions" :key="submission.id">
          <td>
            <router-link :to="`/submissions/${submission.id}`">
              # {{ submission.id }}
            </router-link>
          </td>
          <td>
            <router-link :to="`/problems/${submission.problem}`">
              {{ submission.problem }}
            </router-link>
          </td>
          <td>{{ submission.language }}</td>
          <td>
            <span :class="getStatusClass(submission.status)">
              {{ getStatusText(submission.status) }}
            </span>
          </td>
          <td>{{ submission.score }}</td>
          <td>{{ submission.time_used }}</td>
          <td>{{ submission.memory_used }}</td>
          <td>{{ submission.created_at }}</td>
        </tr>
      </tbody>

      
    </table>
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
.status-pd,
.status-jg 
{
  color: #409eff;
}

.status-ac 
{
  color: #2e7d32;
  font-weight: 600;
}

.status-wa,
.status-se 
{
  color: #c62828;
  font-weight: 600;
}

.status-re
{
  color: #8A2BE2;
  font-weight: 600;
}

.status-tle 
{
  color: #ef6c00;
  font-weight: 600;
}
.pagination {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 16px;
}

.pagination button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>