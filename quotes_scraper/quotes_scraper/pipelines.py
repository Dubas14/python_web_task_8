import json
import os
from itemadapter import ItemAdapter

class DataPipeline:
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'fullname' in adapter.keys():
            self.authors.append(dict(adapter))
        if 'quote' in adapter.keys():
            self.quotes.append(dict(adapter))
        return item

    def close_spider(self, spider):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        quotes_path = os.path.join(base_dir, 'quotes.json')
        authors_path = os.path.join(base_dir, 'authors.json')

        with open(quotes_path, 'w', encoding='utf-8') as fd:
            json.dump(self.quotes, fd, ensure_ascii=False, indent=2)

        with open(authors_path, 'w', encoding='utf-8') as fd:
            json.dump(self.authors, fd, ensure_ascii=False, indent=2)
