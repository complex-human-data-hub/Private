from Private import redis_helper as rh
test_redis_server_ip = 'localhost'
key_1 = 'test_project/shell2/user1_var1'
key_2 = 'test_project/shell2/user1_var2'


def test_get_redis_key():
    assert rh.get_redis_key('user1', 'var1') == 'proj1/shell1/user1_var1'
    assert rh.get_redis_key('user1', 'var1', 'test_project', 'shell2') == key_1


def test_get_project_id():
    assert rh.get_project_id(key_1) == 'test_project'


def test_read_write_delete():
    rh.save_results(key_1, 5, server_ip=test_redis_server_ip)
    assert rh.read_results(key_1, server_ip=test_redis_server_ip) == 5
    assert rh.if_exist(key_1, server_ip=test_redis_server_ip) == 1
    rh.delete_results(key_1, server_ip=test_redis_server_ip)
    assert rh.if_exist(key_1, server_ip=test_redis_server_ip) == 0


def test_delete_user_keys():
    rh.save_results(key_1, 5, server_ip=test_redis_server_ip)
    rh.save_results(key_2, 6, server_ip=test_redis_server_ip)
    rh.delete_user_keys('test_project', 'shell2', server_ip=test_redis_server_ip)
    assert rh.if_exist(key_1, server_ip=test_redis_server_ip) == 0
    assert rh.if_exist(key_2, server_ip=test_redis_server_ip) == 0
