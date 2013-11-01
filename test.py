from firebase import firebase



DNS = 'https://pacificlightheyoofdgd.firebaseio.com'

def post_to_firebase(psig):
    
    firebase = firebase.FirebaseApplication(DNS, authentication=None)
    result = firebase.post('/users', {'pressure',psig})
    
    print result

