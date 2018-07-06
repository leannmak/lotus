# lotus
[![Build Status](https://travis-ci.org/leannmak/lotus.svg?branch=master)](https://travis-ci.org/leannmak/lotus)
[![Coverage Status](https://coveralls.io/repos/github/leannmak/lotus/badge.svg?branch=master)](https://coveralls.io/github/leannmak/lotus?branch=master)  

Simple APIs for common open source tools such as `Ansible`, `Disconf`, `Etcd`, `Minio`, and etc. (c) 2018

## For Toolkit Users
### Setup

```shell
$ pip install git+https://github.com/leannmak/lotus.git
```

### Usage
```
# ansible 2.0
from lotus.api import Ansible2API

client = Ansible2API(
    hosts=['127.0.0.1'],
    passwords=dict(
        conn_pass='connection-password', become_pass='become-password'),
    connection='ssh',
    remote_user='root',
    verbosity=0,
    become=True,
    become_method='sudo',
    become_user='root',
    private_key_file='')
result = client.run(module='shell', args='echo "hello world"')


# disconf
from lotus.api import DisconfAPI

dapi = DisconfAPI(
    url='http://127.0.0.1:8080', user='your-name',
    password='your-password')
dapi.login()
result = dapi.env_list.get()


# etcd
from lotus.api import EtcdAPI

client = EtcdAPI(
    host='your-etcd-address', port=2379,
    cert=('etcd-client.crt', 'etcd-client-key.pem'),
    ca_cert='etcd-ca.crt', protocol='https',
    allow_reconnect=True)
client.connect()
result = client.read(key='/')


# minio
from lotus.api import MinioAPI

client = MinioAPI(
    endpoint='127.0.0.1:9000', access_key='your-access-key',
    secret_key='your-secret-key')
client.connect()
objects = client.list_objects(
    bucket_name='mybucket', prefix='myprefix', recursive=False)
```

## For Toolkit Developers

### Test

```
$ pip install tox
$ tox
```

### Setup

```shell
$ git clone https://github.com/leannmak/lotus.git
$ cd lotus
$ pip install -r requirements.txt
$ python setup.py install
```
