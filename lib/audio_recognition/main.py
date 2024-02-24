'''
This is just some calculation to look for some possibilities
'''




import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import librosa
from scipy.signal import correlate
import time

# Initialize PyAudio
p = pyaudio.PyAudio()

# Audio stream parameters
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024


def load_and_preprocess_audio(file_path):
    audio, sr = librosa.load(file_path, sr=None, mono=True)
    return audio, sr

def extract_features(audio, sr):
    # Extracting MFCCs or spectrogram
    features = librosa.feature.mfcc(y=audio, sr=sr)
    return features

def match_template(live_features, chime_features):
    # Perform normalized cross-correlation and ensure it's in the same length as live_features
    correlation = correlate(chime_features.flatten(), live_features.flatten(), mode='full', method='fft')
    correlation = correlation / np.max(correlation)  # Normalizing the correlation
    
    return correlation

def detect_chime(live_audio_path, chime_audio_path):
    live_audio, sr_live = load_and_preprocess_audio(live_audio_path)
    chime_audio, sr_chime = load_and_preprocess_audio(chime_audio_path)
    
    # Ensure both audio clips are at the same sample rate
    assert sr_live == sr_chime, "Sample rates do not match!"
    
    # live_features = extract_features(live_audio, sr_live)
    # chime_features = extract_features(chime_audio, sr_chime)
    # Esegui la correlazione cross-spettrale
    # Inizia a misurare il tempo
    start_time = time.perf_counter_ns()

    correlation = correlate(live_audio, chime_audio, mode='full')
    # Trova il picco di correlazione
    max_corr_index = np.argmax(correlation)
    
    # Converti l'indice di picco in tempo
    max_corr_time = (max_corr_index - len(chime_audio) + 1) / sr_live
    # Thresholding for detection
    max_corr_value = np.max(correlation)
    # Termina la misurazione del tempo
    end_time = time.perf_counter_ns()

    # Calcola il tempo di esecuzione in microsecondi
    execution_time_microseconds = (end_time - start_time) / 1000
    print(f"Il tempo di esecuzione è {execution_time_microseconds} microsecondi.")
    if max_corr_value > 0.1:
        print(f"Highest correlation is at {max_corr_time} seconds with a value of {max_corr_value}")
        # Trigger action here

    # Calculate the starting sample index for the chime
    start_sample_index = int(max_corr_time * sr_live)

    # Create a time axis for the live audio
    time_axis_live = np.linspace(0, len(live_audio) / sr_live, num=len(live_audio))

    # Create a time axis for the chime, starting from start_time_seconds
    time_axis_chime = np.linspace(max_corr_time, max_corr_time + len(chime_audio) / sr_live, num=len(chime_audio))

    # Plotting
    plt.figure(figsize=(14, 6))
    plt.plot(time_axis_live, live_audio, label='Live Audio')
    plt.plot(time_axis_chime, chime_audio, label='Chime', alpha=0.7)  # Alpha for slight transparency
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.title('Live Audio and Chime Alignment')
    plt.legend()
    plt.show()


detect_chime("./extracted_audio.wav", "cut_audio.wav")

'''
# Function to process live audio
def process_live_audio(chime_features, sr):
    def callback(in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        
        # Feature extraction (simplified)
        live_features = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13)
        
        # Simplified matching (for demonstration)
        # In practice, use a more sophisticated approach for matching
        match = np.correlate(live_features.flatten(), chime_features.flatten())
        
        print(np.max(match))
        if np.max(match) > 0.1:
            print("Chime detected!")
            # Trigger action here
        
        return (in_data, pyaudio.paContinue)
    
    return callback

# Load and preprocess chime audio
chime_audio, sr_chime = load_and_preprocess_audio('./cut_audio.wav')
chime_features = extract_features(chime_audio, sr_chime)

# Open the stream and start processing
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=process_live_audio(chime_features, RATE))

stream.start_stream()

# Keep the stream open and processing
try:
    while stream.is_active():
        # You can place any real-time monitoring or additional logic here
        pass
except KeyboardInterrupt:
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
'''