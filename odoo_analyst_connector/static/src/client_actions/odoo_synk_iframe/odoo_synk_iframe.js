odoo.define('odoo_analyst_connector.odoo_sync_iframe', function (require) {
'use strict';

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var session = require('web.session');
var utils = require('report.utils');

var QWeb = core.qweb;


// var AUTHORIZED_MESSAGES = [
//     'report:do_action',
// ];

var ReportAction = AbstractAction.extend({
    // hasControlPanel: true,
    contentTemplate: 'odoo_analyst_connector.odoo_sync_iframe',

    init: function (parent, action, options) {
        this._super.apply(this, arguments);

        options = options || {};
        this.iframeUrl = action.context && action.context.iframe_url;
    },

});

core.action_registry.add('odoo_analyst_connector.odoo_sync_iframe', ReportAction);

return ReportAction;

});
