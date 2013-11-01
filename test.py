

DNS = 'https://pacificlightheyoofdgd.firebaseio.com'

import json, datetime
    
    
dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime)  or isinstance(obj, datetime.date) else None
datetime_str = json.dumps(datetime.datetime.now(), default=dthandler)

    
print datetime_str    

def post_to_firebase(psig):
    from firebase import firebase
    import json, datetime
    
    
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime)  or isinstance(obj, datetime.date) else None
    datetime_str = json.dumps(datetime.datetime.now(), default=dthandler)
    connection = firebase.FirebaseApplication(DNS, authentication=None)
    result = connection.post('/users', {datetime_str:str(psig)})
    
    print result

