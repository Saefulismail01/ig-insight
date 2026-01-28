"""
Routes package initialization
"""
from .upload import upload_bp
from .data import data_bp
from .analysis import analysis_bp

__all__ = ['upload_bp', 'data_bp', 'analysis_bp']
