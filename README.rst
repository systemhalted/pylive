README
======

This bit longer README file.

- To run pylive you need sandboxed version of PyPy. It will take hours to build.
Installation can be found at http://doc.pypy.org/en/latest/sandbox.html

- Install `virtualenv`.

- $`virtualenv dev --no-site-packages`.

- $. dev/bin/activate.

- $(dev)pip install -r reqs.txt.

- $(dev)cd pylive.

- $(dev) open constants.py with your fav text editor and edit all the variables.

- `base_path` => Your pypy directory base path.

- `pypy_interact` => path to pypy_interact.py.

- `tmp` => tmp directory to launch scripts to pypy, don't confuse with /tmp 
   directory.

- `timeout` => How long you want pypy to run the script to max in second.

- `pypy_bin` => This is normally `python` or `pypy` version to call the 
   sandboxed code.

- `pypy_c` => Link to `pypy_c`, this is produced as result of compilation of 
   sandboxed pypy.

- `memory` => Maximum memory sandboxed code can use.You can specify in GB, MB.

- `TIMEOUT_MSG` => Message to be displayed when sandboxed code reaches timeout.

- `MEMORY_MSG` => Message to be displayed when sandboxed code crosses alloted
   memory.

- `NOOUTPUT_MSG` => Message to be displayed when sandboxed code doesn't provide
   any output.

- `pylive/pylive/static/analytics.js` => Google code analytics pls change.

- `pylive/pylive/templates/inc/disqus_js.html` => Contains disqus details,
  change them accordingly.

- $(dev)/pylive$ python runserver.py => to start pylive, runs port 5000
    
        or

- $(dev)/pylive$ gunicorn pylive:app => runs on port 8000

- check out for deployment http://flask.pocoo.org/docs/deploying/others/

TESTING
=======

- $cp sample/* YOURPY Virtual directory

- $python tests.py (from project home folder)


Any issues feel free to contact me. 
