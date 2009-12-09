import os
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list 
    help = "Scans through the entire project directory and collects all the stale/obsolete import statements" 
    requires_model_validation = True

    def import_statement_extractor(self, directory_path, python_file):
        python_file = '%s/%s' % (directory_path, python_file)       
        for line_no, line in enumerate(open(python_file)):
            line = line.strip()
            if not line.startswith('#') or not line.startswith("'''"):
                if line.startswith('from ') or line.startswith('import '):
                    try:
                        exec(line)
                    except ImportError, e:
                        print '%s(%i): at: %s: Reason: %s' % (python_file, line_no, line, e.__str__())
                    except Exception, e:
                        print '%s(%i): at: %s: Reason: %s' % (python_file, line_no, line, e.__str__())
    
    def directory_py_files(self, parent_directory):
        import os
        directory_generator = os.walk(parent_directory)
        directory_info = directory_generator.next()
        for file in directory_info[2]:
            if file.endswith('py'):
                self.import_statement_extractor(directory_info[0], file)
        for directory in directory_info[1]:
            if not directory.startswith('.'):
                self.directory_py_files('%s/%s' % (parent_directory, directory))
            
    def handle_noargs(self, **options):
        from django.conf import settings
        self.directory_py_files(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))