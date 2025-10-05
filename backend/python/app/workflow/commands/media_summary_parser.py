import json
from ..base import Command, Context
from ... import models

class MediaSummaryParser(Command):
    """
    A command to parse a JSON string into a MediaSummary object.
    """
    def __init__(self, name: str, json_string_param: str = "summary_json", summary_param: str = "media_summary"):
        super().__init__(name)
        self.json_string_param = json_string_param
        self.summary_param = summary_param

    def is_executable(self, context: Context) -> bool:
        """
        Ensures that the JSON string to be parsed exists in the context.
        """
        return context.get(self.json_string_param) is not None

    def execute(self, context: Context):
        """
        Parses the JSON string and stores the resulting MediaSummary object in the context.
        """
        print("Parsing media summary JSON...")
        json_string = context.get(self.json_string_param)
        
        try:
            summary_dict = json.loads(json_string)
            summary = models.MediaSummary(**summary_dict)
            
            context.set(self.summary_param, summary)
            print("Successfully parsed media summary JSON.")

        except json.JSONDecodeError as e:
            raise Exception(f"Failed to decode summary JSON: {e}")
        except Exception as e:
            # This could be a Pydantic validation error
            raise Exception(f"Failed to parse summary object: {e}")
