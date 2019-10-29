from contact.models import Contact
c = Contact(name="Renaud",email="rv@lieutenantguillaume.com", telephone="+32478811988", default=True)
c.save()
