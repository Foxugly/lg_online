from accountant.models import Accountant
from address.models import Address

adr = Address(name="LG", street="Avenue Reine Marie Henriette", number="29", zipcode="1190", city="Bruxelles")
adr.save()
c = Accountant(name="Renaud", email="rv@lieutenantguillaume.com", telephone="+32478811988", default=True, address=adr)
c.save()
