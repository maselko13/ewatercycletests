from dataclasses import dataclass
import constants as c

@dataclass(frozen = True)
class TestResult:
    
    passed: bool
    reason: str = c.PASS_MESSAGE
