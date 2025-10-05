import json
from ..base import Command, Context
from ... import models

class MediaTriggerReader(Command):
    """
    A command to read and parse the initial media trigger message.
    """
    def __init__(self, name: str, trigger_message_param: str = "trigger_message", media_param: str = "media"):
        super().__init__(name)
        self.trigger_message_param = trigger_message_param
        self.media_param = media_param

    def is_executable(self, context: Context) -> bool:
        """
        Ensures that the trigger message exists in the context.
        """
        return context.get(self.trigger_message_param) is not None

    def execute(self, context: Context):
        """
        Parses the trigger message and creates the initial Media object.
        """
        print("Reading media trigger message...")
        message_data = context.get(self.trigger_message_param)
        
        try:
            data = json.loads(message_data)
            file_name = data.get("name")
            bucket_name = data.get("bucket")

            if not file_name or not bucket_name:
                raise ValueError("Invalid trigger message: missing 'name' or 'bucket'.")

            media = models.Media.new_media(file_name)
            media.media_url = f"gs://{bucket_name}/{file_name}"
            
            context.set(self.media_param, media)
            print(f"Successfully created initial media object for '{file_name}'.")

        except (json.JSONDecodeError, ValueError) as e:
            raise Exception(f"Failed to parse trigger message: {e}")
