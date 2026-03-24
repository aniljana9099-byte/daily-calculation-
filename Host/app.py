"""
Sirf do pages: Cash Flow (/) aur Extra/Short (/extra-short).
MySQL table: cash_flow_snapshot — /api/cash-flow-data
"""
import json

from flask import Flask, jsonify, redirect, request, send_from_directory, make_response

from db import get_connection, payload_from_row

app = Flask(__name__, static_folder='.')


def _send_html_no_cache(filename):
    resp = make_response(send_from_directory('.', filename))
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    resp.headers['Pragma'] = 'no-cache'
    return resp


@app.route('/')
def cash_flow():
    return _send_html_no_cache('cash-flow-summary.html')


@app.route('/extra-short')
def extra_short():
    return _send_html_no_cache('extra-short-calc.html')


@app.route('/dashboard')
def legacy_dashboard():
    return redirect('/', code=301)


@app.route('/dashboard/cash-flow-summary')
def legacy_cash_flow():
    return redirect('/', code=301)


@app.route('/dashboard/extra-short-calc')
def legacy_extra_short():
    return redirect('/extra-short', code=301)


@app.route('/api/cash-flow-data', methods=['GET'])
def api_get_cash_flow():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            'SELECT payload FROM cash_flow_snapshot WHERE snapshot_key = %s',
            ('default',),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            return jsonify({'ok': True, 'data': {}})
        data = payload_from_row(row['payload'])
        return jsonify({'ok': True, 'data': data if isinstance(data, dict) else {}})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e), 'data': {}}), 503


@app.route('/api/cash-flow-data', methods=['POST'])
def api_post_cash_flow():
    try:
        body = request.get_json(force=True, silent=True) or {}
        raw = body.get('data')
        if raw is None:
            return jsonify({'ok': False, 'error': 'missing data'}), 400
        if not isinstance(raw, dict):
            return jsonify({'ok': False, 'error': 'data must be object'}), 400
        payload = json.dumps(raw, ensure_ascii=False)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO cash_flow_snapshot (snapshot_key, payload)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE payload = VALUES(payload), updated_at = CURRENT_TIMESTAMP
            """,
            ('default', payload),
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 503


@app.route('/api/cash-flow-data', methods=['DELETE'])
def api_delete_cash_flow():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM cash_flow_snapshot WHERE snapshot_key = %s', ('default',))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 503


@app.route('/api/health')
def api_health():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({'ok': True, 'database': 'connected'})
    except Exception as e:
        return jsonify({'ok': False, 'database': 'error', 'error': str(e)}), 503


@app.route('/styles.css')
def styles():
    resp = make_response(send_from_directory('.', 'styles.css', mimetype='text/css'))
    resp.headers['Cache-Control'] = 'public, max-age=3600'
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
