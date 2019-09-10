import math
from collections import OrderedDict

import numpy as np
from scipy import spatial
from datetime import timedelta
from dateutil.parser import parse


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
    file_itr.reset()
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
    file_itr.reset()
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
    """
    Merge 2 or more events list based on the time. Close events will be merged to a tuple and will compose a list of
    tuples of such events.

    :param lists: list of event lists
    :param keys: list of keys / single key (each key points to the date time attribute in the object)
    :param max_distances: max distance from main event list events to events in other list
    :param keep_unmatched: If the item in list 1 doesn't have a close event in any of the list, we can decide if we
    need to keep it in the output list with this flag
    :return: list of tuples, tuple will have close events from different lists
    """
    zipped_list = OrderedDict()

    main_list = lists[0]
    if isinstance(keys, list):
        main_date_key = keys[0]
    else:
        main_date_key = keys
    main_list.sort(key=lambda r: parse(getattr(r, main_date_key)))
    secondary_lists = lists[1:]
    for secondary_id, secondary_list in enumerate(secondary_lists):
        if isinstance(keys, list):
            secondary_date_key = keys[secondary_id]
        else:
            secondary_date_key = keys
        secondary_list.sort(key=lambda r: parse(getattr(r, secondary_date_key)))
        if isinstance(max_distances, list):
            max_distance = max_distances[secondary_id]
        else:
            max_distance = max_distances
        max_distance_time = timedelta(**{max_distance[0]: max_distance[1]})
        before_key = 0
        after_key = 1
        time_before = parse(getattr(secondary_list[before_key], secondary_date_key))
        time_after = parse(getattr(secondary_list[after_key], secondary_date_key))
        for main_id, main_item in enumerate(main_list):
            if secondary_id == 0:
                zipped_list[main_id] = [main_item]
            item_time = parse(getattr(main_item, main_date_key))
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
                        time_before = parse(getattr(secondary_list[before_key], secondary_date_key))
                        time_after = parse(getattr(secondary_list[after_key], secondary_date_key))
                    else:
                        time_before = parse(getattr(secondary_list[before_key], secondary_date_key))
                        time_after = None
    zipped_tuple_list = []
    for main_id in zipped_list:
        tup = tuple(zipped_list[main_id])
        if keep_unmatched or len(tup) > 1:
            zipped_tuple_list.append(tup)

    return zipped_tuple_list


def bucket_date(lists, keys, time_interval, bucket_start_str=None, keep_empty_buckets=False):
    """
    merge multiple lists in to a single list of tuples. This create buckets from the start time with given interval.
    If the start time is not give it takes the start of that time interval.

    :param lists: list of lists
    :param keys: list of keys, or single key
    :param time_interval: time interval as a list
    :param bucket_start_str: start time
    :param keep_empty_buckets: whether to keep empty buckets in the output
    :return: list of tuples
    """
    bucketed_list = OrderedDict()
    time_granularities = [("microseconds", 0), ("seconds", 0), ("minutes", 0), ("hours", 0), ("days", 1)]
    time_truncate = {}
    for time_granularity in time_granularities:
        time_truncate[time_granularity[0][:-1]] = time_granularity[1]
        if time_interval[0] == time_granularity[0]:
            break

    # sort all lists
    total_items = 0
    if not isinstance(keys, list):
        keys = [keys] * len(lists)
    for list_id, event_list in enumerate(lists):
        event_list.sort(key=lambda r: parse(getattr(r, keys[list_id])))
        total_items += len(event_list)

    # find minimum date
    min_date = parse(getattr(lists[0][0], keys[0]))
    for list_id, event_list in enumerate(lists):
        temp_date = parse(getattr(event_list[0], keys[list_id]))
        if temp_date < min_date:
            min_date = temp_date

    # Start bucketing
    lists_bucketed = False
    if bucket_start_str is None:
        bucket_start = min_date.replace(**time_truncate)
    else:
        bucket_start = parse(bucket_start_str)
    bucketed_list[bucket_start] = []
    counts = [0] * len(lists)
    bucket_length = timedelta(**{time_interval[0]: time_interval[1]})
    while not lists_bucketed:
        for list_id, event_list in enumerate(lists):
            item_added = True
            while item_added and counts[list_id] < len(event_list):
                temp_date = parse(getattr(event_list[counts[list_id]], keys[list_id]))
                item_added = False
                if bucket_start <= temp_date < bucket_start + bucket_length:
                    bucketed_list[bucket_start].append(event_list[counts[list_id]])
                if temp_date < bucket_start + bucket_length:
                    counts[list_id] += 1
                    item_added = True
        if sum(counts) == total_items:
            lists_bucketed = True

        # if there are no items added this round we move to next bucket
        if len(bucketed_list[bucket_start]) == 0 and not keep_empty_buckets:
            bucketed_list.pop(bucket_start)
        if not lists_bucketed:
            bucket_start = bucket_start + bucket_length
            bucketed_list[bucket_start] = []

    bucketed_tuple_list = []
    for bucket_start in bucketed_list:
        bucketed_tuple_list.append(tuple(bucketed_list[bucket_start]))

    return bucketed_tuple_list


def all_pair_euclidean_distance(vector_dict1, vector_dict2):
    """
    It can be used to calculate the all pair euclidean distance between two list of vectors. This will return a
    distribution of the distances.

    :param vector_dict1: vector dict/array one
    :param vector_dict2: vector dict/array two
    :return: list of distances
    """
    hist = []
    if isinstance(vector_dict1, dict) and isinstance(vector_dict2, dict):
        vector_list1 = vector_dict1.values()
        vector_list2 = vector_dict2.values()
    elif isinstance(vector_dict1, np.ndarray) and isinstance(vector_dict2, np.ndarray):
        vector_list1 = vector_dict1
        vector_list2 = vector_dict2
    else:
        raise Exception("Incompatible types" + str(type(vector_dict1)))

    for v1 in vector_list1:
        for v2 in vector_list2:
            hist.append(np.linalg.norm(v1 - v2))
    return hist


def euclidean_distance(v1, v2):
    """
    It can be used to calculate the euclidean distance between two vectors.

    :param v1: vector one
    :param v2: vector two
    :return: distance
    """
    return np.linalg.norm(v1 - v2)


def degrees_to_radians(degrees):
    return degrees * math.pi / 180


def get_distance_km(lat1, lon1, lat2, lon2):
    """
    This return the distance between two location on earth in kilo meters
    :param lat1: latitude of location 1
    :param lon1: longitude of location 1
    :param lat2: latitude of location 2
    :param lon2: latitude of location 2
    :return: distance as a float
    """
    earth_radius_km = 6371
    d_lat = degrees_to_radians(lat2-lat1)
    d_lon = degrees_to_radians(lon2-lon1)
    lat1 = degrees_to_radians(lat1)
    lat2 = degrees_to_radians(lat2)
    a = math.sin(d_lat/2) * math.sin(d_lat/2) + math.sin(d_lon/2) * math.sin(d_lon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return earth_radius_km * c


def get_all_pair_loc_distance(loc_list1, loc_list2):
    """
    Return the all pair location distribution of 2 location traces. Locations are found as list of dictionaries

    :param loc_list1: list of dictionaries with location information
    :param loc_list2: list of dictionaries with location information
    :return: location distribution list
    """
    hist = []
    for l1 in loc_list1:
        for l2 in loc_list2:
            hist.append(get_distance_km(l1['lat'], l1['lon'], l2['lat'], l2['lon']))
    return hist
