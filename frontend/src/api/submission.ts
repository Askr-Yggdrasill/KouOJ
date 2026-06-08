import http from "./http";
import type { CreateSubmissionRequest, CreateSubmissionResponse ,Submission, PaginatedResponse, SubmissionStatus } from "../types/api";

export function createSubmission(data:CreateSubmissionRequest)
{
  return http.post<CreateSubmissionResponse>('/submissions/', data)
}

// 得到单个提交
export function getSubmission(id: string|number)
{
  return http.get<Submission>(`/submissions/${id}/`)
}

// 得到提交列表
export function getSubmissions(params?: SubmissionQuery)
{
  return http.get<PaginatedResponse<Submission>>('/submissions/', 
    {params,})
}

// 用于分页与筛选
export interface SubmissionQuery
{
  page?: number
  status?: SubmissionStatus|''
  problem?: number
}