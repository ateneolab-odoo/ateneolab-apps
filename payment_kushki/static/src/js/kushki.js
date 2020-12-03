odoo.define('payment_kushki.kushki', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var qweb = core.qweb;
    var _t = core._t;

    ajax.loadJS("https://cdn.kushkipagos.com/kushki-checkout.js");
    // ajax.loadJS("/payment_kushki/static/src/js/kushki-checkout.js");
    ajax.loadXML('/payment_kushki/static/src/xml/kushki_templates.xml', qweb);

    if ($.blockUI) {
        // our message needs to appear above the modal dialog
        $.blockUI.defaults.baseZ = 2147483647; //same z-index as StripeCheckout
        $.blockUI.defaults.css.border = '0';
        $.blockUI.defaults.css["background-color"] = '';
        $.blockUI.defaults.overlayCSS["opacity"] = '0.9';
    }

    require('web.dom_ready');
    if (!$('.o_payment_form').length) {
        return Promise.reject("DOM doesn't contain '.o_payment_form'");
    }

var observer = new MutationObserver(function (mutations, observer) {
    for (var i = 0; i < mutations.length; ++i) {
        for (var j = 0; j < mutations[i].addedNodes.length; ++j) {
            if (mutations[i].addedNodes[j].tagName.toLowerCase() === "form" && mutations[i].addedNodes[j].getAttribute('provider') === 'kushki') {
                _redirectToKushkiCheckout($(mutations[i].addedNodes[j]));
            }
        }
    }
});

function displayError(message) {
    var wizard = $(qweb.render('kushki.error', {'msg': message || _t('Payment error')}));
    wizard.appendTo($('body')).modal({'keyboard': true});
    if ($.blockUI) {
        $.unblockUI();
    }
    $("#o_payment_form_pay").removeAttr('disabled');
}

function _redirectToKushkiCheckout(providerForm) {
    // Open Checkout with further options
    if ($.blockUI) {
        var msg = _t("Just one more second, We are redirecting you to Kushki...");
        $.blockUI({
            'message': '<h2 class="text-white"><img src="/web/static/src/img/spin.png" class="fa-pulse"/>' +
                    '    <br />' + msg +
                    '</h2>'
        });
    }

    var paymentForm = $('.o_payment_form');
    if (!paymentForm.find('i').length) {
        paymentForm.append('<i class="fa fa-spinner fa-spin"/>');
        paymentForm.attr('disabled', 'disabled');
    }

    var datos = {
            amount: providerForm.find("input[name='kamount']").val(),
            acquirer_id: providerForm.find("input[name='kacquirer']").val(),
            merchant_id: providerForm.find("input[name='kmerchant_id']").val(),
            private_merchant_id: providerForm.find("input[name='kprivate_merchant_id']").val(),
            environment: providerForm.find("input[name='kenv']").val(),
            regional: providerForm.find("input[name='kregional']").val(),
            currency: providerForm.find("input[name='kcurrency']").val(),
            invoice_num: providerForm.find("input[name='kinvoice_num']").val(),
            reference: providerForm.find("input[name='kreference']").val(),
            partner_id: providerForm.find("input[name='kpartner_id']").val(),
            return_url: providerForm.find("input[name='kreturn_url']").val()
    }

    var wizard = $(qweb.render('kushki.formulario', datos));
    wizard.appendTo($('body')).modal({'keyboard': true});
    if ($.blockUI) {
        $.unblockUI();
    }

    // var _getKushkiInputValue = function (name) {
        // return providerForm.find('input[name="' + name + '"]').val();
    // };

    // var kushki = Kushki(_getKushkiInputValue('kushki_key'));

    // kushki.redirectToCheckout({
        // sessionId: _getKushkiInputValue('session_id')
    // }).then(function (result) {
        // if (result.error) {
            // displayError(result.error.message);
        // }else{

        // }
    // });
}

$.getScript("https://cdn.kushkipagos.com/kushki-checkout.js", function (data, textStatus, jqxhr) {
    observer.observe(document.body, {childList: true});
    _redirectToKushkiCheckout($('form[provider="kushki"]'));
});


});

