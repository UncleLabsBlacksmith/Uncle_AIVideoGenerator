"""Colab worker bridge helpers for Uncle AI Video Generator."""
import os
from functools import wraps
from flask import request, jsonify

COLAB_MODEL = 'colab/free'
COLAB_MODEL_META = {
    'id': COLAB_MODEL,
    'name': 'Google Colab (ฟรี · ต้องเปิด notebook)',
    'pricing': {'cost_per_second': 0},
}

def worker_token_ok():
    expected = os.environ.get('COLAB_WORKER_TOKEN', '').strip()
    if not expected:
        return False, 'Set COLAB_WORKER_TOKEN in .env'
    got = (request.headers.get('X-Worker-Token') or '').strip()
    if got != expected:
        return False, 'Invalid worker token'
    return True, ''

def require_worker(fn):
    @wraps(fn)
    def wrap(*a, **kw):
        ok, err = worker_token_ok()
        if not ok:
            return jsonify(error=err), 401
        return fn(*a, **kw)
    return wrap

def is_colab_job(job_id):
    return str(job_id or '').startswith('colab-')

def colab_model_item():
    return dict(COLAB_MODEL_META)
