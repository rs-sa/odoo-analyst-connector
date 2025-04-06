# # -*- coding: utf-8 -*-
# from odoo import api, fields, models, _
# import json
# from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
#
# from odoo.odoo.http import request
#
#
# class CheckIdentity(models.TransientModel):
#     """ Wizard used to re-check the user's credentials (password) and eventually
#     revoke access to his account to every device he has an active session on.
#
#     Might be useful before the more security-sensitive operations, users might be
#     leaving their computer unlocked & unattended. Re-checking credentials mitigates
#     some of the risk of a third party using such an unattended device to manipulate
#     the account.
#     """
#     _name = 'res.users.odoosync_identitycheck'
#     _description = "Password Check Wizard"
#
#     request = fields.Char(readonly=True, groups=fields.NO_ACCESS)
#     password = fields.Char()
#
#     def _check_identity(self):
#         try:
#             self.create_uid._check_credentials(self.password, {'interactive': True})
#         except AccessDenied:
#             raise UserError(_("Incorrect Password, try again or click on Forgot Password to reset your password."))
#         finally:
#             self.password = False
#
#     def run_check(self):
#         assert request, "This method can only be accessed over HTTP"
#         self._check_identity()
#
#         request.session['identity-check-last'] = time.time()
#         ctx, model, ids, method = json.loads(self.sudo().request)
#         method = getattr(self.env(context=ctx)[model].browse(ids), method)
#         assert getattr(method, '__has_check_identity', False)
#         return method()
#
#     # def revoke_all_devices(self):
#     #     current_password = self.password
#     #     self._check_identity()
#     #     self.env.user._change_password(current_password)
#     #     self.sudo().unlink()
#     #     return {'type': 'ir.actions.client', 'tag': 'reload'}
#
#
