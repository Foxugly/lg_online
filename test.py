from customuser.models import CustomUser

for c in CustomUser.objects.all():
	print(c)

