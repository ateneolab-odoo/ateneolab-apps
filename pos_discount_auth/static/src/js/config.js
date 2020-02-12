odoo.define('pos_discount_auth.config', function (require) {
    "use strict";

    var module = require('point_of_sale.models');
    var PosModelExtend = module.PosModel;
    var models = PosModelExtend.prototype.models;
        for(var i=0; i<models.length; i++){
            var model=models[i];
            if(model.model === "pos.config"){
                 model.fields.push("code");
            }
        }
});
