<script setup lang="ts">
  import { onMounted, ref } from 'vue'
  import { RouterLink, useRoute } from 'vue-router'
  import { getProblem } from '../api/problems'
  import {
    createProblemSolution,
    deleteSolution,
    getProblemSolution,
    updateSolution,
  } from '../api/solutions'
  import { useAuthStore } from '../stores/auth'
  import type { ProblemDetail, Solution } from '../types/api'
  import { getDifficultyClass, getDifficultyText } from '../utils/problem'
  import { formatDateTime } from '../utils/time'

  const route = useRoute()
  const authStore = useAuthStore()
  const problemId = route.params.id as string

  // 题目信息
  const problem = ref<ProblemDetail | null>(null)
  const loading = ref(false)
  const errorMessage = ref('')

  // 题解列表
  const solutions = ref<Solution[]>([])
  const solutionLoading = ref(false)
  const solutionError = ref('')

  // 发布题解表单
  const solutionTitle = ref('')
  const solutionContent = ref('')
  const solutionLanguage = ref('')
  const solutionSubmitting = ref(false)

  // 编辑题解表单
  const editingSolutionId = ref<number | null>(null)
  const editTitle = ref('')
  const editContent = ref('')
  const editLanguage = ref('')

  // 加载题目信息
  async function loadProblem()
  {
    try
    {
      const response = await getProblem(problemId)
      problem.value = response.data
    }
    catch (error)
    {
      errorMessage.value = '题目信息加载失败'
    }
  }

  // 加载题解列表
  async function loadSolutions()
  {
    solutionLoading.value = true
    solutionError.value = ''

    try
    {
      const response = await getProblemSolution(problemId)
      solutions.value = response.data.results
    }
    catch (error)
    {
      solutionError.value = '题解加载失败'
    }
    finally
    {
      solutionLoading.value = false
    }
  }

  // 加载整个题解页
  async function loadPage()
  {
    loading.value = true
    errorMessage.value = ''

    try
    {
      await Promise.all([loadProblem(), loadSolutions()])
    }
    finally
    {
      loading.value = false
    }
  }

  // 发布题解
  async function handleCreateSolution()
  {
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
      await createProblemSolution(
        problemId,
        {
          title: solutionTitle.value.trim(),
          content: solutionContent.value.trim(),
          language: solutionLanguage.value,
          is_public: true,
        }
      )

      solutionTitle.value = ''
      solutionContent.value = ''
      solutionLanguage.value = ''

      await loadSolutions()
    }
    catch (error)
    {
      solutionError.value = '题解发布失败，请确认已经登录'
    }
    finally
    {
      solutionSubmitting.value = false
    }
  }

  // 删除题解
  async function handleDeleteSolution(solutionId: number)
  {
    const confirmed = window.confirm('确定删除这篇题解吗？')

    if (!confirmed)
    {
      return
    }

    try
    {
      await deleteSolution(solutionId)
      solutions.value = solutions.value.filter((solution) => solution.id !== solutionId)
    }
    catch (error)
    {
      solutionError.value = '删除题解失败'
    }
  }

  // 开始编辑题解
  function startEditSolution(solution: Solution)
  {
    editingSolutionId.value = solution.id
    editTitle.value = solution.title
    editContent.value = solution.content
    editLanguage.value = solution.language
    solutionError.value = ''
  }

  // 取消编辑题解
  function cancelEditSolution()
  {
    editingSolutionId.value = null
    editTitle.value = ''
    editContent.value = ''
    editLanguage.value = ''
  }

  // 保存编辑后的题解
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
      const response = await updateSolution(
        solutionId,
        {
          title: editTitle.value.trim(),
          content: editContent.value.trim(),
          language: editLanguage.value,
          is_public: true,
        }
      )

      solutions.value = solutions.value.map((solution) =>
        solution.id === solutionId ? response.data : solution,
      )
      cancelEditSolution()
    }
    catch (error)
    {
      solutionError.value = '更新题解失败'
    }
  }

  onMounted(() =>
  {
    loadPage()
  })
</script>

