from enum import StrEnum


class ExecutionStatus(StrEnum):
    COLLECTED = "collected"
    STARTED = "started"
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"
