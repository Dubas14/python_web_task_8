import pika
from models import Contact


def send_sms(contact):
    print(f"Sending SMS to {contact.phone}")
    contact.is_sent = True
    contact.save()


def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects(id=contact_id).first()
    if contact and contact.preferred_method == 'sms':
        send_sms(contact)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='sms_queue')
channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