<template>
  <main class="solutions-page">
    <p v-if="loading">加载中...</p>
    <p v-else-if="errorMessage">{{ errorMessage }}</p>

    <template v-else>
      <section class="solutions-hero">
        <div>
          <p class="eyebrow">题解</p>
          <h1 v-if="problem">#{{ problem.id }} {{ problem.title }}</h1>
          <h1 v-else>题解列表</h1>

          <div v-if="problem" class="problem-meta">
            <span :class="getDifficultyClass(problem.difficulty)">
              {{ getDifficultyText(problem.difficulty) }}
            </span>
            <span>{{ problem.time_limit }} ms</span>
            <span>{{ problem.memory_limit }} MB</span>
          </div>
        </div>

        <RouterLink class="secondary-button" :to="`/problems/${problemId}`">
          返回题目
        </RouterLink>
      </section>

      <section class="solution-panel">
        <h2>发布题解</h2>

        <form v-if="authStore.user" class="solution-form" @submit.prevent="handleCreateSolution">
          <div class="form-row">
            <input
              v-model="solutionTitle"
              class="title-input"
              type="text"
              placeholder="题解标题"
            />

            <select v-model="solutionLanguage">
              <option value="">通用思路</option>
              <option value="python3">Python3</option>
              <option value="c">C</option>
              <option value="cpp">C++</option>
            </select>
          </div>

          <textarea
            v-model="solutionContent"
            class="solution-editor"
            rows="8"
            placeholder="写下解题思路、算法步骤和复杂度分析..."
          ></textarea>

          <div class="form-footer">
            <span>{{ solutionContent.length }} 字符</span>

            <button
              class="primary-button"
              type="submit"
              :disabled="solutionSubmitting"
            >
              {{ solutionSubmitting ? '发布中...' : '发布题解' }}
            </button>
          </div>
        </form>

        <p v-else>
          登录后可以发布题解。
          <RouterLink to="/login">去登录</RouterLink>
        </p>

        <p v-if="solutionError" class="error-message">{{ solutionError }}</p>
      </section>

      <section>
        <h2>全部题解</h2>
        <p v-if="solutionLoading">题解加载中...</p>

        <div v-else class="solution-list">
          <article v-for="solution in solutions" :key="solution.id" class="solution-card">
            <!-- 编辑题解 -->
            <form v-if="editingSolutionId === solution.id" class="solution-form"
              @submit.prevent="handleUpdateSolution(solution.id)">
              <div class="form-row">
                <input v-model="editTitle" type="text" placeholder="题解标题" />

                <select v-model="editLanguage">
                  <option value="">通用思路</option>
                  <option value="python3">Python3</option>
                  <option value="c">C</option>
                  <option value="cpp">C++</option>
                </select>
              </div>

              <textarea v-model="editContent" class="solution-editor" rows="8"></textarea>

              <div class="form-footer">
                <span>{{ editContent.length }} 字符</span>

                <div class="solution-actions">
                  <button class="primary-button" type="submit">
                    保存
                  </button>

                  <button type="button" @click="cancelEditSolution">
                    取消
                  </button>
                </div>
              </div>
            </form>

            <!-- 普通展示状态 -->
            <div v-else>
              <div class="solution-card-header">
                <div class="solution-heading">
                  <h3>{{ solution.title }}</h3>

                  <div class="solution-meta">
                    <span class="author">{{ solution.author_username }}</span>

                    <span v-if="solution.language" class="language-tag">
                      {{ solution.language }}
                    </span>

                    <span>{{ formatDateTime(solution.created_at) }}</span>
                  </div>
                </div>

                <div v-if="authStore.user && authStore.user.id === solution.author" class="solution-actions">
                  <button type="button" @click="startEditSolution(solution)">
                    编辑
                  </button>

                  <button class="danger-button" type="button" @click="handleDeleteSolution(solution.id)">
                    删除
                  </button>
                </div>
              </div>

              <div class="solution-content">
                {{ solution.content }}
              </div>
            </div>
          </article>

          <p v-if="solutions.length === 0">暂无题解</p>
        </div>
      </section>
    </template>
  </main>
</template>

<style scoped>
.solutions-page {
  display: grid;
  gap: 20px;
  max-width: 1000px;
}

.solutions-hero
{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
}

.solutions-hero h1
{
  margin-bottom: 12px;
}

.solution-panel {
  margin-top: 0;
}

.form-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 160px;
  gap: 12px;
}

.solution-form input,
.solution-form select,
.solution-form textarea {
  width: 100%;
}

.title-input {
  font-weight: 600;
}

.solution-editor {
  min-height: 180px;
  line-height: 1.7;
  font-family: inherit;
}

.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.form-footer span {
  color: var(--text-muted);
  font-size: 13px;
}

.solution-list {
  display: grid;
  gap: 12px;
}

.solution-card {
  padding: 20px;
  background: var(--surface);
  transition:
    border-color 0.2s,
    box-shadow 0.2s;
}

.solution-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
}

.solution-card-header {
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border);
}

.solution-heading {
  min-width: 0;
}

.solution-heading h3 {
  margin: 0 0 8px;
  font-size: 18px;
}

.solution-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  color: var(--text-muted);
  font-size: 13px;
}

.author {
  color: var(--text);
  font-weight: 600;
}

.language-tag {
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 2px 8px;
  color: var(--primary);
  background: var(--surface-muted);
}

.solution-content {
  padding-top: 16px;
  color: var(--text);
  line-height: 1.8;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.danger-button {
  color: var(--danger);
}

.danger-button:hover {
  color: white;
  border-color: var(--danger);
  background: var(--danger);
}

.problem-meta
{
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.problem-meta span
{
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: var(--surface-muted);
  font-size: 14px;
}

.difficulty-easy
{
  color: #2e7d32;
}

.difficulty-medium
{
  color: #ef6c00;
}

.difficulty-hard
{
  color: #c62828;
}

.eyebrow
{
  margin: 0 0 6px;
  color: var(--primary);
  font-size: 13px;
  font-weight: 600;
}

.secondary-button
{
  display: inline-flex;
  align-items: center;
  padding: 8px 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  white-space: nowrap;
}

.primary-button
{
  background: var(--primary);
  border-color: var(--primary);
  color: white;
}

.primary-button:hover
{
  background: var(--primary-hover);
  border-color: var(--primary-hover);
  color: white;
}

.solution-form
{
  display: grid;
  gap: 12px;
}

.solution-card
{
  padding: 20px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
}

.solution-card-header
{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border);
}

.solution-actions
{
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.error-message
{
  margin-top: 12px;
  color: var(--danger);
}
@media (max-width: 720px)
{
  .solutions-hero,
  .solution-card-header
  {
    flex-direction: column;
  }

  .secondary-button
  {
    width: 100%;
    justify-content: center;
  }

  .form-row
  {
    grid-template-columns: 1fr;
  }

  .form-footer
  {
    align-items: stretch;
    flex-direction: column;
  }

  .form-footer .primary-button
  {
    width: 100%;
  }
}
</style>
