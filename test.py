

DNS = 'https://pacificlightheyoofdgd.firebaseio.com'

def post_to_firebase(psig):
    from firebase import firebase
    connection = firebase.FirebaseApplication(DNS, authentication=None)
    result = connection.post('/users', {'pressure',psig})
    
    print result

