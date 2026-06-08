import http from "./http";
import type { LoginRequest, LoginResponse, User } from "../types/api";
import type { RegisterRequest, RegisterResponse } from "../types/api";
// 请求登录用
export function login(data: LoginRequest)
{
  return http.post<LoginResponse>('/auth/login/', data)
}
// 获取用户信息用
export function getMe()
{
  return http.get<User>('/auth/me/')
}
// 请求注册用
export function register(data: RegisterRequest)
{
  return http.post<RegisterResponse>('/auth/register/', data)
}