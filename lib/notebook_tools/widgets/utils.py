"""
Utility functions for notebook widgets.
"""

import os
import sys
from pathlib import Path


def setup_path():
    """
    Ensure the scripts directory is in the Python path.
    This allows importing the generate_toc module from anywhere.
    """
    project_root = Path.cwd()
    scripts_dir = project_root / 'scripts'
    
    if scripts_dir.exists() and str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))


def get_notebook_info():
    """
    Get information about the current notebook.
    Returns a dict with notebook path and name.
    """
    try:
        # This works in Jupyter/IPython environment
        from IPython import get_ipython
        ipython = get_ipython()
        
        if hasattr(ipython, 'kernel'):
            # We're in a notebook
            return {
                'is_notebook': True,
                'kernel_id': ipython.kernel.ident
            }
    except:
        pass
    
    return {'is_notebook': False}