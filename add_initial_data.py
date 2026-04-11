import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evslot_dj_pro.settings')
django.setup()

from charging.models import EVAdmin, EVRegister, EVStation

print("Adding initial data...")

# Admin create
try:
    EVAdmin.objects.create(username='admin', password='admin@')
    print("Admin created")
except:
    print("Admin already exists")

# Sample user
try:
    EVRegister.objects.create(name='manu', address='perambalur', mobile=9384432004, email='manuvelu@gmail.com', uname='manuvelu', passw='manuvelu@', account='', card='', bank='', amount=10000)
    print("User created")
except:
    print("User already exists")

# Sample station
try:
    EVStation.objects.create(name='Auto_LPG', stype='Private', numcharger=6, area='NH 38', city='Perambalur', lat='11.201109', lon='78.878258', uname='Auto_LPG_ST', passw='Auto_LPG@', status=1, landmark='near Sri Ramakrishna College', mobile=6398765432, email='autolpgstation@gmail.com')
    print("Station created")
except:
    print("Station already exists")

print("Done!")
