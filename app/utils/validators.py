"""
Data Validation Utilities
"""


def validate_csv_columns(df, required_columns=None):
    """Validate CSV has required columns"""
    if required_columns is None:
        required_columns = ['Publish time', 'Post type']
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    return True


def validate_file_extension(filename, allowed_extensions=None):
    """Validate file extension"""
    if allowed_extensions is None:
        allowed_extensions = {'csv'}
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
