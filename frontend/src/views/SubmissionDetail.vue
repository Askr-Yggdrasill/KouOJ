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
  // 提交详情代码高亮
  import { computed } from 'vue'
  import CodeMirror from 'vue-codemirror6'
  import { python } from '@codemirror/lang-python'
  import { cpp } from '@codemirror/lang-cpp'
  import { oneDark } from '@codemirror/theme-one-dark'
  
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

  // 根据代码显示高亮
  const codeExtensions = computed(() =>
  {
    if (submission.value?.language === 'python3')
    {
      return [python(), oneDark]
    }

    return [cpp(), oneDark]
  })
  onMounted(()=>
  {
    loadSubmission()
  })
</script>
  
<template>
  <main class="submission-detail-page">
    <p v-if="loading">加载中...</p>
    <p v-else-if="errorMessage">{{ errorMessage }}</p>

    <template v-else-if="submission">
      <section class="submission-hero">
        <div>
          <p class="eyebrow">Submission</p>
          <h1>提交 #{{ submission.id }}</h1>

          <p>
            <RouterLink :to="`/problems/${submission.problem}`">
              {{ submission.problem_title || submission.problem }}
            </RouterLink>
            · {{ submission.language }}
            · {{ submission.score }} 分
          </p>
        </div>

        <span class="status-pill" :class="getStatusClass(submission.status)">
          {{ getStatusText(submission.status) }}
        </span>
      </section>

      <section class="submission-main">
        <div class="info-panel">
          <h2>提交信息</h2>

          <dl>
            <div>
              <dt>提交用户</dt>
              <dd>{{ submission.username }}</dd>
            </div>

            <div>
              <dt>题目</dt>
              <dd>
                <RouterLink :to="`/problems/${submission.problem}`">
                  {{ submission.problem_title || submission.problem }}
                </RouterLink>
              </dd>
            </div>

            <div>
              <dt>语言</dt>
              <dd>{{ submission.language }}</dd>
            </div>

            <div>
              <dt>得分</dt>
              <dd>{{ submission.score }}</dd>
            </div>

            <div>
              <dt>耗时</dt>
              <dd>{{ submission.time_used }} ms</dd>
            </div>

            <div>
              <dt>内存</dt>
              <dd>{{ submission.memory_used }} KB</dd>
            </div>

            <div>
              <dt>提交时间</dt>
              <dd>{{ submission.created_at }}</dd>
            </div>

            <div>
              <dt>判题时间</dt>
              <dd>{{ submission.judged_at || '-' }}</dd>
            </div>
          </dl>
        </div>

        <div class="code-panel">
          <h2>提交代码</h2>
          <CodeMirror v-model="submission.code" class="readonly-editor" :extensions="codeExtensions" :readonly="true" :disabled="true"/>
        </div>
      </section>

      <section>
        <h2>测试点结果</h2>

        <p v-if="submission.results.length === 0">暂无测试点结果</p>

        <table v-else>
          <thead>
            <tr>
              <th>测试点</th>
              <th>状态</th>
              <th>耗时</th>
              <th>内存</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="result in submission.results" :key="result.id">
              <td>#{{ result.testcase }}</td>
              <td>
                <span class="status-pill" :class="getStatusClass(result.status)">
                  {{ getStatusText(result.status) }}
                </span>
              </td>
              <td>{{ result.time_used }} ms</td>
              <td>{{ result.memory_used }} KB</td>
            </tr>
          </tbody>
        </table>
      </section>
    </template>
  </main>
</template>
<style scoped>
.submission-detail-page {
  display: grid;
  gap: 20px;
}

.submission-hero {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
}

.eyebrow {
  margin: 0 0 6px;
  color: var(--primary);
  font-weight: 600;
}

.submission-main {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 20px;
}

.info-panel,
.code-panel {
  min-width: 0;
}

dl {
  display: grid;
  gap: 12px;
  margin: 0;
}

dl div {
  display: grid;
  gap: 4px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border);
}

dt {
  color: var(--text-muted);
  font-size: 14px;
}

dd {
  margin: 0;
  color: var(--text);
  font-weight: 600;
}

.code-panel pre {
  min-height: 420px;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 4px 10px;
  background: var(--surface-muted);
  border: 1px solid var(--border);
  font-size: 14px;
  white-space: nowrap;
}

.mini-pre {
  max-width: 260px;
  max-height: 120px;
  overflow: auto;
  font-size: 13px;
}

.status-pd,
.status-jg {
  color: #b42335;
}

.status-ac {
  color: #16a34a;
  font-weight: 600;
}

.status-wa,
.status-se,
.status-ce {
  color: #dc2626;
  font-weight: 600;
}

.status-re {
  color: #7c3aed;
  font-weight: 600;
}

.status-tle {
  color: #d97706;
  font-weight: 600;
}

.readonly-editor {
  min-height: 420px;
  border: 1px solid #71313b;
  border-radius: var(--radius);
  overflow: hidden;
}

.readonly-editor :deep(.cm-editor) {
  height: 420px;
  font-size: 14px;
}

.readonly-editor :deep(.cm-scroller) {
  font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
}

@media (max-width: 900px) {
  .submission-hero {
    flex-direction: column;
  }

  .submission-main {
    grid-template-columns: 1fr;
  }

  table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }
}
</style>
