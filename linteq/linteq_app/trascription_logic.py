import whisper


def transcription_video(file_input, file_extension):
    # Обработка видео
    file = file_input.read()
    with open(f"audio.{file_extension}", 'wb') as f:
        f.write(file)

    model = whisper.load_model('base')

    option = whisper.DecodingOptions(language='ru', fp16=False)

    result = model.transcribe(f"audio.{file_extension}")

    print('end')

    return result['text']




# def transcription_audio(file_input, file_extension):
#     # Обработка аудио

#     file = file_input.read()
#     with open(f"audio.{file_extension}", 'wb') as f:
#         f.write(file)

#     model = whisper.load_model("base")

#     audio = whisper.load_audio("audio.mp3")
#     audio = whisper.pad_or_trim(audio)

#     mel = whisper.log_mel_spectrogram(audio).to(model.device)

#     _, probs = model.detect_language(mel)
#     print(f"Detected language: {max(probs, key=probs.get)}")

#     options = whisper.DecodingOptions(language='ru', fp16=False)
#     result = whisper.decode(model, mel, options)

#     return result.text
    

# def choice_audio_or_video_format(file):
#     # Выбор функции
#     file_extension = str(file).split('.')[-1]

#     audio_format = ['m4a', 'wav', ]
#     video_format = ['mp3', 'webm', 'mp4']

#     if file_extension in audio_format:
#         print('audio')
#         return transcription_audio(file, file_extension)
        
#     elif file_extension in video_format:
#         print('video')
#         return transcription_video(file, file_extension)

#     else:
#         print('Формат не поддерживается.')
