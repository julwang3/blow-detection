import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import sounddevice as sd

# Settings
SAMPLE_RATE = 44100  # Audio sampling rate (44.1 kHz)
DURATION = 5         # Duration of audio capture in seconds
LOWCUT = 20.0        # Low frequency for bandpass filter
HIGHCUT = 300.0      # High frequency for bandpass filter
CHANNELS = 1         # Mono
RMS_THRESHOLD = 1

def bandpass_filter(audio_data, order=3):
    audio_data = audio_data[:, 0]
    nyquist = 0.5 * SAMPLE_RATE
    low = LOWCUT / nyquist
    high = HIGHCUT / nyquist

    b, a = butter(order, [low, high], btype='bandpass')
    y = filtfilt(b, a, audio_data)  # Zero-phase filter
    return y

def fft(audio_data, is_plot = True):
    # Perform FFT
    fft_result = np.fft.fft(audio_data)
    frequencies = np.fft.fftfreq(len(audio_data), 1 / SAMPLE_RATE)
    magnitude = np.abs(fft_result)

    # Check if plot
    if is_plot:
        plot_fft_data(frequencies, magnitude)

    return magnitude

def spectral_flatness(fft_magnitude):
    # Calculate spectral flatness
    geometric_mean = np.exp(np.mean(np.log(fft_magnitude + 1e-10)))
    arithmetic_mean = np.mean(fft_magnitude)
    return geometric_mean / (arithmetic_mean + 1e-10)

def calculate_rms(data):
    # Calculate the Root Mean Square of the signal
    return np.sqrt(np.mean(data**2))

def plot_data(audio_data):
    # Create a time array based on the number of samples
    time = np.linspace(0, DURATION, len(audio_data))

    # Plot the audio data
    plt.subplot(1, 2, 1)
    plt.plot(time, audio_data)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.title('Audio Data')

def plot_fft_data(frequencies, magnitude):
    # Plot the fft data to visualize
    plt.subplot(1, 2, 2)
    plt.plot(frequencies, magnitude)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.title('Audio Data - FFT')
    plt.xlim((0, 500))


def main():
    # Select blow detection mode
    mode = -1
    while mode != 1 and mode != 2:
        print('-----------------------------------')
        print('Menu:')
        print('1. Continuous Blow Detection')
        print('2. Single Blow Detection and Graph')
        print('-----------------------------------')
        
        try:
            mode = int(input('\nSelect a blow detection mode: '))
            if mode != 1 and mode != 2:
                print("Enter a valid integer!\n")
        except ValueError:
            print("Enter an integer!\n")

    ### 1. Continuous Blow Detection ###
    if mode == 1:
        DURATION = 0.05
        print(f'Blow Detection (RMS) Threshold = {RMS_THRESHOLD:.4f}')
        
        try:
            while True:
                # Record audio data
                audio_data = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='float64')
                sd.wait()  # Wait until the recording is finished

                plot_data(audio_data)

                # Apply bandpass filter to isolate low frequencies of blowing
                audio_data = bandpass_filter(audio_data)

                # Perform FFT
                frequency_magnitudes = fft(audio_data)

                # Detect blow
                rms = calculate_rms(frequency_magnitudes)
                if rms > RMS_THRESHOLD:
                    print(f'Blow detected! RMS: {rms:.4f}')
                else:
                    print(f'RMS: {rms:.4f}')
        
        except KeyboardInterrupt:
            print('Interrupt detected!')
    
    ### 2. Single Blow Detection and Graph ###
    elif mode == 2:
        DURATION = int(input('Enter blow duration in seconds: '))

        # Record audio data
        print(f"Recording for {DURATION} seconds...")
        audio_data = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='float64')
        sd.wait()  # Wait until the recording is finished
        print("Recording complete.")

        # Plot and perform FFT before applying filter
        plot_data(audio_data)
        fft(audio_data)

        # Apply bandpass filter to isolate low frequencies of blowing
        audio_data = bandpass_filter(audio_data)

        # Plot and perform FFT after applying filter
        plot_data(audio_data)
        fft(audio_data)
        plt.show()

if __name__ == "__main__":
    main()
