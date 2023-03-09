from celery import shared_task
from drugs_app.models import Drug


@shared_task(name="set_drug_quantity")
def set_drug_quantity(did, qwntt):
    drug = Drug.objects.get(id=did)
    drug.set_quantity(qwntt)
