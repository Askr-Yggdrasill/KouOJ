<script setup lang="ts">
  import { computed, onMounted, ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { getMe,getMeStats, updateProfile, ChangePassword  } from '../api/auth';
  import type { User, UserStats } from '../types/api';
  import { useAuthStore } from '../stores/auth';
  import defaultAvatar from '../assets/default_avatar.png'

  const user = ref<User|null>(null)
  const stats = ref<UserStats|null>(null)
  const loading = ref(false)
  const errorMessage = ref('')
  // 编辑表单状态
  const editing = ref(false)
  const saving = ref(false)
  const saveMessage = ref('')
  const authStore = useAuthStore()
  // 修改密码
  const changingPassword = ref(false)
  const passwordMessage = ref('')
  const passwordEditing = ref(false)
  const router = useRouter()
  const passwordForm = ref(

  {
    old_password: '',
    new_password: '',
  }
  )
  const profileForm = ref(
    {
      email: '',
      nickname: '',
      avatar_url: '',
      bio: '',
    }
  )
  async function loadProfile()
  {
    loading.value = true
    errorMessage.value = ''

    try
    {
      const [userResponse, statsResponse] = await Promise.all(
        [
          getMe(),
          getMeStats(),
        ]
      )
      user.value = userResponse.data
      stats.value = statsResponse.data
      fillProfileForm()

    }
    catch (error)
    {
      errorMessage.value = '个人信息加载失败'
    }
    finally
    {
      loading.value = false
    }
  }

  // 用于填充表单
  function fillProfileForm()
  {
    if (!user.value)
    {
      return
    }
    profileForm.value =
    {
      email: user.value.email,
      nickname: user.value.nickname,
      avatar_url: user.value.avatar_url,
      bio: user.value.bio,
    }
  }
  
  // 保存更新的信息
  async function handleSaveProfile()
  {
    saving.value = true
    saveMessage.value = ''
    try
    {
      const response = await updateProfile(profileForm.value)
      user.value = response.data
      authStore.user = response.data
      fillProfileForm()
      editing.value = true
      saveMessage.value = "个人资料已更新"
      editing.value = false
    }
    catch(error)
    {
      saveMessage.value = "保存失败"
    }
    finally
    {
      saving.value = false
    }
  }

  // 提交密码修改
  async function handleChangePassword()
  {
    changingPassword.value = true
    passwordMessage.value = ''
    try
    {
      const response = await ChangePassword(passwordForm.value)
      passwordEditing.value = true
      passwordMessage.value = response.data.detail
      passwordForm.value = 
      {
        old_password: '',
        new_password: '',
      }
      //  注册后重新登录
      authStore.logout()
      router.push('/login')
      passwordEditing.value = false
    }
    catch(error)
    {
      passwordMessage.value = '密码修改失败'
    }
    finally
    {
      changingPassword.value = false
    }
  }

  // 格式化日期
  function formatDate(date: Date)
  {
    const year = date.getFullYear()
    const month = String(date.getMonth()+1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2,'0')
    return `${year}-${month}-${day}`
  }

  // 生成热力图
  const heatmapCells = computed(()=>
  {
    const countMap = new Map(stats.value?.heatmap.map((item)=>[item.date.slice(0,10), item.count])?? [],)
    const days = 90
    const cells = []
    const today = new Date()
    for (let i = days-1;i>=0;i--)
    {
      const date = new Date(today)
      date.setDate(today.getDate()-i)

      const dateText = formatDate(date)
      cells.push(
        {
          date:dateText,
          count:countMap.get(dateText)??0,
        }
      )
    }
    return cells 
  })

  // 热力图颜色函数
  function getHeatmapClass(count: number)
  {
    if (count===0) return 'heatmap-empty'
    if (count===1) return 'heatmap-low'
    if (count<=3) return 'heatmap-medium'
    return 'heatmap-high'
  }
  onMounted(()=>
  {
    loadProfile()
  })
</script>

<template>
  <main>
    <h1>个人中心</h1>
    <p v-if="loading">加载中...</p>
    <p v-else-if="errorMessage">{{ errorMessage }}</p>

  <div v-else-if="user && stats" class="profile-page">
      <!-- 用户资料 -->
      <section class="profile-header">
        <div class="profile-identity">
          <img :src="user.avatar_url || defaultAvatar" alt="用户头像" class="avatar" />

          <div class="profile-info">
            <h1>{{ user.nickname || user.username }}</h1>
            <p class="username">@{{ user.username }}</p>
            <p>{{ user.email }}</p>
            <p class="bio">{{ user.bio || '这个人还没有填写个人简介。' }}</p>
          </div>
        </div>

        <div class="profile-actions">
         <button type="button" @click="editing = true">
            编辑资料
          </button>

          <button type="button" @click="passwordEditing = true">
            修改密码
          </button>
        </div>
      </section>

      <!-- 刷题统计 -->
      <section>
        <div class="section-header">
          <div>
            <p class="eyebrow">个人数据统计</p>
            <h2>刷题统计</h2>
          </div>
        </div>

        <div class="stats-grid">
          <div class="stat-item">
            <strong>{{ stats.submit_count }}</strong>
            <span>总提交</span>
          </div>

          <div class="stat-item">
            <strong>{{ stats.accepted_count }}</strong>
            <span>AC 次数</span>
          </div>

          <div class="stat-item">
            <strong>{{ stats.solved_count }}</strong>
            <span>通过题目</span>
          </div>

          <div class="stat-item easy">
            <strong>{{ stats.difficulty.easy }}</strong>
            <span>简单</span>
          </div>

          <div class="stat-item medium">
            <strong>{{ stats.difficulty.medium }}</strong>
            <span>中等</span>
          </div>

          <div class="stat-item hard">
            <strong>{{ stats.difficulty.hard }}</strong>
            <span>困难</span>
          </div>
        </div>
      </section>

      <!-- 热力图 -->
      <section class="heatmap-section">
        <div class="section-header">
          <div>
            <p class="eyebrow">热力图</p>
            <h2>最近刷题情况</h2>
          </div>
        </div>

        <div class="heatmap-scroll">
          <div class="heatmap">
            <div v-for="item in heatmapCells" :key="item.date" :class="['heatmap-cell', getHeatmapClass(item.count)]"
              :title="`${item.date}: ${item.count} AC`"></div>
          </div>
        </div>
      </section>

    <div v-if="editing" class="modal-overlay" @click.self="editing = false">
        <section class="modal-dialog">
          <div class="modal-header">
            <h2>编辑资料</h2>

            <button class="close-button" type="button" aria-label="关闭" @click="editing = false">
              ×
            </button>
          </div>

          <form class="settings-form" @submit.prevent="handleSaveProfile">
            <label>
              <span>昵称</span>
              <input v-model="profileForm.nickname" maxlength="20" />
            </label>

            <label>
              <span>邮箱</span>
              <input v-model="profileForm.email" type="email" />
            </label>

            <label>
              <span>头像 URL</span>
              <input v-model="profileForm.avatar_url" type="url" />
            </label>

            <label>
              <span>个人简介</span>
              <textarea v-model="profileForm.bio" maxlength="200" rows="4"></textarea>
            </label>

            <p v-if="saveMessage">{{ saveMessage }}</p>

            <div class="modal-actions">
              <button type="button" @click="editing = false">
                取消
              </button>

              <button class="primary-button" type="submit" :disabled="saving">
                {{ saving ? '保存中...' : '保存资料' }}
              </button>
            </div>
          </form>
        </section>
      </div>
     <div v-if="passwordEditing" class="modal-overlay" @click.self="passwordEditing = false">
        <section class="modal-dialog modal-dialog-small">
          <div class="modal-header">
            <h2>修改密码</h2>

            <button class="close-button" type="button" aria-label="关闭" @click="passwordEditing = false">
              ×
            </button>
          </div>

          <form class="settings-form" @submit.prevent="handleChangePassword">
            <label>
              <span>旧密码</span>
              <input v-model="passwordForm.old_password" type="password" autocomplete="current-password" />
            </label>

            <label>
              <span>新密码</span>
              <input v-model="passwordForm.new_password" type="password" autocomplete="new-password" />
            </label>

            <p v-if="passwordMessage">{{ passwordMessage }}</p>

            <div class="modal-actions">
              <button type="button" @click="passwordEditing = false">
                取消
              </button>

              <button class="primary-button" type="submit" :disabled="changingPassword">
                {{ changingPassword ? '修改中...' : '修改密码' }}
              </button>
            </div>
          </form>
        </section>
      </div>
    </div>
  </main>
</template>

<style scoped>
.profile-page
{
  display: grid;
  gap: 20px;
}

.profile-header
{
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
}

.profile-identity
{
  display: flex;
  align-items: center;
  gap: 20px;
  min-width: 0;
}

.avatar
{
  width: 112px;
  height: 112px;
  border: 3px solid var(--surface);
  border-radius: 50%;
  object-fit: cover;
  box-shadow: var(--shadow);
}

.profile-info h1
{
  margin: 0 0 6px;
}

.username
{
  color: var(--primary);
}

.bio
{
  max-width: 600px;
  line-height: 1.7;
}

.profile-actions
{
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.eyebrow
{
  margin: 0 0 4px;
  color: var(--primary);
  font-size: 13px;
  font-weight: 600;
}

.section-header
{
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 16px;
  margin-bottom: 18px;
}

.stats-grid
{
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 12px;
}

.stat-item
{
  display: grid;
  gap: 6px;
  padding: 16px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface-muted);
}

.stat-item strong
{
  color: var(--text);
  font-size: 28px;
}

.stat-item span
{
  color: var(--text-muted);
  font-size: 14px;
}

.stat-item.easy strong
{
  color: var(--success);
}

.stat-item.medium strong
{
  color: var(--warning);
}

.stat-item.hard strong
{
  color: var(--danger);
}

.heatmap-scroll
{
  overflow-x: auto;
  padding-bottom: 6px;
}

.heatmap
{
  display: grid;
  grid-template-columns: repeat(30, 24px);
  gap: 4px;
  width: max-content;
  margin: 0 auto;
}

.heatmap-cell
{
  width: 24px;
  height: 24px;
  border: 1px solid var(--border);
  border-radius: 2px;
}

.heatmap-empty
{
  background: #f3f4f6;
}

.heatmap-low
{
  background: #bbf7d0;
  border-color: #86efac;
}

.heatmap-medium
{
  background: #4ade80;
  border-color: #22c55e;
}

.heatmap-high
{
  background: #15803d;
  border-color: #166534;
}
.settings-form
{
  display: grid;
  gap: 16px;
  max-width: 680px;
}

.settings-form label
{
  display: grid;
  gap: 6px;
}

.settings-form label span
{
  font-size: 14px;
  font-weight: 600;
}

.primary-button
{
  justify-self: start;
  background: var(--primary);
  border-color: var(--primary);
  color: white;
}

.modal-overlay
{
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: grid;
  place-items: center;
  padding: 20px;
  background: rgba(15, 23, 42, 0.55);
}

.modal-dialog
{
  width: min(620px, 100%);
  max-height: calc(100vh - 40px);
  overflow-y: auto;
  padding: 24px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: var(--shadow);
}

.modal-dialog-small
{
  width: min(460px, 100%);
}

.modal-header
{
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.modal-header h2
{
  margin: 0;
}

.close-button
{
  width: 36px;
  height: 36px;
  padding: 0;
  font-size: 24px;
  line-height: 1;
}

.modal-actions
{
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
}
@media (max-width: 640px)
{
  .profile-header,
  .profile-identity,
  .section-header
  {
    align-items: flex-start;
    flex-direction: column;
  }

  .stats-grid
  {
    grid-template-columns: repeat(2, 1fr);
  }

  .profile-actions,
  .profile-actions button
  {
    width: 100%;
  }
}
</style>