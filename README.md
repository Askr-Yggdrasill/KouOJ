# KouOJ

KouOJ 是一个基于 Django + Vue3 的简化版 Online Judge 系统，支持用户注册登录、题目列表、题目详情、代码提交、自动判题和提交记录查看。

## 技术栈

- 后端：Python, Django, Django REST Framework
- 数据库：MySQL
- 前端：Vue3, TypeScript, Vite
- 认证：JWT
- 判题：Python subprocess

## 功能

- 用户注册、登录、退出
- JWT 鉴权
- 题目列表、题目详情
- 题目搜索、难度筛选、标签筛选、分页
- Django Admin 写题和维护测试点
- Python3 代码提交
- Judge Worker 自动判题
- 支持 AC、WA、RE、TLE 等状态
- 提交记录和提交详情

## 项目结构

```text
backend/
  config/
  apps/
    accounts/
    problems/
    submissions/
    judge/

frontend/
  src/
    api/
    router/
    stores/
    views/
    utils/
    types/
```
## 后端启动
1. 创建虚拟环境

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
2. 安装依赖
```powershell
pip install -r requirements.txt
```
3. 配置环境变量
复制 .env.example 为 .env，并填写自己的数据库密码：
```text
KOUOJ_DB_PASSWORD=你的MySQL密码
```
4. 创建 MySQL 数据库
```sql
CREATE DATABASE kouoj DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
5. 数据库迁移
```powershell
cd backend
python manage.py makemigrations
python manage.py migrate
```
6. 创建管理员
```powershell
python manage.py createsuperuser
```
7. 启动后端
```powershell
python manage.py runserver
```
后台地址：`http://127.0.0.1:8000/admin/`
启动判题 Worker
另开一个终端：
```powershell
cd backend
python manage.py run_judge
```

只执行一次判题任务：
```powershell
python manage.py run_judge --once
```
前端启动
```powershell
cd frontend
npm install
npm run dev
```
前端地址：`http://localhost:5173/`

## 常用 API
```text
POST /api/auth/register/
POST /api/auth/login/
GET  /api/auth/me/

GET  /api/problems/
GET  /api/problems/{id}/

POST /api/submissions/
GET  /api/submissions/
GET  /api/submissions/{id}/

GET  /api/tags/
```
## 判题说明
当前版本使用 Python subprocess.run() 实现基础判题，支持 Python3 代码运行、标准输出比对和超时控制。

当前状态包括：
```
PENDING
JUDGING
ACCEPTED
WRONG_ANSWER
TIME_LIMIT_EXCEEDED
RUNTIME_ERROR
SYSTEM_ERROR
```
当前版本主要用于课程设计和学习演示，不建议直接部署到公网运行不可信代码。