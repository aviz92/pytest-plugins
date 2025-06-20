from dataclasses import dataclass
from typing import Optional

from pytest_plugins.models.status import ExecutionStatus


@dataclass
class TestData:
    test_file_name: str
    class_test_name: str
    test_name: str
    test_full_name: str
    test_status: ExecutionStatus = ExecutionStatus.COLLECTED
    test_markers: Optional[list] = None
    test_start_time: Optional[str] = None
    test_end_time: Optional[str] = None
    test_duration_sec: Optional[float] = None
    exception_message: Optional[str] = None
