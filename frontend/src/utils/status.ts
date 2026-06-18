import type { SubmissionStatus } from "../types/api";

export function getStatusText(status: SubmissionStatus)
{
  const map: Record<SubmissionStatus, string> =
  {
    PENDING: 'Pending',
    JUDGING: 'Judging',
    ACCEPTED: 'Accepted',
    WRONG_ANSWER: 'Wrong Answer',
    TIME_LIMIT_EXCEEDED: 'Time Limit Exceeded',
    RUNTIME_ERROR: 'Runtime Error',
    SYSTEM_ERROR: 'System Error',
    COMPILE_ERROR: 'Compile Error',
  }
  return map[status]
}

export function getStatusClass(status: SubmissionStatus)
{
  const map: Record<SubmissionStatus, string> =
  {
    PENDING: 'status-pd',
    JUDGING: 'status-jg',
    ACCEPTED: 'status-ac',
    WRONG_ANSWER: 'status-wa',
    TIME_LIMIT_EXCEEDED: 'status-tle',
    RUNTIME_ERROR: 'status-re',
    SYSTEM_ERROR: 'status-se',
    COMPILE_ERROR: 'status-ce',
  }
  return map[status]
}
