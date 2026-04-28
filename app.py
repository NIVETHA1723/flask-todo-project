from flask import jsonify

@app.route('/api')
def api():
    return jsonify({
        "message": "Hello from Nivetha_new branch",
        "status": "success"
    })