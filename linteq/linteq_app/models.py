from django.db import models
import whisper
import time

from whisper.utils import ResultWriter, WriteSRT, WriteVTT, WriteTXT, WriteJSON


class UserFile(models.Model):
    user_file = models.FileField()
    max_line_width = models.IntegerField(default=80)
    max_line_count = models.IntegerField(default=3)
    file_path = models.CharField(max_length=255)
    options = dict()
    model_type = 'base'
    model = ''
    result = dict()
    result_writer = ''
    srt_writer = ''

    def __init__(self):
        super().__init__()
        self.file_path =f'/media{self.user_file.name}/{time.time()}'

        self.model = whisper.load_model(self.model_type)

        self.result = self.model.transcribe(self.user_file)

        self.result_writer = ResultWriter(self.file_path)

        self.srt_writer = WriteSRT(self.result_writer)

        self.test_()


    def test_(self):
        srt_writer = WriteSRT(self.result_writer)
        with open("media/subtitles.srt", "w") as file:
            srt_writer.write_result(self.result, file, self.options)

        # Создание vtt

        vtt_writer = WriteVTT(self.result_writer)
        with open("media/subtitles.vtt", "w") as file:
            vtt_writer.write_result(self.result, file, self.options)

        # Создание txt

        txt_writer = WriteTXT(self.result_writer)
        with open("media/subtitles.txt", "w") as file:
            txt_writer.write_result(self.result, file, self.options)

        # Создание json

        json_writer = WriteJSON(self.result_writer)
        with open("media/subtitles.json", "w") as file:
            json_writer.write_result(self.result, file, self.options)

        print('Done!')
