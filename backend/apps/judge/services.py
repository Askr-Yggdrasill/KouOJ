import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.submissions.models import JudgeResult, Submission

@dataclass
class RunResult:
    '''统一格式'''
    status: str
    output: str = ""
    error_message: str = ""
    time_used: int = 0


def normalize_output(value):
    return value.replace("\r\n", "\n").strip()

# python部分
def run_python_code(code, input_data, timeout_seconds):
    '''运行python代码'''
    with tempfile.TemporaryDirectory() as temp_dir:
        code_path = Path(temp_dir) / "main.py"
        code_path.write_text(code, encoding="utf-8")

        started_at = time.perf_counter()
        try:
            completed = subprocess.run(
                [settings.JUDGE_PYTHON_COMMAND, str(code_path)],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=timeout_seconds,
                cwd=temp_dir,
            )
        except subprocess.TimeoutExpired:
            time_used = int((time.perf_counter() - started_at) * 1000)
            return RunResult(status=Submission.Status.TIME_LIMIT_EXCEEDED, time_used=time_used)

        time_used = int((time.perf_counter() - started_at) * 1000)
        if completed.returncode != 0:
            return RunResult(
                status=Submission.Status.RUNTIME_ERROR,
                output=completed.stdout,
                error_message=completed.stderr[-2000:],
                time_used=time_used,
            )
        return RunResult(
            status=Submission.Status.ACCEPTED,
            output=completed.stdout,
            time_used=time_used,
        )

# cpp运行部分
def docker_base_command(temp_dir):
    '''用到的docker命令'''
    return [
        "docker",
        "run",
        "--rm",
        "-i",
        "--network",
        "none",
        "--memory",
        "128m",
        "--cpus",
        "1",
        "--pids-limit",
        "64",
        "-v",
        f"{temp_dir}:/sandbox",
        "-w",
        "/sandbox",
        "gcc:13",
    ]

def run_docker_command(temp_dir, command, input_data="", timeout_seconds=5):
    '''执行dockers命令'''
    started_at = time.perf_counter()
    try:
        completed = subprocess.run(
            docker_base_command(temp_dir) + ["bash", "-lc", command],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
        )
    except FileNotFoundError:
        time_used = int((time.perf_counter() - started_at) * 1000)
        return RunResult(
            status=Submission.Status.SYSTEM_ERROR,
            error_message="Docker command not found. Please install Docker and make sure it is in PATH.",
            time_used=time_used,
        )
    except subprocess.TimeoutExpired:
        time_used = int((time.perf_counter() - started_at) * 1000)
        return RunResult(status=Submission.Status.TIME_LIMIT_EXCEEDED, time_used=time_used)

    time_used = int((time.perf_counter() - started_at) * 1000)
    if completed.returncode != 0:
        return RunResult(
            status=Submission.Status.RUNTIME_ERROR,
            output=completed.stdout,
            error_message=completed.stderr[-2000:],
            time_used=time_used,
        )

    return RunResult(
        status=Submission.Status.ACCEPTED,
        output=completed.stdout,
        time_used=time_used,
    )

def get_source_name(language):
    '''源代码名'''
    if language == Submission.Language.C:
        return "main.c"
    return "main.cpp"


def get_compile_command(language):
    '''编译命令'''
    if language == Submission.Language.C:
        return "gcc main.c -O2 -std=c11 -o main"
    return "g++ main.cpp -O2 -std=c++17 -o main"

def compile_c_code(temp_dir, language):
    '''编译c/cpp代码'''
    result = run_docker_command(
        temp_dir=temp_dir,
        command=get_compile_command(language),
        timeout_seconds=10,
    )
    if result.status == Submission.Status.RUNTIME_ERROR:
        result.status = Submission.Status.COMPILE_ERROR
    return result

