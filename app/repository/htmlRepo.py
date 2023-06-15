from bson import json_util, ObjectId
import json
from . import db


class HtmlRepo:
    def __init__(self):
        self.htmls = db["html_extraction"]

    def get_html_extraction_by_id(self, html_id):
        html_extraction_data = self.htmls.find_one({"_id": ObjectId(html_id)})
        if html_extraction_data is not None:
            html_extraction_data = json.loads(json_util.dumps(html_extraction_data))
            html_extraction_data["_id"] = html_extraction_data["_id"]["$oid"]
        return html_extraction_data

    def get_all_htmls_extractions(self):
        cursor = self.htmls.find({})
        htmls_extraction_data = list(cursor)
        htmls_extraction_data = json.loads(json_util.dumps(htmls_extraction_data))
        for item in htmls_extraction_data:
            item["_id"] = item["_id"]["$oid"]
        return htmls_extraction_data

    def save_html_extraction(self, html_extraction_data):
        persisted_data = self.htmls.insert_one(html_extraction_data)
        new_id = json.loads(json_util.dumps(persisted_data.inserted_id))
        return list(new_id.values())[0]

    def update_html_extraction(self, html_id, html_extraction_data):
        result = self.htmls.update_one(
            filter={"_id": ObjectId(html_id)},
            update={"$set": {"data_ekstraksi": html_extraction_data}},
        )
        return result.modified_count

    def delete_html_extraction(self, html_id):
        result = self.htmls.delete_one({"_id": ObjectId(html_id)})
        return result.deleted_count
