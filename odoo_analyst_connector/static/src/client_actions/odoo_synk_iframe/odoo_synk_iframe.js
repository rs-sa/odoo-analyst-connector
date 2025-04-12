/** @odoo-module **/

import core from 'web.core';
import AbstractAction from 'web.AbstractAction';
import {qweb} from 'web.core';

const {_t} = core;

var OdooSyncIframe = AbstractAction.extend({
    template: 'OdooSyncIframe',

    init: function (parent, action, options) {
        this._super.apply(this, arguments);
        console.log("action.context : ", action.context);
        console.log("action.context.iframe_url : ", action.context.iframe_url);
        this.iframeUrl = action.context && action.context.iframe_url;
        this.isLoading = true;
        this.error = null;
    },

});

core.action_registry.add('odoo_synk_iframe', OdooSyncIframe);

return OdooSyncIframe;
