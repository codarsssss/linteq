import os
from datetime import timedelta
import whisper
from whisper.utils import WriteSRT, ResultWriter, WriteVTT, WriteTXT, WriteJSON
from .models import FileData
from .clear_logic import clear_func
from django.conf import settings


def write_some_files(transcription_result: dict, options: dict, file, output_dir: str, user_folder_path, files_path, file_name):

    user_folder_path = user_folder_path + '/output'

    os.mkdir(user_folder_path)

    result_writer = ResultWriter(output_dir)

    # Создание srt

    srt_writer = WriteSRT(result_writer)
    with open(f"{user_folder_path}/{file_name}.srt", "w") as file:

        srt_writer.write_result(transcription_result, file, options)

    # Создание vtt

    vtt_writer = WriteVTT(result_writer)
    with open(f"{user_folder_path}/{file_name}.vtt", "w") as file:
        vtt_writer.write_result(transcription_result, file, options)

    # Создание txt

    txt_writer = WriteTXT(result_writer)
    with open(f"{user_folder_path}/{file_name}.txt", "w") as file:
        txt_writer.write_result(transcription_result, file, options)

    # Создание json

    json_writer = WriteJSON(result_writer)
    with open(f"{user_folder_path}/{file_name}.json", "w") as file:
        json_writer.write_result(transcription_result, file, options)

    print('Done!')

    return {
        'srt': f'{files_path}/output/{file_name}.srt',
        'vtt': f'{files_path}/output/{file_name}.vtt',
        'txt': f'{files_path}/output/{file_name}.txt',
        'json': f'{files_path}/output/{file_name}.json'
    }


def translate_text(result, translate_language, model):
    translate_result = model.translate(result)
    print(translate_result)


def transcript_file(file_input, file_name, file_extension, 
                    model_type, dt_now, original_language,
                    translate_language, translate_checkBox):

    file = file_input.read()

    model = whisper.load_model(model_type)
    option = whisper.DecodingOptions(language=original_language,
                                     fp16=False)

    user_folder_path = f'media/user_requests/{dt_now}'

    file_data_model = FileData()

    file_data_model.path = user_folder_path
    file_data_model.delete_date = dt_now + timedelta(
        minutes=settings.STORAGE_TIME)
    file_data_model.save()

    clear_func()
    
    files_path = f'user_requests/{dt_now}'

    if os.path.exists(user_folder_path):
        print('папка есть')
    else:
        os.makedirs(user_folder_path)

    if file_name != '':
        file_name = file_name.replace('/', '')
        with open(f"{user_folder_path}/{file_name}.{file_extension}", 'wb') as f:
            f.write(file)
        result = model.transcribe(f"{user_folder_path}/{file_name}.{file_extension}")
        translate_text(result, translate_language, model)
    else:
        file_name = str(file_input)[:-len(file_extension)-1]
        with open(f"{user_folder_path}/{file_name}.{file_extension}", 'wb') as f:
            f.write(file)
        result = model.transcribe(f"{user_folder_path}/{file_name}.{file_extension}")

    output_dir = "/"

    options = {"max_line_width": 80,
                "max_line_count": 3,
                "highlight_words": False}
    
    # Логика перевода текста
    print(translate_checkBox)
    # if translate_checkBox:
    #     translate_text(result, translate_language)

    return write_some_files(result, options, file, output_dir, user_folder_path, files_path, file_name)
