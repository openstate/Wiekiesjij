import os
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list 
    help = "Scans through the entire project directory and checks each file" 
    requires_model_validation = True
    
    def directory_py_files(self, parent_directory):
        import pyflakes.scripts.pyflakes as pyflake
        directory_generator = os.walk(parent_directory)
        directory_info = directory_generator.next()
        for file in directory_info[2]:
            if file.endswith('py') and not file.startswith('__init__'):
                pyflake.checkPath('%s/%s' % (directory_info[0], file))
        for directory in directory_info[1]:
            if not directory.startswith('.') and not directory.startswith('migrations'):
                self.directory_py_files('%s/%s' % (parent_directory, directory))
            
    def handle_noargs(self, **options):
        try:
            import pyflakes
            self.directory_py_files(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
        except ImportError:
            print "Pyflakes is missing, try easy_install pyflakes"
            
        