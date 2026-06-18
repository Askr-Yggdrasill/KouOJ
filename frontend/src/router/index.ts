import { createRouter, createWebHistory } from "vue-router";

import LoginView from "../views/LoginView.vue";
import ProblemListView from "../views/ProblemListView.vue";
import ProblemDetailView from "../views/ProblemDetailView.vue";
import SubmissionListView from "../views/SubmissionListView.vue";
import SubmissionDetail from "../views/SubmissionDetail.vue";
import RegisterView from "../views/RegisterView.vue";
import ProfileView from "../views/ProfileView.vue";
import HomeView from "../views/HomeView.vue";
import ProblemSolutionsView from "../views/ProblemSolutionsView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta:
      {
        guestOnly: true,
      }
    },
    {
      path: '/problems',
      name: 'problem_list',
      component: ProblemListView,
    },
    {
      path: '/problems/:id',
      name: 'problem-detail',
      component: ProblemDetailView,
    },
    {
      path: '/problems/:id/solutions',
      name: 'problem-solutions',
      component: ProblemSolutionsView,
    },
    {
      path: '/submissions',
      name: 'submission_list',
      component: SubmissionListView,
      meta: 
      {
        requiresAuth: true,
      },
    },
    {
      path: '/submissions/:id',
      name: 'submission_detail',
      component: SubmissionDetail,
      meta:
      {
        requiresAuth: true,
      },
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta:
      {
        guestOnly: true,
      },
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta:
      {
        requiresAuth: true
      },
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
    }
  ],
})
router.beforeEach((to)=>
{
  const token = localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !token)
  {
    return {
      path:'/login',
      query:
      {
        redirect: to.fullPath,
      },
    }
  }
  if (to.meta.guestOnly && token)
  {
    return '/problems'
  }
  return true
})
export default router
