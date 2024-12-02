import librosa
import librosa.display
import matplotlib.pyplot as plt

audio_file = 'LiVsAustin.mp4'
y, sr = librosa.load(audio_file)

spectrogram = librosa.stft(y)
spectrogram_db = librosa.amplitude_to_db(abs(spectrogram))

plt.figure(figsize=(10, 4))
librosa.display.specshow(spectrogram_db, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Sonogram')
plt.tight_layout()
plt.show()