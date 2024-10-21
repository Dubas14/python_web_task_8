import json
from models import Author, Quote

def load_authors(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        authors_data = json.load(f)
        for author in authors_data:
            if not Author.objects(fullname=author['fullname']):
                Author(
                    fullname=author['fullname'],
                    born_date=author.get('born_date', ''),
                    born_location=author.get('born_location', ''),
                    description=author.get('description', '')
                ).save()

def load_quotes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)
        for quote in quotes_data:
            author = Author.objects(fullname=quote['author']).first()
            if author:
                Quote(
                    author=author,
                    quote=quote['quote'],
                    tags=quote['tags']
                ).save()

if __name__ == '__main__':
    load_authors('authors.json')
    load_quotes('qoutes.json')
