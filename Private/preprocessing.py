import numpy as np
from scipy import spatial


def fft(file_itr, segment_size):
    """
    This method will concat all the files under a single iterator (coming from a event) and divide it by segment size,
    then calculate the fft for each segment. Takes a default segment size of 15 minutes

    :param file_itr: file iterator from the event
    :param segment_size: size of the segment
    :return: dict of fft arrays for each segment
    """
    output_length = 512
    file_arrays = []
    for count in range(0, file_itr.get_file_count()):
        byte_file = file_itr.next()
        str_file = np.fromstring(byte_file, dtype=np.float64).byteswap()
        file_arrays.append(str_file)
    complete_array = np.concatenate(file_arrays)
    x = complete_array[0:4 * np.floor_divide(complete_array.shape[0], 4)]
    x = x.reshape((np.divide(x.shape[0], 4), 4))
    time_stamps = (x[:, 3] - x[0, 3])/1000000000
    mag_sq = x[:, 0] * x[:, 0] + x[:, 1] * x[:, 1] + x[:, 2] * x[:, 2]
    if segment_size > 0:
        cut_points = []
        next_cut_value = segment_size
        for idx, val in enumerate(time_stamps):
            if val > next_cut_value:
                cut_points.append(idx)
                next_cut_value += segment_size
        segments = np.split(mag_sq, cut_points)
        output = {}
        for i, segment in enumerate(segments):
            spec = abs(np.fft.fft(np.sqrt(segment), output_length))[1:]
            output[segment_size*i] = spec.reshape((1, output_length - 1))
    else:
        spec = abs(np.fft.fft(np.sqrt(mag_sq), output_length))[1:]
        output = {0: spec.reshape((1, output_length - 1))}

    return output


def mfcc(file_itr):
    """
    Reshapes data in mfcc files
    :param file_itr: file iterator from the event
    :return: reshaped mfcc data
    """
    mfcc_size = 200 * 13
    mfcc_reshaped = np.empty([file_itr.get_file_count(), mfcc_size], dtype=np.float64)
    for count in range(0, file_itr.get_file_count()):
        byte_file = file_itr.next()
        str_file = np.fromstring(byte_file, dtype=np.float64).byteswap()
        mfcc_reshaped[count, :] = str_file.reshape((1, mfcc_size))
    mfcc_reshaped = mfcc_reshaped[~np.all(mfcc_reshaped == 0, axis=1)]
    return mfcc_reshaped


def calculate_similarity(vector1, vector2):
    return spatial.distance.cosine(vector1, vector2)
