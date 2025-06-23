# lib/notebook_tools/widgets/export_widget.py

import ipywidgets as widgets
from IPython.display import display
from pathlib import Path

class ExportWidget:
    """Export widget for creating clean notebooks from working notebooks."""
    
    def __init__(self):
        self.button = widgets.Button(
            description='Export Clean Notebook',
            button_style='success',
            tooltip='Export this working notebook to a clean version',
            icon='download'
        )
        
        self.status = widgets.Label(value="")
        self.output = widgets.Output()
        
        self.button.on_click(self._on_button_click)
        
        self.widget = widgets.VBox([
            self.button,
            self.status,
            self.output
        ])
    
    def display(self):
        display(self.widget)
        
    def _on_button_click(self, b):
        with self.output:
            self.output.clear_output()
            self.status.value = "Exporting..."
            
            try:
                try:
                    import ipynbname
                    nb_path = Path(ipynbname.path())
                except ImportError:
                    # Fallback: find working notebook in current directory
                    import os
                    cwd = Path.cwd()
                    working_notebooks = list(cwd.glob('*.working.ipynb'))
                    if working_notebooks:
                        nb_path = working_notebooks[0]
                    else:
                        print("✗ No .working.ipynb file found in current directory")
                        self.status.value = "No working notebook found"
                        return
                
                if '.working.' not in nb_path.name:
                    print("✗ This is not a .working notebook")
                    self.status.value = "Not a working notebook"
                    return
                
                # Import export function
                import sys
                sys.path.insert(0, '../../lib')
                from notebook_tools.export import export_notebook
                
                result_path = export_notebook(str(nb_path))
                print(f"✓ Exported to: {result_path}")
                print(f"  Tag cells with 'export' to include them")
                print(f"  Push to git to trigger markdown conversion")
                
                self.status.value = "Export successful"
                
            except Exception as e:
                print(f"✗ Error: {e}")
                self.status.value = "Export failed"