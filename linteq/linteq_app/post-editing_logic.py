import openai
import pandas



def gpt_promt(request):
    system_prompt = "Выполни постредакцию машинного перевода (en) так, чтобы текст стал уникальным. Исправь ошибки в переводе (en), сравнив текст машинного перевода (en) с оригиналом (ru)"

    def generate_corrected_transcript(temperature, system_prompt, audio_file):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=temperature,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": open(audio_file, "")
                }
            ]
        )
        return response['choices'][0]['message']['content']

    corrected_text = generate_corrected_transcript(0, system_prompt, fake_company_filepath)