# -*- coding: utf-8 -*-
# Copyright 2018 Akretion - Benoît Guillot
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from collections import OrderedDict
import hashlib


class TestAddressVersion(TransactionCase):

    def setUp(self):
        super(TestAddressVersion, self).setUp()
        self.partner_vals = OrderedDict([
            ('name', u'Name'),
            ('street', u'Street'),
            ('street2', u'Street2'),
            ('zip', u'Zip'),
            ('city', u'City'),
            ('country_id', self.env.ref('base.fr'))
        ])
        create_vals = self.partner_vals.copy()
        create_vals['country_id'] = self.env.ref('base.fr').id
        self.partner = self.env['res.partner'].create(create_vals)

    def test_hash(self):
        test_hash = hashlib.md5(str(self.partner_vals)).hexdigest()
        self.assertEqual(test_hash, self.partner.get_version_hash())

    def test_create_version_partner(self):
        new_partner = self.partner.get_or_create_address_version()
        self.assertEqual(new_partner.active, False)
        self.assertNotEqual(new_partner.id, self.partner.id)
        self.assertEqual(new_partner.parent_id.id, self.partner.id)

    def test_get_version_hash(self):
        self.partner.version_hash = self.partner.get_version_hash()
        self.partner.active = False
        version_partner = self.partner.get_or_create_address_version()
        self.assertEqual(version_partner.id, self.partner.id)
