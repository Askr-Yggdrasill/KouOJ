<script setup lang="ts">
  import { onMounted, onUnmounted, ref } from 'vue'
  import { RouterLink, useRoute } from 'vue-router'
  import { getProblem } from '../api/problems'
  import { createSubmission, getSubmission } from '../api/submission'
  import type { ProblemDetail, Submission } from '../types/api'
  import { getStatusClass, getStatusText } from '../utils/status'
  import { getDifficultyClass, getDifficultyText } from '../utils/problem'

  const route = useRoute();
  const problem = ref<ProblemDetail | null>(null)
  const loading = ref(false)
  const errorMessage = ref('')

  const code = ref('')
  const submitting = ref(false)
  const submission = ref<Submission|null>(null)
  const submitError = ref('')
  let pollingTimer: number|null = null
  // 清除轮询
  function clearPolling()
  {
    if (pollingTimer)
    {
      window.clearInterval(pollingTimer)
      pollingTimer = null
    }
  }
  // 获取问题
  async function loadProblem() 
  {
    loading.value = true;
    errorMessage.value = ''

    try
    {
      const response = await getProblem(route.params.id as string)
      problem.value = response.data
    }
    catch(error)
    {
      errorMessage.value = '加载失败'
    }
    finally
    {
      loading.value = false
    }
  }

  // 轮询函数
  async function pollSubmission(id: number)
  {
    clearPolling()
    async function fetchSubmission()
    {
      const response = await getSubmission(id)
      submission.value = response.data
      if (!['PENDING', 'JUDGING'].includes(response.data.status))
      {
        clearPolling()
      }
    }
    await fetchSubmission()
    pollingTimer = window.setInterval(()=>
    {
      fetchSubmission()
    }, 1000)
  }

  // 提交函数
  async function handleSubmit()
  {
    if (!problem.value)
    {
      return ;
    }
    submitting.value = true
    submitError.value = ''
    submission.value = null

    try
    {
      const response = await createSubmission(
        {
          problem: problem.value.id,
          language: 'python3',
          code: code.value,
        }
      )
      await pollSubmission(response.data.id)
    }
    catch(error)
    {
      submitError.value = '提交失败'
    }
    finally
    {
      submitting.value = false
    }
  }

  onMounted(()=>
  {
    loadProblem()
  })

  onUnmounted(()=>
  {
    clearPolling()
  })
</script>
<template>
  <main>
    <p v-if="loading">加载中...</p>
    <p v-else-if="errorMessage"> {{ errorMessage }}</p> 
    <article v-else-if="problem">
      <h1>{{ problem.id }} {{ problem.title }}</h1>
      <p>
        难度：
        <span :class="getDifficultyClass(problem.difficulty)">
          {{ getDifficultyText(problem.difficulty) }}
        </span>
        时间限制：{{ problem.time_limit }} ms
        内存限制：{{ problem.memory_limit }} MB
      </p>

      <router-link :to="`/submissions?problem=${problem.id}`">
        提交记录
      </router-link>

      <section>
        <h2>Tags:</h2>
        <span v-for="tag in problem.tags">
          {{ tag.name }}
        </span>
      </section>
      <section>
        <h2>题目描述</h2>
        <p>{{ problem.description }}</p>
      </section>
      <section>
        <h2>输入描述</h2>
        <p>{{ problem.input_description }}</p>
      </section>
      <section>
        <h2>输出描述</h2>
        <p>{{ problem.output_description }}</p>
      </section>
      <section>
        <h2>样例</h2>
        <div v-if="problem.sample_cases.length===0">
          暂无样例
        </div>
        <div v-for="sample in problem.sample_cases" :key="sample.id">
          <p>输入</p>
          <pre>{{ sample.input_data }}</pre>
          <p>输出</p>
          <pre>{{ sample.output_data }}</pre>
        </div>
      </section>
      <section>
        <h2>提交代码</h2>
        <textarea v-model="code" rows="10" style="width: 100%; font-family: monospace;"></textarea>
        <div>
          <button type="button" :disabled="submitting" @click="handleSubmit">
            {{ submitting?'提交中...':'提交' }}
          </button>
        </div>
        <p v-if="submitError">{{ submitError }}</p>
        
          <div v-if="submission">
            <h3>判题结果</h3>
            <p>状态：
              <span :class="getStatusClass(submission.status)">
                {{ getStatusText(submission.status) }}
              </span>
            </p>
            <p>得分：{{ submission.score }}</p>
            <p>耗时：{{ submission.time_used }} ms</p>
            <p v-if="submission.error_message">
              错误信息：{{ submission.error_message }}
            </p>
        
            <div v-if="submission.results.length > 0">
              <h4>测试点结果</h4>
              <ul>
                <li v-for="result in submission.results" :key="result.id">
                  #{{ result.testcase }} - 
                  <span :class="getStatusClass(submission.status)">
                    {{ getStatusText(submission.status) }}
                  </span>
                   - {{ result.time_used }} ms
                </li>
              </ul>
            </div>
          </div>
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
</style>