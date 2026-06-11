import http from "./http";
import type { LoginRequest, LoginResponse, User, UserStats } from "../types/api";
import type { RegisterRequest, RegisterResponse, UpdateProfileRequest, ChangePasswordRequest, MessageResponse } from "../types/api";

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

// 获取用户统计信息
export function getMeStats()
{
  return http.get<UserStats>('/auth/me/stats/')
}

// 编辑用户信息
export function updateProfile(data: UpdateProfileRequest)
{
  return http.patch<User>('/auth/me/', data)
}

// 修改密码
export function ChangePassword(data: ChangePasswordRequest)
{
  return http.post<MessageResponse>('/auth/change-password/', data)
}