from pylive.views import build_execution_command, write_to_file, check_error
from nose.tools import assert_multi_line_equal, assert_true, assert_equals
from envoy import run
#tests start here

def test_build_execution_command():
    assert_multi_line_equal(build_execution_command('example.py'),"pypy1.7 /home/kracekumar/pypy-pypy-2346207d9946/pypy/translator/sandbox/pypy_interact.py --tmp=/home/kracekumar/pypy-pypy-2346207d9946/pypy/translator/sandbox/virtualtmp --timeout=60 --heapsize=200m /home/kracekumar/pypy-pypy-2346207d9946/pypy-c example.py", msg="failed")

def test_write_to_file():
    code = """def test():
    print "welcome" """
    assert_true(write_to_file("test.py", code) == True)

def test_check_error_timeout():
    r = run("pypy1.7 /home/kracekumar/pypy-pypy-2346207d9946/pypy/translator/sandbox/pypy_interact.py --tmp=/home/kracekumar/pypy-pypy-2346207d9946/pypy/translator/sandbox/virtualtmp --timeout=60 --heapsize=200m /home/kracekumar/pypy-pypy-2346207d9946/pypy-c test_timeout.py")
    assert_equals(check_error(r.std_err),"timeout")

