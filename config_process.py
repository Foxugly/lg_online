from django.utils import timezone
from django.utils.translation import gettext as _

tag = "[LG&Associates]"
# domain = "www.mylieutenantguillaume.com"
domain = "127.0.0.1:8000"
reply_to = "info@lieutenantguillaume.com"
time_to_complete_subscription = timezone.timedelta(days=2)
show_msg = True
subject_step1 = _("Inscription")
subject_step2 = _("Inscription complétée")
subject_step3 = _("Dossier incomplet")
subject_step4 = _("Dossier complet")
subject_step5 = _("Offre finale")
subject_step6 = _("Offre finale acceptée")
subject_step7 = _("Inscription clôturé")
