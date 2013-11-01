from firebase import firebase
firebase = firebase.FirebaseApplication('https://pacificlightheyoofdgd.firebaseio.com', authentication=None)
authentication = firebase.Authentication('Cd0BqpMxoX7naobGQQio2JgUHdbLmNyYSazlaE6f', 'bertram.matthew@gmail.com    ')
firebase.authentication = authentication
print authentication.extra
user = authentication.get_user()
print user.firebase_auth_token