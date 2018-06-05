#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import redis
import pickle


DB = {
        "host": os.getenv('DB_HOST') or 'localhost',
        "port": os.getenv('DB_PORT') or 6379,
        "db": os.getenv("DB_INDEX") or 0
    }


class BSEModel:
    database = DB

    def __init__(self, data_object=None):
        self.redis_client = redis.StrictRedis(**self.database)
        self.data_object = data_object
        if isinstance(self.data_object, (list, tuple)):
            self.save_bulk()
        elif isinstance(self.data_object, dict):
            self.save()

    def save(self):
        self.name = self.data_object.get('name')
        self.value = pickle.dumps(self.data_object.get('value'))
        self.redis_client.set(self.name, self.value)

    def save_bulk(self):
        pipeline = self.redis_client.pipeline()
        for obj in self.data_object:
            _name = obj.get('name')
            _value = pickle.dumps(obj.get('value'))
            pipeline.set(_name, _value)
        pipeline.execute()

    def __iter__(self):
        for key in self.redis_client.keys():
            yield self.to_dict(key)

    def to_dict(self, key):
        _code, _open, _high, _low, _close = pickle.loads(
            self.redis_client.get(key))
        return {
                'name': key.decode('utf-8'),
                'code': _code,
                'open': _open,
                'close': _close,
                'high': _high,
                'low': _low
        }

    @classmethod
    def search(cls, pattern):
        response = list()
        _cls = cls()
        for _name in _cls.redis_client.keys():
            if _name and _name.lower().find(pattern.lower().encode()) != -1:
                response.append(_cls.to_dict(_name))
        return response

    @classmethod
     def limit(cls, num=10, sort=False, field=None, order=None):
         _resp = list()
         _cls = cls()
         if sort:
             return cls.sorted_resp(list(_cls), field, order)[:num]
         for index, item in enumerate(_cls):
             if num <= index:
                 return _resp
             _resp.append(item)
         return _resp

     @staticmethod
     def sorted_resp(resp, field, order):
         """
         field: field can be any column on which we want sorting `low`|`high`.
         order: order is sorting order `asc`|`desc`.
         """
         return sorted(resp, key=lambda k: float(k[field]), reverse=order == 'desc')
