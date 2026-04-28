from flask import request

@app.route('/submittodoitem', methods=['POST'])
def submit_todo():
    data = request.json
    item_name = data.get("itemName")
    item_desc = data.get("itemDescription")

    return {
        "message": "Item received",
        "itemName": item_name,
        "itemDescription": item_desc
    }