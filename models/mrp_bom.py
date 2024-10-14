from odoo import models, fields, api, _


class MRPProduction(models.Model):
    """Available products that can be made using Bill of Materials"""
    _inherit = "mrp.bom"
    
    product_count = fields.Integer(string="Available Quantity",
                                   compute="_compute_product_count",
                                   help="Number of products that can be made "
                                        "using available BOMs.")


    @api.depends('product_id')
    def _compute_product_count(self):
        """Check number of products that can be made using available BOMs"""
        for record in self:
            record.product_count = ''
            product_id = record.bom_id.bom_line_ids.mapped('product_id')
            bom_quantity = record.bom_id.bom_line_ids.mapped('product_qty')
            product_quantity = [products.free_qty for products in
                                product_id]
            product_count_min = []
            for bom_quant, product_quant in zip(bom_quantity, product_quantity):
                available_quantity = product_quant / bom_quant
                product_count_min.append(available_quantity)
            if 0 in product_quantity:
                record.product_count = 0
            elif len(product_count_min) != 0:
                record.product_count = min(product_count_min)