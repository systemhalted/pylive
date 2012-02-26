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


@app.route('/pylive/')
def pylive():
    return render_template('live.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/examples/')
def examples():
    return render_template('examples.html')

@app.route('/features/')
def features():
    return render_template('features.html')

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
    lexer = PythonTracebackLexer()
    formatter = HtmlFormatter(linenos = True)
    generated_code = highlight(code, lexer, formatter)
    return generated_code

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
    if error.find("SIGTERM") > 0:
        error_type = 'timeout'
    elif error.find('MemoryError') > 0:
        error_type = 'memory'
    elif error.find("Traceback") > 0:
        error_type = 'normal'
    else:
        error_type = None
    return error_type

def process_error(errors):
    errors = errors.split('\n')
    extracted_errors = errors[4:]
    output = '\n'.join(extracted_errors[:-2])
    return output

@app.route('/pylive/execute/', methods=['GET'])
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
        if result.std_out:
            return jsonify(success=1, output=result.std_out, code=generated_code)
        else:
            error_type = check_error(result.std_err)
            d = {'timeout': TIMEOUT_MSG,
                 'memory': MEMORY_MSG,
                 'normal': highlight_error(process_error(result.std_err)),
                  None: NOOUTPUT_MSG}
            print d['normal']        
            return jsonify(success=1, output=d[error_type], code=generated_code)
    else:
        return jsonify(success=0, message='something is wrong from our end')


