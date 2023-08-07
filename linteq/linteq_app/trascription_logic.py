import os
from datetime import timedelta
import whisper
from whisper.utils import WriteSRT, ResultWriter, WriteVTT, WriteTXT, WriteJSON
import openai
from .models import FileData
from .clear_logic import clear_func
from django.conf import settings
import subprocess
from transliterate import slugify
from linteq.secret import OPENAI_TOKEN
import requests
import json


openai.api_key = OPENAI_TOKEN


def write_some_files(transcription_result: dict, options: dict, output_dir: str,
                     user_folder_path, files_path, file_name, translate_checkBox):
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

    if translate_checkBox:
        translated_files = {
            'srt_tr': f'{files_path}/translate_output/{file_name}.srt',
            'vtt_tr': f'{files_path}/translate_output/{file_name}.vtt',
            'txt_tr': f'{files_path}/translate_output/{file_name}.txt',
            'json_tr': f'{files_path}/translate_output/{file_name}.json'
        }
    else:
        translated_files = ''

    return {
        'srt': f'{files_path}/output/{file_name}.srt',
        'vtt': f'{files_path}/output/{file_name}.vtt',
        'txt': f'{files_path}/output/{file_name}.txt',
        'json': f'{files_path}/output/{file_name}.json',
        'translated_files': translated_files
    }


def translate_speech_to_english(file_path, original_language, translate_output_dir):
    command = f'whisper --model base --task translate --language {original_language} \
          {file_path} --output_dir {translate_output_dir}'

    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        translated_text = result.decode('utf-8').strip()
        return translated_text
    except subprocess.CalledProcessError:
        return None


def transcript_file(file_input, file_name, file_extension,
                    model_type, dt_now, original_language,
                    translate_language, translate_checkBox):
    file = file_input.read()

    slug_file_name = slugify(file_name)

    if slug_file_name is None:
        slug_file_name = file_name

    model = whisper.load_model(model_type)

    # ЯЗЫК
    # option = whisper.DecodingOptions(language=original_language,
    #                                  fp16=False)



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
        # result = model.transcribe(f"{user_folder_path}/{file_name}.{file_extension}")
        result = openai.Audio.transcribe(model="whisper-1", file=media_file, response_format='json')
        if translate_checkBox:
            translate_speech_to_english(pth, original_language, translate_output_dir)


    else:
        file_name = str(file_input)[:-len(file_extension) - 1]
        pth = f"{user_folder_path}/{file_name}.{file_extension}"
        with open(pth, 'wb') as f:
            f.write(file)
        media_file = open(pth, "rb")
        # result = model.transcribe(f"{user_folder_path}/{file_name}.{file_extension}")
        result = openai.Audio.transcribe(model="whisper-1", file=media_file, response_format='json')
        if translate_checkBox:
            translate_speech_to_english(pth, original_language, translate_output_dir)

    output_dir = "/"

    options = {"max_line_width": 80,
               "max_line_count": 3,
               "highlight_words": False}

    return write_some_files(result, options, output_dir, user_folder_path, files_path, file_name, translate_checkBox)

# transcription_result: dict, options: dict, file, output_dir: str,
#                      user_folder_path, files_path, file_name, translate_checkBox
