import serial, datetime


#---------------------------------------------------------------#


logging_frequency = 60 #seconds
critical_pressure = 2500 # psig

 
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
from Daemon import Daemon
 
class MyDaemon(Daemon):
        def run(self):
                while True:

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

                            if result['pressure'] < critical_pressure:


                                try:
                                    
                                    print 'Sending Joe an email'
                                    notify_joe(100)

                                except:

                                    print "failed to send a message"




 
if __name__ == "__main__":
        daemon = MyDaemon('/tmp/daemon-example.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)

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

        if result['pressure'] < critical_pressure:


            try:
                
                print 'Sending Joe an email'
                notify_joe(result['pressure'])

            except:

                print "failed to send a message"




