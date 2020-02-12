odoo.define('pos_discount_auth.screens', function (require) {
    "use strict";

    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var screens = require('point_of_sale.screens');

    PosBaseWidget.include({
        init:function(parent,options){
            var self = this;
            this._super(parent,options);
            if (this.gui && this.gui.screen_instances.products && this.gui.screen_instances.products.action_buttons.discount) {
                var disc_widget = this.gui.screen_instances.products.action_buttons.discount;
                disc_widget.password_confirm_discount = function(pc) {
                    self.gui.screen_instances.products.order_widget.password_confirm_discount(pc);
                };
                disc_widget.button_click = function (val) {
                    self.gui.screen_instances.products.order_widget.validate_options = {
                        'title': 'Input authorized code',
                        'value': '',
                    };
                    self.gui.screen_instances.products.order_widget.password_button_click(val);
                };

            }
        },
    });

    screens.OrderWidget.include({
        // password widget
        password_button_click: function() {
            var self = this;
            this.validate_options.confirm = function(val) {
                self.gui.screen_instances.products.order_widget.discount_options = {
                        'title': 'Input discount %',
                        'value': this.pos.config.discount_pc,
                    };
                    self.gui.screen_instances.products.order_widget.password_confirm_discount(val);
            };

             self.gui.show_popup('password', self.validate_options);
        },
        password_confirm_discount: function(val) {
            if (val == this.pos.config.code){
                this.gui.screen_instances.products.order_widget.discount_button_click();
            }else{
                this.gui.show_popup('error', {'title':'Error','body':'Wrong Code'});
            }
        },

        apply_discount: function(pc) {
            var order    = this.pos.get_order();
            var lines    = order.get_orderlines();
            var product  = this.pos.db.get_product_by_id(this.pos.config.discount_product_id[0]);

            var i = 0;
            while ( i < lines.length ) {
                if (lines[i].get_product() === product) {
                    order.remove_orderline(lines[i]);
                } else {
                    i++;
                }
            }
           
            var discount = - pc / 100.0 * order.get_total_with_tax();

            if( discount < 0 ){
                order.add_product(product, { price: discount });
            }
        },
      
        discount_button_click: function() {
            var self = this;
            this.discount_options.confirm = function(val) {
                self.confirm_discount(val);
            };
            this.gui.show_popup('number', this.discount_options);
        },

        confirm_discount: function(val) {
            val = Math.round(Math.max(0,Math.min(100,val)));
            this.apply_discount(val);
        },
    });
    return screens;
});
