from pressurelogging import *



#---------------------------------------------------------------#


logging_frequency = 60 #seconds
critical_pressure = 400 # psig

#---------------------------------------#
#Start timer

start_time = datetime.datetime.now()


#--------------------------------------------------------------------#

DNS = 'https://pacificlightheyoofdgd.firebaseio.com'
ser = serial.Serial( port = '/dev/ttyACM0', baudrate = 9600, timeout =0)


queue = ""
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
