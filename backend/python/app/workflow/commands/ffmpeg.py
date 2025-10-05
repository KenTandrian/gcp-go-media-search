import os
import subprocess
import tempfile
from ..base import Command, Context
from ... import models

class TranscodeVideo(Command):
    """
    A command to transcode a video file using FFmpeg.
    """
    def __init__(self, name: str, temp_file_path_param: str = "temp_file_path", transcoded_file_path_param: str = "transcoded_file_path"):
        super().__init__(name)
        self.temp_file_path_param = temp_file_path_param
        self.transcoded_file_path_param = transcoded_file_path_param

    def is_executable(self, context: Context) -> bool:
        """
        Ensures that the path to the temporary file exists in the context.
        """
        return context.get(self.temp_file_path_param) is not None

    def execute(self, context: Context):
        """
        Executes the FFmpeg command to transcode the video.
        """
        print("Transcoding video with FFmpeg...")
        input_path = context.get(self.temp_file_path_param)
        
        # Create a new temporary file for the output.
        _, output_path = tempfile.mkstemp(suffix=".mp4")

        try:
            # This is a simple transcoding command. In a real application,
            # you would have more complex logic to handle different formats and settings.
            command = [
                "ffmpeg",
                "-i", input_path,
                "-vcodec", "libx264",
                "-acodec", "aac",
                "-strict", "-2",
                output_path,
            ]
            
            # Execute the command
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            
            print(f"FFmpeg output: {result.stdout}")
            if result.stderr:
                print(f"FFmpeg errors: {result.stderr}")

            context.set(self.transcoded_file_path_param, output_path)
            print(f"Successfully transcoded video to '{output_path}'.")

        except FileNotFoundError:
            raise Exception("FFmpeg is not installed or not in the system's PATH.")
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFmpeg command failed with exit code {e.returncode}: {e.stderr}")
        except Exception as e:
            raise Exception(f"An error occurred during transcoding: {e}")
