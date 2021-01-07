# Import Flask things
from flask import request

# Import Helpers
from app.helpers.dict import AttrDict
from app.helpers.checker import check_if_db_operator_exists

# Import Utils
import json
import math


class DataTable:

    def __init__(self, document, schema):
        """
        Receving Default Arguments
        :param document:
        :param schema:
        """
        self.document = document
        self.schema = schema
        self.args = AttrDict(json.loads(request.get_data(parse_form_data=True, as_text=True)))
        self.limit = self.args.limit or 10
        self.page = self.args.page or 1

    @property
    def get_data(self):
        data = self.document.objects
        data = self.advance_search(data)

        data = data.skip(self.limit * (self.page - 1))
        data = data.limit(self.limit * self.page)

        total_available_data = self.document.objects.count()
        last_page = math.ceil(total_available_data / self.limit)
        prev_page = (self.page - 1) > 0 and (self.page - 1) or None
        next_page = (self.page + 1) <= last_page and (self.page + 1) or None

        return {
            "total_records": total_available_data,
            "total_records_got": data.count(),
            "current_page": self.page,
            "limit": self.limit,
            "next_page": next_page,
            "prev_page": prev_page,
            "first_page": 1,
            "last_page": last_page,
            "data": self.schema(many=True).dump(data).data
        }

    def advance_search(self, data):
        """
        Advancing Database Search
        :param data:
        :return:
        """
        if len(self.args.search):
            for search in self.args.search:
                search = AttrDict(search)
                if check_if_db_operator_exists(operator=search.operator):
                    data = data.filter(**{f'{search.key}__{search.operator or "equal"}': search.value})
        return data
