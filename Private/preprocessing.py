import numpy as np
from scipy import spatial
from datetime import datetime, timedelta


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


def zip_date(lists, keys, max_distances, keep_unmatched=True):
    zipped_list = {}
    dt_format = '%Y-%m-%d %H:%M:%S'

    main_list = lists[0]
    if isinstance(keys, list):
        main_date_key = keys[0]
    else:
        main_date_key = keys
    main_list.sort(key=lambda r: datetime.strptime(r[main_date_key], dt_format))
    secondary_lists = lists[1:]
    for secondary_id, secondary_list in enumerate(secondary_lists):
        if isinstance(keys, list):
            secondary_date_key = keys[secondary_id]
        else:
            secondary_date_key = keys
        secondary_list.sort(key=lambda r: datetime.strptime(r[secondary_date_key], dt_format))
        if isinstance(max_distances, list):
            max_distance = max_distances[secondary_id]
        else:
            max_distance = max_distances
        max_distance_time = timedelta(**{max_distance[0]: max_distance[1]})
        before_key = 0
        after_key = 1
        time_before = datetime.strptime(secondary_list[before_key][secondary_date_key], dt_format)
        time_after = datetime.strptime(secondary_list[after_key][secondary_date_key], dt_format)
        for main_id, main_item in enumerate(main_list):
            if secondary_id == 0:
                zipped_list[main_id] = [main_item]
            item_time = datetime.strptime(main_item[main_date_key], dt_format)
            item_added = False
            while not item_added:
                # if list 2 is over (time_after will be None) then we will group everything else in list 1 with the last
                # item in list 2
                item_added = True
                if time_after is None:
                    if time_before - item_time <= max_distance_time:
                        zipped_list[main_id].append(secondary_list[before_key])
                # item below and after both is greater than the item time, this mean below should be the closest one
                elif item_time <= time_before:
                    if time_before - item_time <= max_distance_time:
                        zipped_list[main_id].append(secondary_list[before_key])
                # if item time is between time before and time after, then one of these should be the closest one
                elif time_before <= item_time <= time_after:
                    if item_time - time_before > time_after - item_time:
                        if time_after - item_time <= max_distance_time:
                            zipped_list[main_id].append(secondary_list[after_key])
                    else:
                        if item_time - time_before <= max_distance_time:
                            zipped_list[main_id].append(secondary_list[before_key])
                # if both below and after is less than the item time we need to increase the pointer positions
                else:
                    item_added = False
                    before_key += 1
                    after_key += 1
                    # we might go off the array if list 2 is over, so check fo the length
                    if after_key < len(secondary_list):
                        time_before = datetime.strptime(secondary_list[before_key][secondary_date_key], dt_format)
                        time_after = datetime.strptime(secondary_list[after_key][secondary_date_key], dt_format)
                    else:
                        time_before = datetime.strptime(secondary_list[before_key][secondary_date_key], dt_format)
                        time_after = None
    zipped_tuple_list = []
    for main_id in zipped_list:
        tup = tuple(zipped_list[main_id])
        if (keep_unmatched or len(tup)>1):
            zipped_tuple_list.append(tup)

    return zipped_tuple_list

