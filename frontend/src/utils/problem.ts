import type { ProblemListItem } from "../types/api";
export function getDifficultyText(difficulty: ProblemListItem['difficulty'])
{
  const map: Record<ProblemListItem['difficulty'], string> =
  {
    easy: '简单',
    medium: '中等',
    hard: '困难',
  }
  return map[difficulty]
}

export function getDifficultyClass(difficulty: ProblemListItem['difficulty'])
{
  const map: Record<ProblemListItem['difficulty'], string> =
  {
    easy: 'difficulty-easy',
    medium: 'difficulty-medium',
    hard: 'difficulty-hard',
  }
  return map[difficulty]
}