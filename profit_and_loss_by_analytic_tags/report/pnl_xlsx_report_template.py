# -*- encoding: utf-8 -*-

import time
from odoo import models, api, _, fields
from odoo.exceptions import ValidationError
from xlsxwriter.utility import xl_rowcol_to_cell
from datetime import datetime
from mergedeep import merge

import logging 
_logger = logging.getLogger(__name__)

class XlsxReport(models.AbstractModel): 
    _name = 'report.profit_and_loss_by_analytic_tags.pnl_excel'
    _inherit = 'report.odoo_report_xlsx.abstract'

    def get_domain_query(self, type_account, obj_wizard):
        domain = "WHERE "
        if type_account == 13:
            domain += "account.user_type_id = 13"
        if type_account == 14:
            domain += "account.user_type_id = 14"
        if type_account == 15:
            domain += "account.user_type_id = 15"
        if type_account == 16:
            domain += "account.user_type_id = 16"
        if type_account == 17:
            domain += "account.user_type_id = 17"
        if obj_wizard.tag_ids:
            if len(obj_wizard.tag_ids) == 1:
                domain += " AND aat_acl.account_analytic_tag_id = %s"%(str(obj_wizard.tag_ids.id))
            else:
                domain += " AND aat_acl.account_analytic_tag_id in %s"%(str(tuple(obj_wizard.tag_ids.ids)))
        if obj_wizard.start_date and obj_wizard.end_date:
            domain += " AND aml.date >= '%s' AND aml.date <= '%s'"%(obj_wizard.start_date, obj_wizard.end_date)
        domain += " AND am.state = 'posted'"
        return domain
    
    def generate_xlsx_report(self, workbook, data, objects): 
        workbook.set_properties({
            'comments' : 'Profit and loss'
        })
        money_format = workbook.add_format({'num_format': '[$$]#,##0.00'})
        money_format_bold = workbook.add_format({'num_format': '[$$]#,##0.00', 'bold': True})
        bold = workbook.add_format({'bold': True})
        sheet = workbook.add_worksheet(_('Reporte'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(100)
        sheet.set_column(0, 0, 15)
        domain_income = self.get_domain_query(13, objects)
        query_op_income = """
SELECT aat_acl.account_analytic_tag_id as tag_id,at.name, sum(aml.balance)* -1 as op_income
FROM account_analytic_tag_account_move_line_rel as aat_acl
JOIN account_move_line as aml 
ON aat_acl.account_move_line_id = aml.id
JOIN account_move as am
ON aml.move_id = am.id
JOIN account_account as account
ON aml.account_id = account.id
JOIN account_analytic_tag as at
ON at.id = aat_acl.account_analytic_tag_id
%s
GROUP BY aat_acl.account_analytic_tag_id,at.name ORDER BY aat_acl.account_analytic_tag_id""" % (domain_income)
        self._cr.execute(query_op_income)
        lines_operating_income = self._cr.dictfetchall()
        groupby_tag_income = {item['name']:item for item in lines_operating_income}
        
        domain_revenue = self.get_domain_query(17, objects)
        query_op_revenue = """
SELECT aat_acl.account_analytic_tag_id as tag_id,at.name, sum(aml.balance) as op_revenue
FROM account_analytic_tag_account_move_line_rel as aat_acl
JOIN account_move_line as aml 
ON aat_acl.account_move_line_id = aml.id
JOIN account_move as am
ON aml.move_id = am.id
JOIN account_account as account
ON aml.account_id = account.id
JOIN account_analytic_tag as at
ON at.id = aat_acl.account_analytic_tag_id
%s
GROUP BY aat_acl.account_analytic_tag_id,at.name ORDER BY aat_acl.account_analytic_tag_id""" % (domain_revenue)
        self._cr.execute(query_op_revenue)
        lines_op_revenue = self._cr.dictfetchall()
        groupby_tag_revenue = {item['name']:item for item in lines_op_revenue}


        domain_other_income = self.get_domain_query(14, objects)
        query_other_income = """
SELECT aat_acl.account_analytic_tag_id as tag_id,at.name, sum(aml.balance)*-1 as other_income
FROM account_analytic_tag_account_move_line_rel as aat_acl
JOIN account_move_line as aml 
ON aat_acl.account_move_line_id = aml.id
JOIN account_move as am
ON aml.move_id = am.id
JOIN account_account as account
ON aml.account_id = account.id
JOIN account_analytic_tag as at
ON at.id = aat_acl.account_analytic_tag_id
%s
GROUP BY aat_acl.account_analytic_tag_id,at.name ORDER BY aat_acl.account_analytic_tag_id""" % (domain_other_income)
        self._cr.execute(query_other_income)
        lines_other_income = self._cr.dictfetchall()
        groupby_tag_other_income = {item['name']:item for item in lines_other_income}



        domain_expense = self.get_domain_query(15, objects)
        query_expense = """
SELECT aat_acl.account_analytic_tag_id as tag_id,at.name, sum(aml.balance) as expense
FROM account_analytic_tag_account_move_line_rel as aat_acl
JOIN account_move_line as aml 
ON aat_acl.account_move_line_id = aml.id
JOIN account_move as am
ON aml.move_id = am.id
JOIN account_account as account
ON aml.account_id = account.id
JOIN account_analytic_tag as at
ON at.id = aat_acl.account_analytic_tag_id
%s
GROUP BY aat_acl.account_analytic_tag_id,at.name ORDER BY aat_acl.account_analytic_tag_id""" % (domain_expense)
        self._cr.execute(query_expense)
        lines_expense = self._cr.dictfetchall()
        groupby_tag_expense = {item['name']:item for item in lines_expense}


        domain_depre = self.get_domain_query(16, objects)
        query_depre = """
SELECT aat_acl.account_analytic_tag_id as tag_id,at.name, sum(aml.balance) as depreciation
FROM account_analytic_tag_account_move_line_rel as aat_acl
JOIN account_move_line as aml 
ON aat_acl.account_move_line_id = aml.id
JOIN account_move as am
ON aml.move_id = am.id
JOIN account_account as account
ON aml.account_id = account.id
JOIN account_analytic_tag as at
ON at.id = aat_acl.account_analytic_tag_id
%s
GROUP BY aat_acl.account_analytic_tag_id,at.name ORDER BY aat_acl.account_analytic_tag_id""" % (domain_depre)
        self._cr.execute(query_depre)
        lines_depre = self._cr.dictfetchall()
        groupby_tag_depre = {item['name']:item for item in lines_depre}


        final_dict_by_tag = merge(groupby_tag_income, groupby_tag_revenue, groupby_tag_other_income, groupby_tag_expense, groupby_tag_depre)
        tag_index = 1
        sheet.write(1, 0, "Income", bold)
        sheet.write(2, 0, "Gross Profit", bold)
        sheet.write(3, 0, "Operating Income")
        sheet.write(4, 0, "Operating Revenue")
        sheet.write(5, 0, "Total Gross Profit", bold)
        sheet.write(6, 0, "Other Income")
        sheet.write(7, 0, "Total Income", bold)
        sheet.write(8, 0, "Expenses", bold)
        sheet.write(9, 0, "Expenses")
        sheet.write(10, 0, "Depreciation")
        sheet.write(11, 0, "Total Expenses", bold)
        sheet.write(12, 0, "Net Profit", bold)
        for tag, line in final_dict_by_tag.items():
            sheet.write(0, tag_index, tag, bold)
            sheet.write(3, tag_index, line.get("op_income", 0), money_format)
            sheet.write(4, tag_index, line.get("op_revenue", 0), money_format)
            sheet.write(5, tag_index, line.get("op_income", 0) - line.get("op_revenue", 0), money_format_bold)
            sheet.write(6, tag_index, line.get("other_income", 0), money_format)
            sheet.write(7, tag_index, (line.get("op_income", 0) - line.get("op_revenue", 0)) + line.get("other_income", 0), money_format_bold)

            sheet.write(9, tag_index, line.get("expense", 0), money_format)
            sheet.write(10, tag_index, line.get("depreciation", 0), money_format)
            sheet.write(11, tag_index, line.get("expense", 0) + line.get("depreciation", 0), money_format_bold)
            sheet.write(12, tag_index, (line.get("op_income", 0) - line.get("op_revenue", 0)) + line.get("other_income", 0) - (line.get("expense", 0) -  line.get("depreciation", 0)), money_format_bold)
            tag_index += 1

        