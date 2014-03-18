# coding=utf-8

import json
from  bson.json_util import default, object_hook


class JSONParserException(Exception):
    pass


class JSONParser(object):
    """
    Common JSON Parser
    http://api.mongodb.org/python/1.7/api/pymongo/json_util.html
    """

    @staticmethod
    def to_json(collection):
        """
        Serialize a Python Collection to a JSON String

        collection: Python Collection
        Returns: String
        """
        try:
            json_str = json.dumps(collection, default=default)
            return json_str
        except Exception as e:
            raise JSONParserException(e)

    @staticmethod
    def to_collection(json_str):
        """
        Deserialize a JSON String into a Python Collection

        json_str: String
        Returns: Python Collection
        """
        try:
            collection = json.loads(json_str, object_hook=object_hook)
            return collection
        except Exception as e:
            raise JSONParserException(e)
