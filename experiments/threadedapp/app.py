import os
import time
from flask import Flask, abort
from tasks import flask_async, tasks

app = Flask(__name__)
app.secret_key = os.urandom(42)


@app.route('/foo')
@flask_async
def foo():
    time.sleep(10)
    return {'Result': True}


@app.route('/foo/<task_id>', methods=['GET'])
def foo_results(task_id):
    """
        Return results of asynchronous task.
        If this request returns a 202 status code, it means that task hasn't finished yet.
        """
    task = tasks.get(task_id)
    if task is None:
        abort(404)
    if 'result' not in task:
        return {'TaskID': task_id}, 202
    return task['result']


if __name__ == '__main__':
    app.run(debug=True)
