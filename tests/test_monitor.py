import pytest
import re
from py_eeive import monitor

def strip_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def test_monitor_success():
    @monitor(retries=1, log=False)
    def success_func():
        return "done"
    
    assert success_func() == "done"

def test_monitor_retry_and_fail(capsys):
    @monitor(retries=2, retry_delay=0.1, log=False)
    def fail_func():
        raise ValueError("Test error")

    fail_func()
    clean_output = strip_ansi(capsys.readouterr().out)
    
    assert "Attempt 1/2" in clean_output
    assert "Attempt 2/2" in clean_output
    assert "Script failed permanently" in clean_output
    assert "ValueError" in clean_output
    assert "Test error" in clean_output

def test_monitor_custom_error_explanation(capsys):
    custom = {
        "ValueError": {"cause": "Custom cause", "fix": "Custom fix"}
    }
    
    @monitor(retries=1, custom_errors=custom, log=False)
    def custom_fail():
        raise ValueError("Oops")

    custom_fail()
    clean_output = strip_ansi(capsys.readouterr().out)
    
    assert "Custom cause" in clean_output
    assert "Custom fix" in clean_output
    assert "ValueError" in clean_output