<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  import { getSubmission } from '../api/submission';
  import type { Submission } from '../types/api';
  import { getStatusClass, getStatusText } from '../utils/status';
  const route = useRoute()
  const submission = ref<Submission|null>(null)
  const loading = ref(false)
  const errorMessage = ref('')
  
  async function loadSubmission() 
  {
    loading.value = true
    errorMessage.value = ''
    try
    {
      const response = await getSubmission(route.params.id as string)
      submission.value = response.data
    } 
    catch(error)
    {
      errorMessage.value = '提交详情加载错误'
    } 
    finally
    {
      loading.value = false
    }
  }
  onMounted(()=>
  {
    loadSubmission()
  })
</script>
  
<template>
  <main>
    <p v-if="loading">加载中...</p>
    <p v-else-if="errorMessage"> {{ errorMessage }}</p>
    <article v-else-if="submission">
      <h1>提交 #{{ submission.id }}</h1>

      <p>用户：{{ submission.username }}</p>
      <p>题目：{{ submission.problem_title }}</p>
      <p>语言：{{ submission.language }}</p>
      <p>
        状态：<span :class="getStatusClass(submission.status)">
          {{ getStatusText(submission.status) }}
        </span>
      </p>
      <p>得分：{{ submission.score }}</p>
      <p>耗时：{{ submission.time_used }}</p>
      <p>消耗内存：{{ submission.memory_used }}</p>
      <p>提交时间：{{ submission.created_at }}</p>
      <p>判题时间：{{ submission.judged_at }}</p>

      <section>
        <h2>测试点结果</h2>
        <p v-if="submission.results.length===0">
          暂无测试点信息
        </p>
        <table v-else border="1" cellpadding="8">
          <thead>
            <tr>
              <th>测试点</th>
              <th>状态</th>
              <th>耗时</th>
              <th>消耗内存</th>
              <th>输出</th>
              <th>错误信息</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="result in submission.results" :key="result.id">
              <td>{{ result.testcase }}</td>
              <td>{{ result.status }}</td>
              <td>{{ result.time_used }}</td>
              <td>{{ result.memory_used }}</td>
              <td>{{ result.output }}</td>
              <td>{{ result.error_message }}</td>
            </tr>
          </tbody>
        </table>
      </section>
    </article>
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
</style>