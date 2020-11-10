from Private import disk_helper as dh
key_1 = 'test_project/shell2/user1_var1'
key_2 = 'test_project/shell2/user1_var2'
data_location = "/tmp/cache"


def test_read_write_delete():
    dh.save_results(key_1, 5, location=data_location)
    assert dh.read_results(key_1, location=data_location) == 5


def test_get_matching_keys():
    dh.save_results(key_1, 5, location=data_location)
    dh.save_results(key_2, 6, location=data_location)
    matching_keys = dh.get_matching_keys('test_project/shell2/', location=data_location)
    assert len(matching_keys) == 2

