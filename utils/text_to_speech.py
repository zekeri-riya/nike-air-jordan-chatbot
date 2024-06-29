from gtts import gTTS
import pygame

pygame.mixer.init()

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    # Wait until the sound has finished playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up
    pygame.mixer.music.stop()
