import requests
import json
import os
import sys
from flask import Flask, abort, request, jsonify

env_dist = os.environ
ES_URL = env_dist.get("ES_URL")
if ES_URL:
    URL = ES_URL + "/_search"
else:
    print("Please set the elasticsearch uri in env by ES_URL")
    sys.exit(0)

# 根据百分比查询s
query_by_pct = {
    "_source": ["system.filesystem.used.pct", "system.filesystem.available", "system.filesystem.total",
                "system.filesystem.mount_point", "host.name"],
    "query": {
        "bool": {
            "must":
                {"range": {"system.filesystem.used.pct": {
                    "gt": 0.7
                }}}
            ,
            "filter":
                {"range": {"@timestamp": {"gt": "now-2m"}}}

        }
    },
    "aggs": {
        "hostname": {
            "terms": {
                "field": "host.name",
                "size": 10
            },
            "aggs": {
                "mountpoint": {
                    "terms": {
                        "field": "system.filesystem.mount_point",
                        "size": 10
                    },
                    "aggs": {
                        "mount_pec": {
                            "terms": {
                                "field": "system.filesystem.used.pct",
                                "size": 10
                            }
                        }
                    }
                }
            }
        }

    }
}

# 根据剩余的 byte 查询
query_by_byte = {
    "_source": [
        "system.filesystem.used.pct",
        "system.filesystem.available",
        "system.filesystem.total",
        "system.filesystem.mount_point",
        "system.filesystem.free",
        "host.name"
    ],
    "query": {
        "bool": {
            "must_not": [
                {
                    "range": {
                        "system.filesystem.total": {
                            "lte": 5368709120
                        }
                    }
                }
            ],
            "must": {
                "range": {
                    "system.filesystem.free": {
                        "lt": 10737418240
                    }
                }
            },
            "filter": {
                "range": {
                    "@timestamp": {
                        "gte": "now-2m"
                    }
                }
            }
        }
    },
    "aggs": {
        "hostname": {
            "terms": {
                "field": "host.name",
                "size": 10
            },
            "aggs": {
                "mountpoint": {
                    "terms": {
                        "field": "system.filesystem.mount_point",
                        "size": 10
                    },
                    "aggs": {
                        "mount_free": {
                            "terms": {
                                "field": "system.filesystem.free",
                                "size": 10
                            }
                        }
                    }
                }
            }
        }
    }
}


def query_from_es(url, query):
    """
    根据参数从 ES 查询数据,并将根据 host 汇聚的列表返回
    """
    headers = {'Content-Type': 'application/json'}
    try:
        res = requests.post(url, headers=headers, data=json.dumps(query))
        return res.json()['aggregations']['hostname']['buckets']
    except Exception as error:
        print(error)
        return False


app = Flask(__name__)


@app.route('/hdbypct', methods=['POST'])
def hdbypct():
    """
    根据剩余百分比查询
    """
    if not request.json or 'warn' not in request.json:
        abort(400)
    warn = request.json['warn']
    query_by_pct['query']['bool']['must']['range']['system.filesystem.used.pct']['gt'] = warn
    data = query_from_es(URL, query_by_pct)

    if data != False:
        return jsonify({
            'status_code': 200,
            'data': data
        })
    else:
        abort(501)


@app.route('/hdbybyte', methods=['GET', 'POST'])
def hdbybyte():
    """
    根据剩余可用空间查询
    """
    if not request.json or 'bytes' not in request.json:
        abort(400)
    byte = request.json['bytes']
    query_by_byte['query']['bool']['must']['range']['system.filesystem.free']['lt'] = byte
    data = query_from_es(URL, query_by_byte)

    if data != False:
        return jsonify({
            'status_code': 200,
            'data': data
        })
    else:
        abort(501)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
