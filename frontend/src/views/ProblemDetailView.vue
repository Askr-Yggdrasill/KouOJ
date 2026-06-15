<script setup lang="ts">
  import { onMounted, onUnmounted, ref } from 'vue'
  import { RouterLink, useRoute } from 'vue-router'
  import { getProblem } from '../api/problems'
  import { createSubmission, getSubmission } from '../api/submission'
  import { createProblemSolution, getProblemSolution, deleteSolution, updateSolution } from '../api/solutions'
  import type { ProblemDetail, Submission, Language, Solution } from '../types/api'
  import { getStatusClass, getStatusText } from '../utils/status'
  import { getDifficultyClass, getDifficultyText } from '../utils/problem'
  import { useAuthStore } from '../stores/auth'

  const route = useRoute();
  const problem = ref<ProblemDetail | null>(null)
  const loading = ref(false)
  const errorMessage = ref('')
  const submitLanguage = ref<Language>('cpp')
  // 提交部分
  const code = ref('')
  const submitting = ref(false)
  const submission = ref<Submission|null>(null)
  const submitError = ref('')
  // 题解部分
  const solutions = ref<Solution[]>([])
  const solutionLoading = ref(false)
  const solutionError = ref('')
  const solutionTitle = ref('')
  const solutionContent = ref('')
  const solutionLanguage = ref('')
  const solutionSubmitting = ref(false)
  const authStore = useAuthStore() // 判断登录
  const editingSolutionId = ref<number|null>(null)
  const editTitle = ref('')
  const editContent = ref('')
  const editLanguage = ref('')

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
      await loadSolutions()
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
          language: submitLanguage.value,
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
  // 加载题解列表
  async function loadSolutions()
  {
    if (!problem.value) return 
    solutionLoading.value = true
    solutionError.value = ''
    try
    {
      const response = await getProblemSolution(problem.value.id)
      solutions.value = response.data.results
    }
    catch(error)
    {
      solutionError.value = '题解加载失败'
    }
    finally
    {
      solutionLoading.value = false
    }
  }

  // 递交题解
  async function handleCreateSolution()
  {
    if (!problem.value) return
    solutionSubmitting.value = true
    solutionError.value = ''
    
    if (!solutionTitle.value.trim())
    {
      solutionError.value = '请输入题解标题'
      return
    }
    if (!solutionContent.value.trim())
    {
      solutionError.value = '请输入题解内容'
      return 
    }

    solutionSubmitting.value = true
    solutionError.value = ''
    try
    {
      await createProblemSolution(problem.value.id, 
      {
        title: solutionTitle.value,
        content: solutionContent.value,
        language:solutionLanguage.value,
        is_public:true,
      })
      solutionTitle.value = ''
      solutionContent.value = ''
      solutionLanguage.value = ''

      await loadSolutions()
    }
    catch(error)
    {
      solutionError.value = '题解发布失败'
    }
    finally
    {
      solutionSubmitting.value = false
    }
  }
  
  // 删除题解
  async function handleDeleteSolution(solutionId: number)
  {
    const confirmed = window.confirm('确定删除吗?')
    if (!confirmed) return 
    try
    {
      await deleteSolution(solutionId)
      solutions.value = solutions.value.filter(
        (solution) => solution.id !==solutionId,
      )
    }
    catch (error)
    {
      solutionError.value = '删除题解失败'
    }
  }

  // 编辑题解
  function startEditSolution(solution: Solution)
  {
    editingSolutionId.value = solution.id
    editTitle.value = solution.title
    editContent.value = solution.content
    editLanguage.value = solution.language
    solutionError.value = ''
  }
  
  function cancelEditSolution()
  {
    editingSolutionId.value = null
    editTitle.value = ''
    editContent.value = ''
    editLanguage.value = ''
  }

  async function handleUpdateSolution(solutionId: number)
  {
    if (!editTitle.value.trim())
    {
      solutionError.value = '请输入题解标题'
      return
    }
    if (!editContent.value.trim())
    {
      solutionError.value = '请输入题解内容'
      return 
    }
    try
    {
      const response = await updateSolution(solutionId,
      {
        title: editTitle.value.trim(),
        content: editContent.value.trim(),
        language: editLanguage.value.trim(),
        is_public: true,
      })
      solutions.value = solutions.value.map((solution)=>
        solution.id === solutionId?response.data:solution,
      )
      cancelEditSolution()
    }
    catch(error)
    {

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
        <select v-model="submitLanguage">
          <option value="python3">Python3</option>
          <option value="c">C</option>
          <option value="cpp">C++</option>
        </select>
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
      <section>
        <h2>题解</h2>
        <div v-if="authStore.user">
          <form @submit.prevent="handleCreateSolution">
            <div>
              <input v-model="solutionTitle" type="text" placeholder="题解标题"/>
            </div>

            <div>
              <select v-model="solutionLanguage">
                <option value="">不限定语言</option>
                <option value="python3">Python3</option>
                <option value="c">C</option>
                <option value="cpp">C++</option>
              </select>
            </div>

            <div>
              <textarea v-model="solutionContent" rows="6" 
              style="width: 100%; font-family: monospace;"></textarea>
            </div>

            <button type="submit" :disabled="solutionSubmitting">
              {{ solutionSubmitting ? '发布中...' : '发布题解' }}
            </button>
          </form>
        </div>
        <p v-else>
          登陆后才可以发布题解
          <router-link to="/login">去登陆</router-link>
        </p>
        

        <p v-if="solutionError">{{ solutionError }}</p>
        <p v-if="solutionLoading">题解加载中...</p>

        <div v-else>
         <article v-for="solution in solutions" :key="solution.id">
            <div v-if="editingSolutionId === solution.id">
              <input v-model="editTitle" type="text" />

              <select v-model="editLanguage">
                <option value="">不限定语言</option>
                <option value="python3">Python3</option>
                <option value="c">C</option>
                <option value="cpp">C++</option>
              </select>

              <textarea v-model="editContent" rows="6" style="width: 100%; font-family: monospace;"></textarea>

              <button type="button" @click="handleUpdateSolution(solution.id)">
                保存
              </button>

              <button type="button" @click="cancelEditSolution">
                取消
              </button>
            </div>

            <div v-else>
              <h3>{{ solution.title }}</h3>

              <div v-if="authStore.user && authStore.user.id === solution.author">
                <button type="button" @click="startEditSolution(solution)">
                  编辑
                </button>

                <button type="button" @click="handleDeleteSolution(solution.id)">
                  删除
                </button>
              </div>

              <p>
                作者：{{ solution.author_username }}
                <span v-if="solution.language">
                  语言：{{ solution.language }}
                </span>
                <span>
                  发布时间：{{ solution.created_at }}
                </span>
              </p>

              <pre>{{ solution.content }}</pre>
            </div>
          </article>

          <p v-if="solutions.length === 0">暂无题解</p>
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