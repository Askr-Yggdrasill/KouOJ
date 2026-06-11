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

    <div v-else-if="user && stats">
      <section class="profile-card">
        <img :src="user.avatar_url||defaultAvatar" alt="avatar" class="avatar">
        <div>
          <h2>{{ user.nickname|| user.username }}</h2>
          <p>@{{ user.username }}</p>
          <p>{{ user.email }}</p>
          <p>{{ user.bio||'' }}</p>
        </div>

        <button type="button" @click="editing=!editing">{{ editing?'取消编辑':'编辑资料' }}</button>
        <button type="button" @click="passwordEditing=!passwordEditing">{{ passwordEditing?'取消修改':'修改密码' }}</button>

        <h2>刷题统计</h2>
        <div class="stats-grid">
          <div>
            <strong>{{ stats.submit_count }}</strong>
            <p>总提交</p>
          </div>

          <div>
            <strong>{{ stats.accepted_count }}</strong>
            <p>AC次数</p>
          </div>
          <div>
            <strong>{{ stats.solved_count }}</strong>
            <p>通过题目</p>
          </div>
          <div>
              <strong>{{ stats.difficulty.easy }}</strong>
              <p>简单</p>
          </div>
          <div>
              <strong>{{ stats.difficulty.medium }}</strong>
              <p>中等</p>
          </div>
          <div>
              <strong>{{ stats.difficulty.hard }}</strong>
              <p>困难</p>
          </div>
        </div>
      </section>
      <section class="heatmap-section">
        <div class="heatmap">
          <div v-for="item in heatmapCells" :key="item.date" :class="['heatmap-cell', getHeatmapClass(item.count)]" :title="`${item.date}: ${item.count} AC`"></div>
        </div>
      </section>

      <section v-if="editing">
        <h2>编辑资料</h2>
        <form @submit.prevent="handleSaveProfile">
          <div>
            <label>昵称</label>
            <input v-model="profileForm.nickname" maxlength="20"> 
          </div>
          <div>
            <label>邮箱</label>
            <input v-model="profileForm.email" type="email">
          </div>
          <div>
            <label>头像(输入url)</label>
            <input v-model="profileForm.avatar_url"> 
          </div>
        
          <div>
            <label>个人简介</label>
            <input v-model="profileForm.bio" maxlength="200" rows="4">
          </div>

          <button type="submit" :disabled="saving">
            {{ saving?'保存中...':'保存' }}
          </button>
        </form>
      </section>
      <p v-if="saveMessage">{{ saveMessage }}</p>
      <section v-if="passwordEditing">
        <h2>修改密码</h2>
        <form @submit.prevent="handleChangePassword">
          <div>
            <label>旧密码</label>
            <input v-model="passwordForm.old_password" type="password">
          </div>
          <div>
            <label>新密码</label>
            <input v-model="passwordForm.new_password" type="password">
          </div>
         <button type="submit" :disabled="changingPassword">
            {{ changingPassword ? '修改中' : "修改密码" }}
          </button>
        </form>
       
        <p v-if="changingPassword">{{ passwordMessage }}</p>

      </section>
    </div>
  
  </main>
</template>

<style scoped>
img.avatar {
  width: 144px;
  height: 144px;
  border-radius: 50%;
  object-fit: cover;
}
.heatmap-section {
  margin-top: 24px;
  text-align: center;
}

.heatmap {
  display: grid;
  grid-template-columns: repeat(30, 14px);
  gap: 4px;
  justify-content: center;
  margin: 12px auto 0;
}

.heatmap-cell {
  width: 14px;
  height: 14px;
  border-radius: 2px;
  border: 1px solid #e5e7eb;
}

.heatmap-empty {
  background: #f3f4f6;
}

.heatmap-low {
  background: #b7eb8f;
}

.heatmap-medium {
  background: #52c41a;
}

.heatmap-high {
  background: #237804;
}
</style>