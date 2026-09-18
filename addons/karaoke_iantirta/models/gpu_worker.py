import json

from sigil import _, api, fields, models
from sigil.tools import config


class GpuWorker(models.Model):
    _name = 'gpu.worker'
    _description = 'GPU Worker'

    provider = fields.Selection([
        ("kaggle", "Kaggle")
    ], required=True)

    access_token = fields.Char(
        string="Kaggle API Token",
        help='https://www.kaggle.com/settings/api  (click "Generate New Token" under "API")'
    )

    _quota_json = fields.Json(compute="get_quotas", store=True)

    # Helper
    _worker = None

    def _get_worker_class(self):
        from kplus_tools import KaggleWorker
        provider_map = {
            "kaggle": KaggleWorker
        }
        return provider_map.get(self.provider)

    def get_worker(self):
        if self._worker is None:
            self._worker = self._get_worker_class(self.access_token)
        return self._worker

    def get_quotas(self):
        worker = self.get_worker()
        return json.dumps(worker.get_quotas())

    def action_run(self):
        worker = self.get_worker()