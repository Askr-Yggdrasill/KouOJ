import http from './http'
import type { CreateSolutionRequest, PaginatedResponse, Solution } from '../types/api'

export function getProblemSolution(problemId: number | string) {
  return http.get<PaginatedResponse<Solution>>(`/problems/${problemId}/solutions/`)
}

export function createProblemSolution(
  problemId: number | string,
  data: CreateSolutionRequest,
) {
  return http.post<Solution>(`/problems/${problemId}/solutions/`, data)
}

export function updateSolution(solutionId: number, data: CreateSolutionRequest) {
  return http.patch<Solution>(`/solutions/${solutionId}/`, data)
}

export function deleteSolution(solutionId: number) {
  return http.delete(`/solutions/${solutionId}/`)
}
