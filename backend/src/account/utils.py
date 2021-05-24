from .tasks import send_mail

class Util:

    @staticmethod
    def send_email(data):
        send_mail.delay(data)
