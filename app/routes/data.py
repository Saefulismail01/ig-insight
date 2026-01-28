"""
Data Routes
Handle data retrieval endpoints
"""
from flask import Blueprint, jsonify, request, current_app

from ..services import load_processed_data

data_bp = Blueprint('data', __name__)


@data_bp.route('/data')
def get_data():
    """Get processed data"""
    upload_id = request.args.get('upload_id') or request.headers.get('X-Upload-Id')
    if not upload_id:
        return jsonify({'error': 'Missing upload_id. Please upload a CSV file first.'}), 400

    processed_data = load_processed_data(current_app.config['UPLOAD_FOLDER'], upload_id)
    
    if processed_data is None:
        return jsonify({'error': 'No data available for this upload_id. Please upload again.'}), 400
    
    return jsonify(processed_data)
