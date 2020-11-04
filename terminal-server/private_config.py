import os
# If running locally, there is no need 
# for this protection 
USE_CSRF = False

SECRET_KEY = os.urandom(24)
private_host = 'private_server' # localhost, private_server (docker), FQDN
private_port = 51135
private_project_id = '999-999-999' # Fake data
certfile = 'server.crt'

