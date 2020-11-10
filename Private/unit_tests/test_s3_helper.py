from Private import s3_helper as s3h
test_redis_server_ip = 'localhost'
key_1 = 'test_project/shell2/user1_var1'
key_2 = 'test_project/shell2/user1_var2'
key_no_exist = 'test_project/shell5/user1_var2'
file_key = 'test_project/test_file'


def test_no_exist_file():
    assert s3h.if_exist(key_no_exist) == 0


def test_read_write_delete():
    s3h.save_results(key_1, 5)
    assert s3h.read_results(key_1) == 5
    assert s3h.if_exist(key_1) == 1


def test_get_matching_keys():
    s3h.save_results(key_1, 5)
    s3h.save_results(key_2, 6)
    matching_keys = s3h.get_matching_keys('test_project/shell2/')
    assert len(matching_keys) == 2


def test_read_file():
    file = s3h.read_file(file_key)
    assert file == b'test_content\n'
