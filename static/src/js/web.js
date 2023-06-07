odoo.define('cfr.web.js', function (require) {
    "use strict";

    var core = require('web.core');
    var Menu = require('web.Menu');

    Menu.include({
        start: function () {
            var self = this;
            this._super.apply(this, arguments);
            if (this.action) {
                var menu_id = this.action.context.params.menu_id;
                console.log("Menu ID:", menu_id);
                alert("Hello! I am an alert box!!":menu_id);
                // You can now use the menu_id variable as needed
            }
        },
    });
});