from pressurelogging import *

from Daemon import Daemon
 
class MyDaemon(Daemon):
        def run(self):
            
                #---------------------------------------------------------------#


                logging_frequency = 60*15 #seconds
                critical_pressure = 400 # psig
                
                #---------------------------------------#
                #Start timer
                
                start_time = datetime.datetime.now()
                
                
                #--------------------------------------------------------------------#
                
                
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


