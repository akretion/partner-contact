# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, exceptions, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    use_parent_company_name = fields.Boolean("User Parent Company",
        help="If checked, the company of this contact will be the same as the parent partner")
    display_use_parent_company_name = fields.Boolean(compute="_compute_display_use_parent_company_name")
    company = fields.Char(string="Contact Company",
        compute="_compute_company", store=True, readonly=False)

    @api.depends("parent_id.is_company")
    def _compute_display_use_parent_company_name(self):
        for partner in self:
            if partner.parent_id.is_company:
                partner.display_use_parent_company_name = True
            else:
                partner.display_use_parent_company_name = False

    @api.depends("use_parent_company_name", "parent_id.name", "parent_id.is_company")
    def _compute_company(self):
        for partner in self:
            if partner.use_parent_company_name and partner.parent_id.is_company:
                partner.company = partner.parent_id.name

    @api.model_create_multi
    def create(self, vals_list):
        # use_parent_company_name by default for addresses belonging to a company
        for vals in vals_list:
            if "use_parent_company_name" not in vals and vals.get("parent_id"):
                parent = self.browse(vals["parent_id"])
                if parent.is_company and not vals.get("company"):
                    vals["use_parent_company_name"] = True
        return super().create(vals_list)

    @api.onchange("parent_id")
    def onchange_parent_id(self):
        res = super().onchange_parent_id()
        if self.parent_id.is_company:
            if not self.company:
                self.use_parent_company_name = True
        return res

    # take company into account into contact display name
    def _get_contact_name(self, partner, name):
        company = partner.company
        if company:
            contact_name = "%s, %s" % (company, name)
        else:
            contact_name = name
        return contact_name
