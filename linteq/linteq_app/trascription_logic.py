import whisper


def transcription_audio(file_input):
    file = file_input.read()
    with open('audio.mp4', 'wb') as f:
        f.write(file)

    model = whisper.load_model('base')
    option = whisper.DecodingOptions(language='ru', fp16=False)
    result = model.transcribe('audio.mp4')

    print(result)
