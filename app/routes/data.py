"""
Data Routes
Handle data retrieval endpoints
"""
from flask import Blueprint, jsonify

data_bp = Blueprint('data', __name__)


@data_bp.route('/data')
def get_data():
    """Get processed data"""
    from .upload import get_processed_data
    
    processed_data = get_processed_data()
    
    if processed_data is None:
        return jsonify({'error': 'No data available. Please upload a CSV file first.'}), 400
    
    return jsonify(processed_data)
