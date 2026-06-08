import http from './http'
import type { PaginatedResponse, ProblemDetail, ProblemListItem, Tag } from '../types/api'

export function getProblems(params?: ProblemQuery){
  return http.get<PaginatedResponse<ProblemListItem>> ('/problems/', {params,})
}

export function getProblem(id: string|number){
  return http.get<ProblemDetail> (`/problems/${id}/`)
}

export function getTags()
{
  return http.get<PaginatedResponse<Tag>>('/tags/')
}

export interface ProblemQuery
{
  search?: string
  difficulty?: 'easy'|'medium'|'hard'|''
  tags?: number|''
  page?: number
}