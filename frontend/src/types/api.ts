export interface Tag
{
  id: number
  name: string
}

export interface SampleCase
{
  id: number
  input_data: string
  output_data: string
  order: number
}

export interface ProblemListItem
{
  id: number
  title: string
  difficulty: 'easy'|'medium'|'hard'
  time_limit: number
  memory_limit: number
  tags: Tag[]
}


export interface ProblemDetail extends ProblemListItem
{
  description: string
  input_description: string
  output_description: string
  is_public: boolean
  sample_cases: SampleCase[]
  created_at: string
  updated_at: string
}

export interface PaginatedResponse<T>
{
  count: number
  next: string|null
  previous: string|null
  results: T[]
}

export interface User
{
  id: number
  username: string
  email: string
  role: 'user'|'admin'
  solved_count: number
  submit_count: number
}

export interface LoginRequest
{
  username: string
  password: string
}

export interface LoginResponse
{
  access: string
  refresh: string
}

export type SubmissionStatus = |'PENDING'|'JUDGING'|'ACCEPTED'|'WRONG_ANSWER'|'TIME_LIMIT_EXCEEDED'|'RUNTIME_ERROR'|'SYSTEM_ERROR'
export interface CreateSubmissionRequest
{
  problem: number
  language: 'python3'
  code: string
}

export interface CreateSubmissionResponse
{
  id: number
  problem: number
  language: 'python3'
  code: string
}

export interface JudgeResult
{
  id: number
  testcase: number
  status: SubmissionStatus
  time_used: number
  memory_used: number
  output:string
  error_message: string
}

export interface Submission
{
  id: number
  username: string
  problem: number
  problem_title: string
  language: 'python3'
  code: string
  status: SubmissionStatus
  score: number
  time_used: number
  memory_used: number
  error_message: string
  results: JudgeResult[]
  created_at: string
  judged_at: string|null
}
// 注册模块请求
export interface RegisterRequest
{
  username: string
  email: string
  password: string
}
// 注册模块响应
export interface RegisterResponse
{
  id: number
  username: string
  email: string
}