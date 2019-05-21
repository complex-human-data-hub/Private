import numpy as np
from scipy import spatial


def fft(file_itr):
    nfft = 512
    output = np.empty([file_itr.get_file_count(), nfft - 1], dtype=np.float64)
    for count in range(0, file_itr.get_file_count()):
        byte_file = file_itr.next()
        str_file = np.fromstring(byte_file, dtype=np.float64).byteswap()
        if str_file.shape[0] > 0:
            X = str_file[0:4 * np.floor_divide(str_file.shape[0], 4)]
            X = X.reshape((np.divide(X.shape[0], 4), 4))
            # todo: Reason behind cropping the input is not clear
            mag_sq = X[-nfft:, 0] * X[-nfft:, 0] + X[-nfft:, 1] * X[-nfft:, 1] + X[-nfft:, 2] * X[-nfft:, 2]
            spec = abs(np.fft.fft(np.sqrt(mag_sq), nfft))[1:]
            if sum(spec) > 0:
                output[count, :] = spec.reshape((1, nfft - 1))

    return output


def mfcc(file_itr):
    mfcc_size = 200 * 13
    mfcc = np.empty([file_itr.get_file_count(), mfcc_size], dtype=np.float64)
    for count in range(0, file_itr.get_file_count()):
        byte_file = file_itr.next()
        str_file = np.fromstring(byte_file, dtype=np.float64).byteswap()
        mfcc[count, :] = str_file.reshape((1, mfcc_size))
    mfcc = mfcc[~np.all(mfcc == 0, axis=1)]
    return mfcc


def calculate_similarity(vector1, vector2):
    return spatial.distance.cosine(vector1, vector2)

# from file_iterator import FileIterator
# AccelerometerData = ['DataFiles/accel_20190323021805Z_252b64e9-01ac-45c2-85af-91b5ea1dc40a.bin',
#                      'DataFiles/accel_20190323022821Z_b4d3807a-4802-4691-a243-4b0992e5df67.bin',
#                      'DataFiles/accel_20190323023913Z_31bc0ec8-87e1-4e3c-97aa-0da82fbcb50e.bin']
# AudioData = ['DataFiles/audio_20190323141540Z_dcf1df30-23c9-4f07-abbd-b2abecdce39d.mfcc',
#              'DataFiles/audio_20190323230637Z_a26b78d0-d1b9-47ee-946c-77ca1feb6246.mfcc',
#              'DataFiles/audio_20190323231714Z_c7231c2a-60c6-4ddf-bbf1-a04e71240a33.mfcc']
# GPSData = ['DataFiles/location_2def78e3-abf8-408a-9157-b703b7574e99.csv',
#            'DataFiles/location_2e19c2c6-4815-4c67-9d56-8e062f5f6dd9.csv',
#            'DataFiles/location_3acd4064-8619-42f1-b0e6-84b30391ab13.csv']
# y = FileIterator(AudioData)
# fft_array = mfcc(y)
# print fft_array
# print calculate_similarity(fft_array[1], fft_array[0])
# print calculate_similarity(fft_array[1], fft_array[1])
