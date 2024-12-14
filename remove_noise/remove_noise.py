import numpy as np
import scipy.io.wavfile as wav
import matplotlib
matplotlib.use('TkAgg')  # 使用TkAgg后端，这个后端适用于生成图像文件
import matplotlib.pyplot as plt
import scipy.signal as signal
import os


def load_audio(file_path):
    """
    加载音频文件
    """
    rate, data = wav.read(file_path)
    if data.ndim > 1:
        data = data[:, 0]  # 如果是立体声，选择左声道
    return rate, data


def plot_frequency_spectrum(data, rate, title="Frequency Spectrum"):
    """
    绘制频谱图
    """
    fft_data = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(data), 1 / rate)
    magnitude = np.abs(fft_data)

    plt.figure(figsize=(10, 6))
    plt.plot(freqs[:len(freqs) // 2], magnitude[:len(magnitude) // 2])
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.show()


def apply_fft_filter(data, rate, threshold=1000, filter_type='low'):
    """
    使用傅里叶变换去除噪声（低通或高通滤波）
    """
    fft_data = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(data), 1 / rate)

    # 选择滤波类型
    if filter_type == 'low':
        fft_data[np.abs(freqs) > threshold] = 0
    elif filter_type == 'high':
        fft_data[np.abs(freqs) < threshold] = 0
    else:
        raise ValueError("filter_type should be 'low' or 'high'")

    denoised_data = np.fft.ifft(fft_data)
    return np.real(denoised_data)


def bandpass_filter(data, rate, lowcut=300, highcut=3000):
    """
    使用带通滤波器去除不需要的低频和高频噪声
    """
    nyquist = 0.5 * rate
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = signal.butter(4, [low, high], btype='band')
    filtered_data = signal.filtfilt(b, a, data)
    return filtered_data


def noise_gate_filter(data, rate, noise_threshold=0.02):
    """
    频谱门控方法，去除幅度小于噪声阈值的频率成分
    """
    fft_data = np.fft.fft(data)
    magnitude = np.abs(fft_data)
    phase = np.angle(fft_data)

    # 应用噪声门限
    fft_data[magnitude < noise_threshold] = 0
    denoised_data = np.fft.ifft(fft_data)
    return np.real(denoised_data)


def compute_dynamic_threshold(data, rate):
    """
    动态计算阈值来适应不同频段的噪声强度
    """
    fft_data = np.fft.fft(data)
    magnitude = np.abs(fft_data)

    mean_magnitude = np.mean(magnitude)
    threshold = mean_magnitude * 0.5  # 使用平均值的50%作为阈值
    return threshold


def adaptive_noise_reduction(data, rate):
    """
    自适应噪声减少方法
    """
    threshold = compute_dynamic_threshold(data, rate)
    fft_data = np.fft.fft(data)
    magnitude = np.abs(fft_data)
    phase = np.angle(fft_data)

    # 去除低于动态阈值的频率成分
    fft_data[magnitude < threshold] = 0
    denoised_data = np.fft.ifft(fft_data)
    return np.real(denoised_data)


def save_audio(file_path, data, rate):
    """
    保存去噪后的音频到文件
    """
    wav.write(file_path, rate, data.astype(np.int16))


def plot_audio_waveform(data, rate, title="Audio Waveform"):
    """
    绘制音频波形图
    """
    time = np.arange(0, len(data)) / rate
    plt.figure(figsize=(10, 6))
    plt.plot(time, data)
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.show()


def compare_audio_files(file1, file2, rate1, rate2):
    """
    比较两个音频文件
    """
    data1, data2 = None, None
    if file1 and os.path.exists(file1):
        rate1, data1 = load_audio(file1)
    if file2 and os.path.exists(file2):
        rate2, data2 = load_audio(file2)

    if data1 is not None:
        plot_audio_waveform(data1, rate1, "Original Audio")
    if data2 is not None:
        plot_audio_waveform(data2, rate2, "Processed Audio")


def main():
    """
    主程序，演示不同的去噪技术
    """
    file_path = 'noisy_audio.wav'  # 需要去噪的音频文件
    rate, data = load_audio(file_path)

    # 绘制原始音频的频谱图
    plot_frequency_spectrum(data, rate, "Original Frequency Spectrum")

    # 使用傅里叶变换去噪（低通滤波）
    denoised_data_low = apply_fft_filter(data, rate, threshold=1000, filter_type='low')
    save_audio('denoised_audio_low.wav', denoised_data_low, rate)

    # 使用带通滤波器去噪
    denoised_data_bandpass = bandpass_filter(data, rate, lowcut=300, highcut=3000)
    save_audio('denoised_audio_bandpass.wav', denoised_data_bandpass, rate)

    # 使用频谱门控去噪
    denoised_data_gate = noise_gate_filter(data, rate, noise_threshold=0.02)
    save_audio('denoised_audio_gate.wav', denoised_data_gate, rate)

    # 使用自适应噪声减少去噪
    denoised_data_adaptive = adaptive_noise_reduction(data, rate)
    save_audio('denoised_audio_adaptive.wav', denoised_data_adaptive, rate)

    # 绘制去噪后的音频波形图
    compare_audio_files('noisy_audio.wav', 'denoised_audio_low.wav', rate, rate)
    compare_audio_files('noisy_audio.wav', 'denoised_audio_bandpass.wav', rate, rate)
    compare_audio_files('noisy_audio.wav', 'denoised_audio_gate.wav', rate, rate)
    compare_audio_files('noisy_audio.wav', 'denoised_audio_adaptive.wav', rate, rate)


if __name__ == "__main__":
    main()
