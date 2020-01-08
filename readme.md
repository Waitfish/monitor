# Monitor from es
`Elastic stack` 中的 `Metricbeat` 会将系统数据放到 ES 中,但是 `Kibana`不能设置密码,而且无法实现报警功能.这个项目就是通过`python`的`requests`从`ES`中将需要的数据读出来,通过接口返回.

## run
```
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
