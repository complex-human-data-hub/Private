from datetime import timedelta

import numpy as np
from scipy import spatial


def fft(file_itr, segment_size):
    """
    This method will concat all the files under a single iterator (coming from a event) and divide it by segment size,
    then calculate the fft for each segment
    :param file_itr: file iterator from the event
    :param segment_size: size of the segment
    :return: dict of fft arrays for each segment
    """
    '''
    todo - Finalize on the segment start point (start of the file or start of the hour?)
    todo - Timestamp is from the uptime. And if we know the exact time of the first event we can estimate time for all 
    events. However, there is no way find that. We can estimate the first event time from the file name, which can be 
    wrong. Going forward we might need to change the code from the android application end.
    '''
    output_length = 512
    file_arrays = []
    file_datetime = file_itr.get_file_datetime()
    for count in range(0, file_itr.get_file_count()):
        byte_file = file_itr.next()
        str_file = np.fromstring(byte_file, dtype=np.float64).byteswap()
        file_arrays.append(str_file)
    complete_array = np.concatenate(file_arrays)
    X = complete_array[0:4 * np.floor_divide(complete_array.shape[0], 4)]
    X = X.reshape((np.divide(X.shape[0], 4), 4))
    time_stamps = (X[:, 3] - X[0, 3])/1000000000
    cut_points = []
    next_cut_value = segment_size
    for idx, val in enumerate(time_stamps):
        if val > next_cut_value:
            cut_points.append(idx)
            next_cut_value += segment_size

    mag_sq = X[:, 0] * X[:, 0] + X[:, 1] * X[:, 1] + X[:, 2] * X[:, 2]
    segments = np.split(mag_sq, cut_points)
    output = {}
    for i, segment in enumerate(segments):
        spec = abs(np.fft.fft(np.sqrt(segment), output_length))[1:]
        output[str(file_datetime + timedelta(seconds=segment_size*i))] = spec.reshape((1, output_length - 1))

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
# AccelerometerData = ['DataFiles/accel_20190323022821Z_b4d3807a-4802-4691-a243-4b0992e5df67.bin',
#                      'DataFiles/accel_20190323021805Z_252b64e9-01ac-45c2-85af-91b5ea1dc40a.bin',
#                      'DataFiles/accel_20190323023913Z_31bc0ec8-87e1-4e3c-97aa-0da82fbcb50e.bin']
# AudioData = ['DataFiles/audio_20190323141540Z_dcf1df30-23c9-4f07-abbd-b2abecdce39d.mfcc',
#              'DataFiles/audio_20190323230637Z_a26b78d0-d1b9-47ee-946c-77ca1feb6246.mfcc',
#              'DataFiles/audio_20190323231714Z_c7231c2a-60c6-4ddf-bbf1-a04e71240a33.mfcc']
# GPSData = ['DataFiles/location_2def78e3-abf8-408a-9157-b703b7574e99.csv',
#            'DataFiles/location_2e19c2c6-4815-4c67-9d56-8e062f5f6dd9.csv',
#            'DataFiles/location_3acd4064-8619-42f1-b0e6-84b30391ab13.csv']
# y = FileIterator(AccelerometerData)
# fft_array = fft_v2(y, 300)
# print fft_array
# print calculate_similarity(fft_array[1], fft_array[0])
# print calculate_similarity(fft_array[1], fft_array[1])
