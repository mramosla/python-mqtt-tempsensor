from twilio.rest import Client
import twilio_init


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = twilio_init.account_sid
auth_token = twilio_init.auth_token
client = Client(account_sid, auth_token)


def sms_send(status):
  alert_msg = "Alert! Office temp in {} zone.".format(status)
  message = client.messages \
                .create(
                     body=alert_msg,
                     from_= twilio_init.twilioNum,
                     to=twilio_init.sendtoNum
                 )

  print(message.sid)

