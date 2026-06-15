import http from "./http";
import type { HomeData } from "../types/api";

export function getHomeData()
{
  return http.get<HomeData>("/home/")
}