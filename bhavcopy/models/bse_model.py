#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from limpyd import model
import os

local_db = model.RedisDatabase(
    host=os.getenv('DB_HOST') or 'localhost',
    port=os.getenv('DB_PORT') or 6379,
    db=os.getenv("DB_INDEX") or 0
)


class BSEModel(model.RedisModel):
    database = local_db

    name = model.StringField(indexable=True)
    code = model.StringField()
    open_at = model.StringField()
    close_at = model.StringField()
    low = model.StringField()
    high = model.StringField()

    def __repr__(self):
        return str(self.hmget('name'))

    @classmethod
    def search(cls, pattern):
        response = list()
        for item in cls.collection().instances():
            _name = item.name.get()
            if _name and _name.lower().find(pattern.lower()) != -1:
                response.append(cls.to_dict(item))
        return response

    @staticmethod
    def to_dict(obj):
        return {
            'name': obj.name.get(),
            'code': obj.code.get(),
            'open': obj.open_at.get(),
            'close': obj.close_at.get(),
            'high': obj.high.get(),
            'low': obj.low.get()
        }

    def __iter__(self):
        for obj in self.collection().instances():
            yield self.to_dict(obj)

    @classmethod
    def limit(cls, num=10):
        _resp = list()
        for index, item in enumerate(cls()):
            if num <= index:
                return _resp
            _resp.append(item)
        return _resp
