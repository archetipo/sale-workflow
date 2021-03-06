# -*- coding: utf-8 -*-
# (c) 2014 Carlos Sánchez Cifuentes <csanchez@grupovermon.com>
# (c) 2015 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# (c) 2015 Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def recalculate_prices(self):
        return self.reset_lines(price=True)

    @api.multi
    def recalculate_names(self):
        return self.reset_lines(price=False)

    @api.multi
    def reset_lines(self, price=False):
        """
        Reset lines according informations on products and price list
        :param price: boolean to indicate if we are resetting price or
                      descriptions
        """
        for line in self.mapped('order_line'):
            order = line.order_id
            res = line.product_id_change(
                order.pricelist_id.id, line.product_id.id,
                qty=line.product_uom_qty, uom=line.product_uom.id,
                qty_uos=line.product_uos_qty, uos=line.product_uos.id,
                name=line.name, partner_id=order.partner_id.id, lang=False,
                update_tax=True, date_order=order.date_order, packaging=False,
                fiscal_position=order.fiscal_position.id, flag=price)
            if price:
                line.write(res['value'])
            else:
                if 'name' in res['value']:
                    line.write({'name': res['value']['name']})
        return True
