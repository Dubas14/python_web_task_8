import pika
from models import Contact
from faker import Faker

fake = Faker()


def create_contacts(n):
    contacts = []
    for _ in range(n):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            preferred_method=fake.random_element(['email', 'sms'])
        ).save()
        contacts.append(contact)
    return contacts


def send_to_queue(contact):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    if contact.preferred_method == 'email':
        queue = 'email_queue'
    else:
        queue = 'sms_queue'

    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=str(contact.id))
    print(f"Sent contact {contact.fullname} ({contact.preferred_method}) to {queue}")

    connection.close()


if __name__ == '__main__':
    contacts = create_contacts(10)
    for contact in contacts:
        send_to_queue(contact)
