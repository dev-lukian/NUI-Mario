import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
from . import constants as c
from . components import speech_states
from threading import Timer


class SpeechRecognizer:
    def __init__(self):
        load_dotenv()
    
        speech_config = speechsdk.SpeechConfig(subscription=os.getenv('SPEECH_KEY'), region=os.getenv('SPEECH_REGION'))

        speech_config.speech_recognition_language="en-US"
        speech_config.set_service_property('punctuation', 'explicit', speechsdk.ServicePropertyChannel.UriQueryParameter)
        speech_config.set_property(property_id=speechsdk.PropertyId.Speech_SegmentationSilenceTimeoutMs, value="300")

        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        self.recognizer = speech_recognizer
        self.recognizer.speech_start_detected.connect(self.handle_detected)
        self.recognizer.recognizing.connect(self.handle_recognizing)
        self.recognizer.recognized.connect(self.handle_recognized)
        self.recognizer.session_stopped.connect(self.handle_restart)

        self.all_events = []
        self.speech_state = speech_states.SpeechStates()


    def recognize(self):
        print('Listening for voice input')
        result = self.recognizer.recognize_once_async()

    def handle_detected(self, event):
        self.speech_state.state = c.LISTENING

    def handle_recognizing(self, event):
        self.speech_state.state = c.LOADING

    def handle_recognized(self, event):
        if event.result.text.lower() in c.COMMANDS:
            self.all_events.append([event.result.text.lower(), False])
            self.speech_state.state = c.RECOGNIZED
            print('Recognized voice input "%s"' % event.result.text.lower())
        else:
            self.speech_state.state = c.FAILED
            print('Voice input was not recognized')
        
        def changeState():
            self.speech_state.state = c.STAND_BY

        t = Timer(0.25, changeState)
        t.start()
    
    def handle_restart(self, event):
        t = Timer(0.1, self.recognize)
        t.start()


