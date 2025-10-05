import os
from ..base import Command, Context

class MediaCleanup(Command):
    """
    A command to delete temporary files created during the workflow.
    """
    def __init__(self, name: str, *temp_file_path_params: str):
        super().__init__(name)
        if not temp_file_path_params:
            raise ValueError("At least one temp_file_path_param must be provided.")
        self.temp_file_path_params = temp_file_path_params

    def execute(self, context: Context):
        """
        Deletes all the temporary files specified by the path parameters.
        """
        print("Cleaning up temporary files...")
        
        for param in self.temp_file_path_params:
            file_path = context.get(param)
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"Successfully deleted temporary file: {file_path}")
                except OSError as e:
                    # In a real app, you might want to log this as a warning
                    # instead of raising an exception that halts the chain.
                    print(f"Error deleting temporary file {file_path}: {e}")