def run_c_code(code, language, test_cases, timeout_seconds):
    '''运行c/cpp代码'''
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / get_source_name(language)
        source_path.write_text(code, encoding="utf-8")

        compile_result = compile_c_code(temp_dir, language)
        if compile_result.status != Submission.Status.ACCEPTED:
            return compile_result, []

        results = []
        for test_case in test_cases:
            result = run_docker_command(
                temp_dir=temp_dir,
                command="./main",
                input_data=test_case.input_data,
                timeout_seconds=timeout_seconds,
            )
            results.append((test_case, result))
        return None, results

def acquire_pending_submission():
    '''获取正在pending的代码，运行'''
    with transaction.atomic():
        submission = (
            Submission.objects.select_for_update(skip_locked=True)
            .filter(status=Submission.Status.PENDING)
            .order_by("id")
            .first()
        )
        if submission is None:
            return None
        submission.status = Submission.Status.JUDGING
        submission.save(update_fields=["status"])
        return submission

def create_judge_result(submission, test_case, run_result, status):
    '''创建格式化的评测结果'''
    JudgeResult.objects.create(
        submission=submission,
        testcase=test_case,
        status=status,
        time_used=run_result.time_used,
        memory_used=0,
        output=run_result.output[-2000:],
        error_message=run_result.error_message,
    )

def judge_single_case(submission, test_case, run_result):
    '''判断单个测试点是否正确'''
    status = run_result.status
    if status == Submission.Status.ACCEPTED:
        if normalize_output(run_result.output) != normalize_output(test_case.output_data):
            status = Submission.Status.WRONG_ANSWER
    create_judge_result(submission, test_case, run_result, status)
    return status

def judge_submission(submission):
    '''判题入口'''
    test_cases = list(submission.problem.test_cases.all())
    if not test_cases:
        submission.status = Submission.Status.SYSTEM_ERROR
        submission.error_message = "该题目没有测试点。"
        submission.judged_at = timezone.now()
        submission.save(update_fields=["status", "error_message", "judged_at"])
        return submission

    timeout_seconds = max(1, submission.problem.time_limit / 1000)
    total_score = 0
    max_time = 0
    final_status = Submission.Status.ACCEPTED
    final_error = ""

    JudgeResult.objects.filter(submission=submission).delete()

    if submission.language == Submission.Language.PYTHON3:
        case_results = [
            (
                test_case,
                run_python_code(submission.code, test_case.input_data, timeout_seconds),
            )
            for test_case in test_cases
        ]
    elif submission.language in (Submission.Language.C, Submission.Language.CPP):
        compile_error, case_results = run_c_code(
            submission.code,
            submission.language,
            test_cases,
            timeout_seconds,
        )
        if compile_error is not None:
            submission.status = compile_error.status
            submission.score = 0
            submission.time_used = compile_error.time_used
            submission.error_message = compile_error.error_message
            submission.judged_at = timezone.now()
            submission.save(
                update_fields=["status", "score", "time_used", "error_message", "judged_at"]
            )
            return submission
    else:
        submission.status = Submission.Status.SYSTEM_ERROR
        submission.error_message = f"Unsupported language: {submission.language}"
        submission.judged_at = timezone.now()
        submission.save(update_fields=["status", "error_message", "judged_at"])
        return submission

    for test_case, run_result in case_results:
        status = judge_single_case(submission, test_case, run_result)

        if status == Submission.Status.ACCEPTED:
            total_score += test_case.score

        max_time = max(max_time, run_result.time_used)
        if status != Submission.Status.ACCEPTED:
            final_status = status
            final_error = run_result.error_message

    submission.status = final_status
    submission.score = 100 if final_status == Submission.Status.ACCEPTED else total_score
    submission.time_used = max_time
    submission.error_message = final_error
    submission.judged_at = timezone.now()
    submission.save(
        update_fields=["status", "score", "time_used", "error_message", "judged_at"]
    )
    return submission

def process_next_submission():
    submission = acquire_pending_submission()
    if submission is None:
        return None
    return judge_submission(submission)