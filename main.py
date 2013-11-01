import serial, datetime, firebase, time


#---------------------------------------------------------------#


logging_frequency = 60*20 #seconds
critical_pressure = 400 # psig



#--------------------------------------------------------------------#

DNS = 'https://pacificlightheyoofdgd.firebaseio.com'


def post_to_firebase(psig):
    from firebase import firebase
    import json, datetime
    
    
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime)  or isinstance(obj, datetime.date) else None
    datetime_str = json.dumps(datetime.datetime.now(), default=dthandler)
    connection = firebase.FirebaseApplication(DNS, authentication=None)
    result = connection.post('/readings', { 'datetime':str(datetime_str),'pressure':str(psig)})
    
    print result


    
     
def handle_queue(queue):

    lines = queue.split('\n')
    current_list = []
    for each in lines:

        if each.strip() == '':
            break
        #print each

        try:
            key,value = each.split(':')

            if key == 'voltage':
                value = float(value[:5])
            elif key == 'pressure':
                value = float(value[:8])
            current_list.append({key:value})

        except:
            pass
    return current_list [-2:]


def notify_joe(psi):
    import smtplib
    #Gmail parameters-----------------------------------------------#


    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
     
    sender = 'plt.noreply@gmail.com'
    recipient = 'matt.bertram@pacificlighttech.com'
    subject = 'Test: Ar Tank in 211i Low'
    body = 'This is an automated message from PLT management.\n The tank in 211i needs to be changed. The pressure is currently: ' +str(psi)+' psig'



    body = "" + body + ""
     
    headers = ["From: " + sender,
               "Subject: " + subject + ' @ '+str(psi)+' psig',
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/html"]
    headers = "\r\n".join(headers)
     
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
     
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(sender, 'lucas105163')
     
    session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
    session.quit()


ser = serial.Serial( port = '/dev/ttyACM0', baudrate = 9600, timeout =0)


queue = ""

#---------------------------------------#
#Start timer

start_time = datetime.datetime.now()


import sys, time


while(True):
    queue+= ser.read(50)
    current_reading = handle_queue(queue)

    result = {}
    for d in current_reading: result.update(d)
    now_time = datetime.datetime.now()
    delta_time = now_time-start_time

    if delta_time.seconds >= logging_frequency:
        print result
        start_time = datetime.datetime.now()

        #----- Testing Criteria-----#
        
        try:
            
            print "posting to firebase"
            post_to_firebase(result['pressure'])
            
        except:
            print "failed to post to firebase"
            
        if result['pressure'] < critical_pressure:


            try:
                
                print 'Sending Joe an email'
                notify_joe(result['pressure'])

            except:

                print "failed to send a message"




