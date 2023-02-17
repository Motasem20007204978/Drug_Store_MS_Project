from celery import shared_task
from orders_app.models import OrderedDrug


@shared_task(name="reject_order")
def reject_orders(did):
    ordered_drugs = OrderedDrug.objects.filter(drug_id=did)
    for ordered_drug in ordered_drugs:
        if not ordered_drug.order.is_rejected():
            ordered_drug.order.set_status("RE")
    return "the orders is rejected successfully"
