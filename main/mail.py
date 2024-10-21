
import os
# * FUNCTIONS RELATED TO MAIL


def verifymail(mail):
    from validate_email import validate_email
    return validate_email(mail)


def send__mail(id, mail, request, user):
    import smtplib
    from email.mime.text import MIMEText
    message = f"""
        <link
      rel="stylesheet"
      href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
      integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z"
      crossorigin="anonymous"
    />


    <form action="/id" method="post" class="bg-light"  style="padding:5%;"  >
    <h1>Hey👋, {user.name}</h1>
    <h2>Looks like you've sent a request to reset your djank password</h2>
    <br>
    If so, click the below link to change your password
    However, if you didn't send any request, then please ignore this email.
    <br>
    <a href="http://{request.META['HTTP_HOST']}/mail/id/{id.unique_id}/{id.unique_id_2}" class="btn btn-primary">Verify Mail</a>
    <br>
    Thanks
    </form>
    """
    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    email = os.getenv("MAIL_VERIFY_EMAIL")
    password = os.getenv("MAIL_VERIFY_PASSWORD")
    smtp_obj.login(email, password)  # type: ignore
    sender_email = email
    reciver_email = mail
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Djank, Reset Password Request'
    msg['From'] = sender_email
    msg["To"] = reciver_email
    smtp_obj.sendmail(sender_email, reciver_email, msg.as_string())


def send_verify_mail(mail, request, user):
    import smtplib
    from email.mime.text import MIMEText
    message = f"""
        <link
      rel="stylesheet"
      href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
      integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z"
      crossorigin="anonymous"
    />


    <form action="" method="post" class="bg-light"  style="padding:5%;"  >
    <h1>Hey👋, {user.name}</h1>
    <h2>Looks like you've registered for the Entrepreneurship summit 2025</h2>
    <br>
    If so, click the below link to verify it
    However, if you didn't send any request, then please ignore this email.
    <br>
    <a href="http://{request.META['HTTP_HOST']}/mail/verify/{user.unique_id}/" class="btn btn-primary">Verify Mail</a>
    <br>
    Thanks
    </form>
    """
    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    email = os.getenv("MAIL_VERIFY_EMAIL")
    password = os.getenv("MAIL_VERIFY_PASSWORD")
    smtp_obj.login(email, password)
    sender_email = email
    reciver_email = mail
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Djank, Verify Your Mail'
    msg['From'] = sender_email
    msg["To"] = reciver_email
    smtp_obj.sendmail(sender_email, reciver_email, msg.as_string())

# * made this file to make database functions  that will work upon the mail


def check_if_key_is_valid(ids):
    from datetime import datetime, timedelta, timezone
    for id in ids.objects.all():
        # print(ids.objects.all())
        if datetime.now(tz=timezone.utc) - id.time_created > timedelta(hours=2):
            p = id.unique_id
            pk = id.pk
            id.delete()
            return False
        return True
