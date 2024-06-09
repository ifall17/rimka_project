import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import wavio
import numpy as np

# Function to transcribe speech
def transcribe_speech(api, language):
    r = sr.Recognizer()

    try:
        import pyaudio
    except Exception as e:
        st.error(f"PyAudio installation issue: {e}")
        return f"PyAudio installation issue: {e}"

    try:
        with sr.Microphone() as source:
            st.info("Speak now...")
            r.adjust_for_ambient_noise(source)
            audio_text = r.listen(source)
            st.info("Audio captured, transcribing...")

            try:
                if api == "Google":
                    text = r.recognize_google(audio_text, language=language)
                elif api == "Sphinx":
                    text = r.recognize_sphinx(audio_text, language=language)
                else:
                    return "Selected API not supported."
                return text
            except sr.UnknownValueError:
                return "Sorry, I did not understand the audio."
            except sr.RequestError as e:
                return f"Could not request results from {api} service; {e}"
            except Exception as e:
                return f"An error occurred during transcription: {e}"
    except Exception as e:
        st.error(f"Microphone access issue: {e}")
        return f"Microphone access issue: {e}"

# Main function
def main():
    st.title("Speech Recognition App")
    st.write("Click on the microphone to start speaking, and click again to stop:")

    # Initialize session state variables
    if 'recording' not in st.session_state:
        st.session_state.recording = False
    if 'transcription' not in st.session_state:
        st.session_state.transcription = ""

    # Select API
    api = st.selectbox("Select Speech Recognition API", ["Google", "Sphinx"])

    # Select language
    language = st.text_input("Enter language code (e.g., 'en-US' for English, 'es-ES' for Spanish):", "en-US")

    # Button to start/stop recording
    if st.button("Start/Stop Recording"):
        if st.session_state.recording:
            st.session_state.recording = False
            st.session_state.transcription = transcribe_speech(api, language)
        else:
            st.session_state.recording = True

    # Display the transcription
    if not st.session_state.recording and st.session_state.transcription:
        st.write("Transcription: ", st.session_state.transcription)
        if st.button("Save Transcription"):
            with open("transcription.txt", "w") as f:
                f.write(st.session_state.transcription)
            st.success("Transcription saved to transcription.txt")

if __name__ == "__main__":
    main()





