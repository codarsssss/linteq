import os
import whisper
from whisper import DecodingOptions
from whisper.utils import WriteSRT, ResultWriter, WriteVTT, WriteTXT, WriteJSON
from .models import FileData


def write_some_files(transcription_result: dict, options: dict, file, output_dir: str, user_folder_path, files_path):

    user_folder_path = user_folder_path + '/output'

    os.mkdir(user_folder_path)

    result_writer = ResultWriter(output_dir)

    # Создание srt

    srt_writer = WriteSRT(result_writer)
    with open(f"{user_folder_path}/subtitles.srt", "w") as file:

        srt_writer.write_result(transcription_result, file, options)

    # Создание vtt

    vtt_writer = WriteVTT(result_writer)
    with open(f"{user_folder_path}/subtitles.vtt", "w") as file:
        vtt_writer.write_result(transcription_result, file, options)

    # Создание txt

    txt_writer = WriteTXT(result_writer)
    with open(f"{user_folder_path}/subtitles.txt", "w") as file:
        txt_writer.write_result(transcription_result, file, options)

    # Создание json

    json_writer = WriteJSON(result_writer)
    with open(f"{user_folder_path}/subtitles.json", "w") as file:
        json_writer.write_result(transcription_result, file, options)

    print('Done!')

    return {
        'srt': f'{files_path}/output/subtitles.srt',
        'vtt': f'{files_path}/output/subtitles.vtt',
        'txt': f'{files_path}/output/subtitles.txt',
        'json': f'{files_path}/output/subtitles.json'
    }


def transcript_file(file_input, file_name, file_extension, model_type, dt_now):

    file = file_input.read()

    model = whisper.load_model(model_type)

    user_folder_path = f'media/user_requests/{dt_now}'

    file_data_model = FileData()

    file_data_model.path = user_folder_path
    file_data_model.save()
    
    files_path = f'user_requests/{dt_now}'

    if os.path.exists(user_folder_path):
        print('папка есть')
    else:
        os.makedirs(user_folder_path)

    if file_name != '':
        file_name = file_name[:-len(file_extension)].replace('/', '')
        with open(f"{user_folder_path}/{file_name}.{file_extension}", 'wb') as f:
            f.write(file)
        result = model.transcribe(f"{user_folder_path}/{file_name}.{file_extension}")
    else:
        file_name = str(file_input)[:-len(file_extension)-1]
        with open(f"{user_folder_path}/{file_name}.{file_extension}", 'wb') as f:
            f.write(file)
        result = model.transcribe(f"{user_folder_path}/{file_name}.{file_extension}")

    output_dir = "/"

    options = {"max_line_width": 80,
                "max_line_count": 3,
                "highlight_words": False}

    return write_some_files(result, options, file, output_dir, user_folder_path, files_path)

