"""
Upload Routes
Handle file upload and processing
"""
from flask import Blueprint, request, jsonify, current_app
import pandas as pd
import io
from ..services import DataProcessor, create_upload_id, save_processed_data

upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """Upload and process CSV file"""

    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if file and file.filename.endswith('.csv'):
            try:
                print(f"Processing file: {file.filename}")
                
                # Read CSV file with proper settings for quoted fields and BOM
                # Use utf-8-sig to handle BOM (Byte Order Mark)
                file_content = file.stream.read().decode("utf-8-sig")
                stream = io.StringIO(file_content, newline=None)
                df = pd.read_csv(stream, quotechar='"', escapechar='\\')
                
                print(f"CSV loaded successfully. Shape: {df.shape}")
                print(f"Columns: {df.columns.tolist()}")
                print(f"First row Views: {df['Views'].iloc[0] if 'Views' in df.columns else 'Views column not found'}")
                
                # Process the data
                processor = DataProcessor()
                processed_data = processor.process_insight_data(df)

                # Persist per-upload result (multi-user safe vs global variable)
                upload_id = create_upload_id()
                save_processed_data(
                    current_app.config['UPLOAD_FOLDER'],
                    upload_id,
                    processed_data
                )
                
                print("Data processed successfully")
                
                return jsonify({
                    'success': True,
                    'message': 'File uploaded and processed successfully',
                    'upload_id': upload_id,
                    # keep returning data for current UI behavior
                    'data': processed_data,
                })
                
            except Exception as e:
                import traceback
                error_detail = traceback.format_exc()
                print(f"Error processing file: {str(e)}")
                print(f"Full traceback: {error_detail}")
                
                return jsonify({
                    'success': False, 
                    'error': f'Error processing file: {str(e)}', 
                    'detail': error_detail
                }), 400
        
        return jsonify({
            'success': False, 
            'error': 'Invalid file format. Please upload a CSV file.'
        }), 400
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Unexpected error in upload_file: {str(e)}")
        print(f"Full traceback: {error_detail}")
        
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}',
            'detail': error_detail
        }), 500
