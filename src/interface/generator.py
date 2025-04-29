import os
import yaml
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from src.interface.iterators import ComposedIterator, StringListIterator

class AnnotationGenerator:
    def __init__(self, template_dir=None):
        if template_dir is None:
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True
        )
        
    def load_config(self, config_path):
        """Load and validate the YAML configuration file."""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # TODO: Add validation against schema
        return config
        
    def generate_interface(self, config_path, output_dir):
        """Generate the annotation interface from a YAML config file."""
        config = self.load_config(config_path)
        
        # Process iterator configuration
        self._process_iterator_config(config)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate HTML files
        self._generate_html_files(config, output_dir)
        
        # Generate backend files
        self._generate_backend_files(config, output_dir)
    
    def _process_iterator_config(self, config):
        """Process iterator configuration to prepare it for the template."""
        if 'input' in config and 'iterator' in config['input']:
            iterator_config = config['input']['iterator']
            
            # If it's a composed iterator, process each iterator
            if iterator_config.get('type') == 'composed':
                for name, iterator in iterator_config.get('config', {}).get('iterators', {}).items():
                    # Extract values from the iterator
                    if 'values' in iterator:
                        # Convert values to a list to ensure JSON serialization
                        iterator['values_list'] = list(iterator['values'])
                    else:
                        # If no values method, use an empty list
                        iterator['values_list'] = []
                    
                    # Add a values property that returns the list
                    iterator['values'] = iterator['values_list']
                    
        return config
        
    def _generate_html_files(self, config, output_dir):
        """Generate the HTML files for the interface."""
        # Load the base template
        template = self.env.get_template('html/base.html.j2')
        
        # Generate index.html (development version)
        index_html = template.render(**config)
        with open(os.path.join(output_dir, 'index.html'), 'w') as f:
            f.write(index_html)
            
        # Generate index.prod.html (production version)
        # TODO: Add production-specific modifications
        with open(os.path.join(output_dir, 'index.prod.html'), 'w') as f:
            f.write(index_html)
            
    def _generate_backend_files(self, config, output_dir):
        """Generate the backend files for the interface."""
        # Load the backend template
        template = self.env.get_template('backend/app.py.j2')
        
        # Generate app.py
        app_py = template.render(**config)
        with open(os.path.join(output_dir, 'app.py'), 'w') as f:
            f.write(app_py)
            
def main():
    """Command-line interface for the generator."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate annotation interface from YAML config')
    parser.add_argument('config', help='Path to YAML configuration file')
    parser.add_argument('--output', '-o', help='Output directory', default='output')
    
    args = parser.parse_args()
    
    generator = AnnotationGenerator()
    generator.generate_interface(args.config, args.output)
    
if __name__ == '__main__':
    main() 