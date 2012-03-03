from pylive.views import build_execution_command, write_to_file, check_error
from nose.tools import assert_multi_line_equal, assert_true, assert_equals
from envoy import run
from pylive.constants import * 
#tests start here


def test_build_execution_command():
    assert_multi_line_equal(build_execution_command('example.py'),\
    "%s %s --tmp=%s --timeout=%s --heapsize=%s %s %s"%(pypy_bin,pypy_interact,\
    tmp, timeout, memory, pypy_c, "example.py"))

def test_write_to_file():
    code = """def test():
    print "welcome" """
    assert_true(write_to_file("test.py", code) == True)

def test_check_error_timeout():
    r = run(build_execution_command('test_timeout.py'))
    assert_equals(check_error(r.std_err),"timeout")

