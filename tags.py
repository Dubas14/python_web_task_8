from models import Quote
import redis


cache = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def search_by_author(name):
    cached_result = cache.get(f"name:{name}")
    if cached_result:
        print(cached_result)
        return

    quotes = Quote.objects(author__fullname__icontains=name)
    if quotes:
        result = "\n".join([f"{quote.quote} - {quote.author.fullname}" for quote in quotes])
        cache.set(f"name:{name}", result)
        print(result)
    else:
        print("Author not found.")


def search_by_tag(tag):
    cached_result = cache.get(f"tag:{tag}")
    if cached_result:
        print(cached_result)
        return

    quotes = Quote.objects(tags__icontains=tag)
    if quotes:
        result = "\n".join([f"{quote.quote} - {quote.author.fullname}" for quote in quotes])
        cache.set(f"tag:{tag}", result)
        print(result)
    else:
        print("Tag not found.")


def search_by_tags(tags):
    cached_result = cache.get(f"tags:{','.join(tags)}")
    if cached_result:
        print(cached_result)
        return

    quotes = Quote.objects(tags__in=tags)
    if quotes:
        result = "\n".join([f"{quote.quote} - {quote.author.fullname}" for quote in quotes])
        cache.set(f"tags:{','.join(tags)}", result)
        print(result)
    else:
        print("No quotes found for the given tags.")


def main():
    while True:
        command = input("Enter command (name:author, tag:tag, tags:tag1,tag2, exit): ")
        if command.startswith("name:"):
            name = command.split(":", 1)[1].strip()
            search_by_author(name)
        elif command.startswith("tag:"):
            tag = command.split(":", 1)[1].strip()
            search_by_tag(tag)
        elif command.startswith("tags:"):
            tags = command.split(":", 1)[1].strip().split(",")
            search_by_tags(tags)
        elif command == "exit":
            break
        else:
            print("Unknown command!")


if __name__ == '__main__':
    main()
