"""
Schema definitions for the Annotation Toolkit.
"""

import os
import yaml

def load_schema(schema_name):
    """
    Load a schema by name.
    
    Args:
        schema_name (str): Name of the schema file without extension
        
    Returns:
        dict: The loaded schema
    """
    schema_path = os.path.join(os.path.dirname(__file__), f"{schema_name}.yaml")
    with open(schema_path, 'r') as f:
        return yaml.safe_load(f)

# Load common schemas
BASE_SCHEMA = load_schema('base_schema')
SINGLE_IMAGE_RATING_SCHEMA = load_schema('single_image_rating')

__all__ = ['load_schema', 'BASE_SCHEMA', 'SINGLE_IMAGE_RATING_SCHEMA'] 