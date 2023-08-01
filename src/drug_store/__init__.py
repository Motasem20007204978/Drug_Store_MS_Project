from __future__ import absolute_import, unicode_literals

from .celery import app as celery_app

# import drug_store.schema


__all__ = ["celery_app"]
