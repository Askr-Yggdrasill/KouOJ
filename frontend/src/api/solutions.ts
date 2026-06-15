import http from "./http";
import type { CreateSolutionRequest, PaginatedResponse, Solution } from "../types/api";

// GET接口
export function getProblemSolution(problemId: number| string)
{
  return http.get<PaginatedResponse<Solution>>
  (
    `/problems/${problemId}/solutions/`,
  )
}

// POST接口
export function createProblemSolution(problemId: number|string, data:CreateSolutionRequest,)
{
  return http.post<Solution>
  (
    `/problems/${problemId}/solutions/`,data,
  )
}

// UPDATE接口
export function updateSolution(solutionId: number, data:CreateSolutionRequest,)
{
  return http.patch<Solution>(`/solutions/${solutionId}`,data)
}

// DELETE接口
export function deleteSolution(solutionId: number)
{
  http.delete(`/solutions/${solutionId}/`)
}
