import os
from datetime import timedelta
from whisper.utils import WriteSRT, ResultWriter, WriteVTT, WriteTXT, WriteJSON
import openai
from .models import FileData
from .clear_logic import clear_func
from django.conf import settings
from transliterate import slugify
from linteq.secret import OPENAI_TOKEN


openai.api_key = OPENAI_TOKEN


def write_some_files(transcription_result: dict, options: dict, output_dir: str,
                     user_folder_path, files_path, file_name, translate_checkBox, translate_result=None):

    writers = {'srt': WriteSRT, 'vtt': WriteVTT, 'txt': WriteTXT, 'json': WriteJSON}
    
    user_folder_path = user_folder_path + '/output'
    
    os.mkdir(user_folder_path)

    result_writer = ResultWriter(output_dir)

    # Создание srt

    for ext, writer in writers.items():
        writer = writer(result_writer)
        with open(f"{user_folder_path}/{file_name}.{ext}", "w") as file:
            writer.write_result(transcription_result, file, options)


    if translate_checkBox:
        for ext, writer in writers.items():
            writer = writer(result_writer)
            with open(f"media/{files_path}/translate_output/{file_name}.{ext}", "w") as file:
                writer.write_result(translate_result, file, options)

        translated_files = {f'{ext}' + '_tr': f'{files_path}/translate_output/{file_name}.{ext}' for ext, _ in writers.items()}
        
    else:
        translated_files = ''

    transcripted_files = {f'{ext}': f'{files_path}/output/{file_name}.{ext}' for ext, _ in writers.items()}
    transcripted_files['translated_files'] = translated_files
    return transcripted_files


def translate_speech_to_english(file_path):
    audio_file = open(file_path, "rb")
    transcript = openai.Audio.translate("whisper-1", audio_file,
                                        response_format='verbose_json')
    return transcript


def transcript_file(file_input, file_name, file_extension,
                    dt_now, translate_language,
                    translate_checkBox):
    
    output_dir = "/"

    options = {"max_line_width": 80,
               "max_line_count": 3,
               "highlight_words": False}
    
    file = file_input.read()

    slug_file_name = slugify(file_name)

    if slug_file_name is None:
        slug_file_name = file_name


    file_data_model = FileData()
    file_data_model.delete_date = dt_now + timedelta(
        minutes=settings.STORAGE_TIME)

    dt_now = str(dt_now).replace(' ', '_')
    dt_now = str(dt_now).replace(':', '_')

    user_folder_path = f'media/user_requests/{dt_now}'
    file_data_model.path = user_folder_path
    file_data_model.save()

    clear_func()

    files_path = f'user_requests/{dt_now}'

    if not os.path.exists(user_folder_path):
        os.makedirs(user_folder_path)
        translate_output_dir = user_folder_path + '/translate_output'
        os.mkdir(translate_output_dir)

    if file_name != '':
        file_name = slug_file_name.replace('/', '')
        file_name = file_name.replace('*', '')
        pth = f"{user_folder_path}/{file_name}.{file_extension}"
        with open(pth, 'wb') as f:
            f.write(file)
        media_file = open(pth, "rb")
        result = openai.Audio.transcribe(model="whisper-1", file=media_file,
                                        response_format='verbose_json')
        if translate_checkBox:
            return write_some_files(result, options, output_dir, user_folder_path,
                            files_path, file_name, translate_checkBox, translate_speech_to_english(pth))


    else:
        file_name = str(file_input)[:-len(file_extension) - 1]
        pth = f"{user_folder_path}/{file_name}.{file_extension}"
        with open(pth, 'wb') as f:
            f.write(file)
        media_file = open(pth, "rb")
        result = openai.Audio.transcribe(model="whisper-1", file=media_file, 
                                        response_format='verbose_json')
        if translate_checkBox:
            return write_some_files(result, options, output_dir, user_folder_path,
                            files_path, file_name, translate_checkBox, translate_speech_to_english(pth))
            
    return write_some_files(result, options, output_dir, user_folder_path,
                            files_path, file_name, translate_checkBox)

