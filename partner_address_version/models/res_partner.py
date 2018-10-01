# -*- coding: utf-8 -*-
# Copyright 2018 Akretion - Benoît Guillot
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api
import hashlib
from collections import OrderedDict


class ResPartner(models.Model):
    _inherit = "res.partner"

    version_hash = fields.Char(readonly=True, copy=False)
    date_version = fields.Datetime(string='Date version', readonly=True)

    @api.multi
    def get_or_create_address_version(self):
        self.ensure_one()
        version_hash = self.get_version_hash()
        versioned_partner = self.with_context(active_test=False).search(
            [('version_hash', '=', version_hash)])
        if versioned_partner:
            return versioned_partner
        default = {
            'active': False,
            'version_hash': version_hash,
            'parent_id': self.parent_id and self.parent_id.id or self.id,
            'date_version': fields.Datetime.now(),
        }
        versioned_partner = self.copy(default=default)
        return versioned_partner

    def get_version_fields(self):
        return ['name', 'street', 'street2', 'zip', 'city', 'country_id']

    def get_version_hash(self):
        version_fields = self.get_version_fields()
        version = OrderedDict()
        for field in version_fields:
            if self[field]:
                version[field] = self[field]
        version_hash = hashlib.md5(str(version)).hexdigest()
        return version_hash
