import pyaudio
import array
import wave
import webrtcvad
import simpleaudio as sa
import requests
import openai
import json
import os
import utils
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']
rss_api_key = os.environ['RSS_API']


# include chat history in it
def get_completion_from_messages(messages,
                                 model="gpt-3.5-turbo",
                                 temperature=0,
                                 max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # degree of randomness of the model's output
        max_tokens=max_tokens,  # maximum number of tokens the model can ouptut
    )
    return response.choices[0].message["content"]


def process_user_message(user_input, all_messages, debug=True):
    delimiter = "```"

    # Step 1: Check if it flags the Moderation API or is a prompt injection
    response = openai.Moderation.create(input=user_input)
    moderation_output = response["results"][0]

    if moderation_output["flagged"]:
        print("Step 1: Input flagged by Moderation API.")
        return "Sorry, we cannot process this request."

    if debug:
        print("Step 1: Input passed moderation check.")

    # category_and_product_response = utils.find_category_and_product_only(
    #   user_input, utils.get_products_and_category())
    # print(print(category_and_product_response)
    # Step 2: Extract the list of products
    # category_and_product_list = utils.read_string_to_list(category_and_product_response)
    # print(category_and_product_list)

    # if debug: print("Step 2: Extracted list of products.")

    # Step 3: If products are found, look them up
    # product_information = utils.generate_output_string(category_and_product_list)
    # if debug: print("Step 3: Looked up product information.")

    # Step 4: Answer the user question
    # system_message = f"""
    # You are a customer service assistant for a large electronic store. \
    # Respond in a friendly and helpful tone, with concise answers. \
    # Make sure to ask the user relevant follow-up questions.
    # """
    system_message = utils.system_message
    product_information = json.dumps(utils.products)
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"},
        {'role': 'assistant', 'content': f"Relevant product information:\n{product_information}"}
    ]

    final_response = get_completion_from_messages(all_messages + messages)
    if debug:
        print("Step 4: Generated response to user question.")
    all_messages = all_messages + [messages[1]]

    # Step 5: Put the answer through the Moderation API
    response = openai.Moderation.create(input=final_response)
    moderation_output = response["results"][0]

    if moderation_output["flagged"]:
        if debug:
            print("Step 5: Response flagged by Moderation API.")
        return "Sorry, we cannot provide this information."

    if debug:
        print("Step 5: Response passed moderation check.")

    # Step 6: Ask the model if the response answers the initial user query well
    user_message = f"""
    Customer message: {delimiter}{user_input}{delimiter}
    Agent response: {delimiter}{final_response}{delimiter}

    Does the response sufficiently answer the question?
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]
    evaluation_response = get_completion_from_messages(messages)
    if debug:
        print("Step 6: Model evaluated the response.")

    # Step 7: If yes, use this answer; if not, say that you will connect the user to a human
    if "Y" in evaluation_response:  # Using "in" instead of "==" to be safer for model output variation (e.g., "Y." or "Yes")
        if debug:
            print("Step 7: Model approved the response.")
        return final_response, all_messages
    else:
        if debug:
            print("Step 7: Model disapproved the response.")
        neg_str = "I'm unable to provide the information you're looking for. I'll connect you with a human representative for further assistance."
        return neg_str, all_messages


def voice_out(response):
    # Step 1: use voicerRSS text-to-speech api and Download the audio file
    url = f"http://api.voicerss.org/?key={rss_api_key}&hl=en-us&v=Amy&c=MP3&f=16khz_16bit_mono&src=" + response

    response = requests.get(url)
    # Check for a valid response
    if response.status_code == 200:
        # Step 2: Save the audio file
        filename = 'output.mp3'
        with open(filename, 'wb') as file:
            file.write(response.content)

        # Convert MP3 to WAV (simpleaudio only plays WAV files)
        from pydub import AudioSegment
        sound = AudioSegment.from_mp3(filename)
        filename_wav = 'output.wav'
        sound.export(filename_wav, format="wav")

        # Step 3: Play the audio file
        wave_obj = sa.WaveObject.from_wave_file(filename_wav)
        play_obj = wave_obj.play()
        play_obj.wait_done()

        # Step 4: Delete both audio files to save space
        os.remove(filename)
        os.remove(filename_wav)
    else:
        print(f'Failed to retrieve audio: {response.status_code}')


def record_audio(debug=True):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=480)

    vad = webrtcvad.Vad(1)  # Set aggressiveness mode, an integer between 0 and 3.
    frames = []
    silent_frames = 0
    if debug:
        print("Recording. Speak into the microphone...")

    while True:
        buf = stream.read(480)
        # Convert the byte data to an array of short integers
        is_speech = vad.is_speech(buf, 16000)

        frames.append(buf)  # Convert the array back to bytes before appending
        if not is_speech:
            silent_frames += 1
            if silent_frames > 30:  # If more than 20 consecutive silent frames, stop recording
                break
        else:
            silent_frames = 0
    if debug:
        print("Done recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio
    with wave.open('output.wav', 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))

    return 'output.wav'


def whisper_tts(audio_file_path, prompt=utils.whisper_prompt, debug=True):
    audio_file = open(audio_file_path, "rb")
    transcript = openai.Audio.translate("whisper-1", audio_file, prompt=prompt)
    if debug:
        print(transcript)
    return transcript['text']


def sound_input():
    # let user start conversation by hit enter button
    input()
    sound_file = record_audio()

    from pydub import AudioSegment
    sound = AudioSegment.from_wav(sound_file)
    filename_mp3 = 'input.mp3'
    sound.export(filename_mp3, format="mp3")

    transcript = whisper_tts(filename_mp3)
    os.remove(filename_mp3)
    return transcript


if __name__ == "__main__":
    context = [{'role': 'system', 'content': "You are Service Assistant"}]
    while 1:
        user_input = sound_input()
        # print("user say:", user_input)
        response, context = process_user_message(
            user_input, context, debug=False)
        print("===================")
        print(response)
        voice_out(response)
        print("===================")
        context.append({'role': 'assistant', 'content': f"{response}"})
