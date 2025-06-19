import speech_recognition as sr
from gtts import gTTS
import tempfile
import os

# Initialize recognizer globally
recognizer = sr.Recognizer()

def capture_audio(language_code="bn-BD"):
    """
    Capture audio from the microphone and return the transcribed text.
    :param language_code: Language code (default is Bengali - bn-BD)
    :return: Transcribed text or None in case of failure
    """
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=15)
            text = recognizer.recognize_google(audio, language=language_code)
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

def transcribe_audio_file(file_path, language_code="bn-BD"):
    """
    Transcribe audio from a file and return the transcribed text.
    :param file_path: Path to the audio file
    :param language_code: Language code (default is Bengali - bn-BD)
    :return: Transcribed text or None in case of failure
    """
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language=language_code)
        return text
    except sr.UnknownValueError:
        print("Could not understand the audio in the file.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def speak_bengali_text(text, delete_after_use=True):
    """
    Convert Bengali text to speech and save it as an mp3 file.
    :param text: Text to be spoken in Bengali
    :param delete_after_use: Boolean to decide whether to delete the temporary file after use
    :return: Path to the temporary mp3 file
    """
    try:
        tts = gTTS(text=text, lang='bn')
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        
        # Optionally delete the file after it's used
        if delete_after_use:
            temp_file.close()  # Close the temp file to allow deletion later
            os.remove(temp_file.name)  # Delete the file after it's used

        return temp_file.name
    except Exception as e:
        print(f"An error occurred while generating speech: {e}")
        return None
