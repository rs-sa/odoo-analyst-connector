/** @odoo-module **/
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {Layout} from "@web/search/layout";
import {Component, useState, onMounted} from "@odoo/owl";

export class OdooSyncIframe extends Component {
    setup() {
        this.notification = useService("notification");
        const iframe_url = this.props.action.context?.iframe_url

        this.state = useState({
            isLoading: true,
            error: null,
            iframeUrl: iframe_url, // Read URL from context
        });

        onMounted(() => this.initializeIframe());
    }

    async initializeIframe() {
        const iframe_url = this.props.action.context?.iframe_url
        try {
            // Instead of using fetch directly, we'll use the iframe to navigate to the login page
            // This avoids CORS issues since the iframe will handle the authentication
            this.state.iframeUrl = iframe_url ;
            this.state.isLoading = false;
        } catch (error) {
            console.error('Authentication error:', error);
            this.state.error = error.message || "Failed to connect to remote Odoo server";
            this.notification.add(this.state.error, {
                type: 'danger',
                sticky: true,
            });
        }
    }

    handleIframeLoad(ev) {
        console.log("Iframe loaded");
        // The iframe has loaded - we can hide the loading indicator
        this.state.isLoading = false;
    }

    changeColor() {
        document.getElementById("myParagraph").style.backgroundColor = "red";
    }
}

OdooSyncIframe.template = 'odoo_analyst_connector.OdooSyncIframe';
OdooSyncIframe.components = {Layout};

// Register the action with required services
registry.category("actions").add("odoo_synk_iframe", OdooSyncIframe);

