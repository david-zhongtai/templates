from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuration
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
app.config['HOST'] = os.getenv('FLASK_HOST', '0.0.0.0')
app.config['PORT'] = int(os.getenv('FLASK_PORT', 5000))

# Sample data store (replace with database in production)
items = [
    {"id": 1, "name": "Item 1", "description": "First item"},
    {"id": 2, "name": "Item 2", "description": "Second item"},
]

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "${{ values.appName }}"}), 200

@app.route('/api/v1/items', methods=['GET'])
def get_items():
    """Get all items"""
    return jsonify({"items": items, "count": len(items)}), 200

@app.route('/api/v1/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get a specific item by ID"""
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/api/v1/items', methods=['POST'])
def create_item():
    """Create a new item"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    new_id = max([item["id"] for item in items], default=0) + 1
    new_item = {
        "id": new_id,
        "name": data["name"],
        "description": data.get("description", "")
    }
    items.append(new_item)
    return jsonify(new_item), 201

@app.route('/api/v1/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing item"""
    item = next((item for item in items if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    data = request.get_json()
    if data:
        item.update({k: v for k, v in data.items() if k != "id"})
    
    return jsonify(item), 200

@app.route('/api/v1/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item"""
    global items
    item = next((item for item in items if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )

