from firebase import firebase
firebase = firebase.FirebaseApplication('https://pacificlightheyoofdgd.firebaseio.com', authentication=None)
result = firebase.get('/users', None, {'print': 'pretty'})
print result
{'error': 'Permission denied.'}

authentication = firebase.Authentication('Cd0BqpMxoX7naobGQQio2JgUHdbLmNyYSazlaE6f', 'bertram.matthew@gmail.com    ')
firebase.authentication = authentication
print authentication.extra
{'admin': False, 'debug': False, 'email': 'ozgurvt@gmail.com', 'id': 123, 'provider': 'password'}

user = authentication.get_user()
print user.firebase_auth_token