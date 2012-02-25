from flask import render_template, request, jsonify
from pylive import app
from envoy import run
from constants import *
import datetime
from os.path import sep
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename, PythonTracebackLexer

def build_execution_command(filename):
    command = "%s %s --tmp=%s --timeout=%s --heapsize=%s %s %s"%(pypy_bin,\
                pypy_interact,tmp,timeout, memory, pypy_c, filename)
    return command


@app.route('/')
def index():
    return render_template('live.html')

def write_to_file(filename, code):
    try:
        with open(filename, 'w') as f:
            f.writelines(code)
        return True
    except IOError:
        return False        

def highlight_sourcecode(code):
    lexer = get_lexer_for_filename("python.py", stripall= True)
    formatter = HtmlFormatter(linenos = True)
    generated_code = highlight(code, lexer, formatter)
    return generated_code

def highlight_error(code):
    code = code.split('Traceback')
    lexer = PythonTracebackLexer()
    formatter = HtmlFormatter(linenos = True)
    generated_code = highlight(code[1], lexer, formatter)
    #return generated_code.split('[Sub')[0])

def check_error(error):
    """
    Warning: cannot find your CPU L2 cache size in /proc/cpuinfo
    Not Implemented: SomeString(no_nul=True)
    RuntimeError
    'import site' failed

    pypy print above four lines irrespective of success and failure in pypy1.7
    and pypy1.8 sandbox.

    Check for MemoryError(greater than heapsize), SIGTERM(time consuming),
    Traceback(normal error like syntax error, ImportError)
    """
    error_type = ''
    if error.find("SIGTERM"):
        error_type = 'timeout'
    elif error.find('MemoryError'):
        error_type = 'memory'
    elif error.find("Traceback"):
        error_type = 'normal'
    else:
        error_type = 'special'
    return error_type

def process_error(errors):
    errors = errors.replace(' ','&nbsp').split('\n')
    extracted_errors = errors[4:]
    output = '<br/>'.join(extracted_errors)
    return output

@app.route('/execute/', methods=['GET'])
def execute_python():
    code = request.args.get('code')
    base = '_'.join(datetime.datetime.now().ctime().split()) 
    base_filename = '.'.join([base, 'py'])
    base_html = '.'.join([base, 'html'])
    filename = sep.join([tmp, base_filename])
    filename_html = sep.join([tmp, base_html])
    if write_to_file(filename, code):
        result = run(build_execution_command(base_filename))
        generated_code = highlight_sourcecode(code)
        print result.std_err
        print result.std_err.find('Traceback')
        if result.std_err.find('Traceback') >= 0:
            output = highlight_error(result.std_err)
            return jsonify(success=1, output=output, code=generated_code)
        else:
            return jsonify(success=1, output=result.std_out, code=generated_code)
    else:
        return jsonify(success=0, message='something is wrong from our end')


