"""
Table of Contents Generator Widget

Provides an interactive widget for generating TOC in Jupyter notebooks.
"""

import ipywidgets as widgets
from IPython.display import display, Javascript
import json
import os
from pathlib import Path
from typing import List, Tuple, Optional


class TOCWidget:
    """Interactive Table of Contents generator for Jupyter notebooks."""
    
    def __init__(self):
        """Initialize the TOC widget with button and output area."""
        # ui elements
        self.button = widgets.Button(
            description='Generate TOC',
            button_style='primary',
            tooltip='Generate table of contents for this notebook',
            icon='list'
        )
        
        self.status = widgets.Label(value="Ready to generate TOC")
        self.output = widgets.Output()
        
        # bnd event handler
        self.button.on_click(self._on_button_click)
        
        # wdget container
        self.widget = widgets.VBox([
            self.button,
            self.status,
            self.output
        ])
    
    def display(self):
        """Display the TOC widget in the notebook."""
        display(self.widget)
        
    def _on_button_click(self, b):
        """Handle button click event."""
        with self.output:
            self.output.clear_output()
            self.status.value = "Generating TOC..."
            
            # Direct Python approach instead of JavaScript
            try:
                # Get the current notebook path
                import ipynbname
                nb_path = str(ipynbname.path())
            except:
                # Fallback: try to get from environment
                try:
                    import os
                    nb_path = os.environ.get('JPY_SESSION_NAME', '')
                    if not nb_path:
                        # Try to find the notebook in current directory
                        import glob
                        notebooks = glob.glob('*.ipynb')
                        if notebooks:
                            nb_path = notebooks[0]
                            print(f"Assuming notebook: {nb_path}")
                except:
                    print("Could not detect notebook path automatically")
                    print("Please run the generate_toc script manually")
                    return
            
            # Import and run the generate_toc function
            try:
                import sys
                import os
                
                # Add scripts to path
                project_root = os.path.abspath(os.path.join(os.getcwd(), '../..'))
                scripts_path = os.path.join(project_root, 'scripts')
                if scripts_path not in sys.path:
                    sys.path.insert(0, scripts_path)
                
                from generate_toc import generate_toc
                
                # Generate TOC
                result = generate_toc(nb_path, update_in_place=True)
                
                if result:
                    print(f"✓ TOC updated successfully!")
                    print(f"  Notebook: {nb_path}")
                    print("\n⚠️  Please reload the notebook to see changes")
                    print("  (In Jupyter: File → Reload Notebook from Disk)")
                else:
                    print("✗ Failed to update TOC")
                    print("  Make sure you have a cell with <!-- TOC --> marker")
                    
            except Exception as e:
                print(f"Error: {e}")
                print("\nTroubleshooting:")
                print("1. Make sure you have a markdown cell with <!-- TOC -->")
                print("2. Ensure the generate_toc.py script is in the scripts/ folder")
                print("3. Check that your notebook has been saved")
            
            self.status.value = "TOC generation completed"
        
    @staticmethod
    def create_toc_cell():
        """
        Helper method to create JavaScript that inserts a TOC marker cell.
        
        Usage in notebook:
            from notebook_tools import TOCWidget
            TOCWidget.create_toc_cell()
        """
        js_code = """
        require(['base/js/namespace'], function(Jupyter) {
            var cell = Jupyter.notebook.insert_cell_below('markdown');
            cell.set_text('<!-- TOC -->');
            cell.render();
        });
        """
        display(Javascript(js_code))
        print("✓ TOC marker cell created below current cell")