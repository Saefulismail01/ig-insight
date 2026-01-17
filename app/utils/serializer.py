"""
Data Serialization Utilities
"""
import pandas as pd
import numpy as np


def serialize_data(obj):
    """Recursively serialize pandas objects to JSON-serializable types"""
    if isinstance(obj, dict):
        return {key: serialize_data(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [serialize_data(item) for item in obj]
    elif pd.isna(obj) if hasattr(pd, 'isna') else False:
        return None
    elif isinstance(obj, (pd.Timestamp, pd.Period)):
        return str(obj)
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        # Handle NaN and inf values
        if np.isnan(obj) or np.isinf(obj):
            return None
        return float(obj)
    elif isinstance(obj, float):
        # Handle Python float NaN and inf values
        if np.isnan(obj) or np.isinf(obj):
            return None
        return obj
    elif isinstance(obj, int):
        return obj
    elif hasattr(obj, 'item'):  # numpy scalars
        val = obj.item()
        if isinstance(val, float) and (np.isnan(val) or np.isinf(val)):
            return None
        return val
    else:
        return obj
