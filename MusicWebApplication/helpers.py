from django.core.mail import send_mail
from django.conf import settings

def User_Account_Recovery_Email_Token(Email_ID, Token):
    Subject = "Your password reset link"
    Email_Body = f"Hi, click on the link to reset your password http://127.0.0.1:8000/changePassword/{Token}/"
    From_Email_Address = settings.EMAIL_HOST_USER
    Recipient_List = [Email_ID]
    send_mail(Subject, Email_Body, From_Email_Address, Recipient_List)
    return True