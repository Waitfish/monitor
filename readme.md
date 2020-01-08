# Monitor from es
`Elastic stack` 中的 `Metricbeat` 会将系统数据放到 ES 中,但是 `Kibana`不能设置密码,而且无法实现报警功能.这个项目就是通过`python`的`requests`从`ES`中将需要的数据读出来,通过接口返回.

## run
```
export ES_URL=http://10.x.x.x:9200
pip install -r requirements.txt
python index.py
```
默认监听`5000`端口

## docker
### dockerfile
覆盖 `ES_URL`,修改为自己的 `ES` 地址
```dockerfile
FROM python:3.6-alpine

EXPOSE 5000
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV ES_URL http://127.0.0.1:9200

CMD [ "python", "./index.py" ]
```

## API
### 根据硬盘剩余百分比查询
```bash
curl -H "Content-type: application/json" -X POST -d '{"warn":0.7}' x.x.x.88:5000/hdbypct                                                 
```
```json
{"data":[{"doc_count":2,"key":"Log-Server-x.x.x.88","mountpoint":{"buckets":[{"doc_count":2,"key":"/","mount_pec":{"buckets":[{"doc_count":2,"key":0.902}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}},{"doc_count":1,"key":"BigData001-x.x.x.124","mountpoint":{"buckets":[{"doc_count":1,"key":"/var/www/html/yum","mount_pec":{"buckets":[{"doc_count":1,"key":1.0}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}},{"doc_count":1,"key":"DB-Link-x.x.x.82","mountpoint":{"buckets":[{"doc_count":1,"key":"/","mount_pec":{"buckets":[{"doc_count":1,"key":0.895}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}},{"doc_count":1,"key":"Java-sunyard-x.x.x.99","mountpoint":{"buckets":[{"doc_count":1,"key":"/boot","mount_pec":{"buckets":[{"doc_count":1,"key":0.764}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}},{"doc_count":1,"key":"MQ-sunyard-x.x.x.16","mountpoint":{"buckets":[{"doc_count":1,"key":"/boot","mount_pec":{"buckets":[{"doc_count":1,"key":0.764}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}},{"doc_count":1,"key":"MariaDB-x.x.x.105","mountpoint":{"buckets":[{"doc_count":1,"key":"/","mount_pec":{"buckets":[{"doc_count":1,"key":0.704}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}},{"doc_count":1,"key":"Minio-x.x.x.121","mountpoint":{"buckets":[{"doc_count":1,"key":"/boot","mount_pec":{"buckets":[{"doc_count":1,"key":0.764}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}},{"doc_count":1,"key":"Outside-x.x.x.180","mountpoint":{"buckets":[{"doc_count":1,"key":"/","mount_pec":{"buckets":[{"doc_count":1,"key":0.839}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}},{"doc_count":1,"key":"UAT-x.x.x.162","mountpoint":{"buckets":[{"doc_count":1,"key":"/boot","mount_pec":{"buckets":[{"doc_count":1,"key":0.741}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}}],"status_code":200}
```

### 根据硬盘剩余容量(bytes)查询
```bash
curl -H "Content-type: application/json" -X POST -d '{"bytes":5368709120}' x.x.x.88:5000/hdbybyte                                                
```
```json
{"data":[{"doc_count":2,"key":"Log-Server-x.x.x.88","mountpoint":{"buckets":[{"doc_count":2,"key":"/","mount_free":{"buckets":[{"doc_count":1,"key":5143040000},{"doc_count":1,"key":5162508288}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}}],"doc_count_error_upper_bound":0,"sum_other_doc_count":0}}],"status_code":200}
```