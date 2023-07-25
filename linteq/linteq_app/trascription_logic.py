import whisper
from whisper import DecodingOptions
from whisper.utils import WriteSRT, ResultWriter, WriteVTT, WriteTXT, WriteJSON



def write_some_files(transcription_result: dict, options: dict, file, output_dir: str):
    result_writer = ResultWriter(output_dir)

    # Создание srt

    srt_writer = WriteSRT(result_writer)
    with open("media/subtitles.srt", "w") as file:
        srt_writer.write_result(transcription_result, file, options)

    # Создание vtt

    vtt_writer = WriteVTT(result_writer)
    with open("media/subtitles.vtt", "w") as file:
        vtt_writer.write_result(transcription_result, file, options)

    # Создание txt

    txt_writer = WriteTXT(result_writer)
    with open("media/subtitles.txt", "w") as file:
        txt_writer.write_result(transcription_result, file, options)

    # Создание json

    json_writer = WriteJSON(result_writer)
    with open("media/subtitles.json", "w") as file:
        json_writer.write_result(transcription_result, file, options)

    print('Done!')


def transcription_video(file_input, file_extension):
    # Обработка видео
    file = file_input.read()
    with open(f"audio.{file_extension}", 'wb') as f:
        f.write(file)

    model = whisper.load_model('base')

    # options = whisper.DecodingOptions(language='ru', fp16=False)

    result = model.transcribe(f"audio.{file_extension}")

    output_dir = "/"

    options = {"max_line_width": 80,
                "max_line_count": 3,
                "highlight_words": False}
    
    write_some_files(result, options, file, output_dir)

