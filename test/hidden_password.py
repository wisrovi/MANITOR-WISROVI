from decouple import config

userID = config('userID',default='')
password = config('password',default='')

print(userID, password)