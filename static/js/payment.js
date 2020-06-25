var total = document.getElementById("order-total").innerText

showPayment = () => {
    document.querySelector(".checkout-button").style.visibility = 'hidden';
    document.getElementById("paypal-button-container").style.visibility = 'visible';
}

paypal.Buttons({

    style: {
        color: 'blue',
        shape: 'pill',
    },

    createOrder: function (data, actions) {
        // This function sets up the details of the transaction, including the amount and line item details.
        return actions.order.create({
            purchase_units: [{
                amount: {
                    value: parseFloat(total).toFixed(2)
                }
            }]
        });
    },
    onApprove: function (data, actions) {
        // This function captures the funds from the transaction.
        return actions.order.capture()
        .then(function (details) {
            // This function shows a transaction success message to your buyer.
            document.getElementById("payment-done").click();
        });
    }
}).render('#paypal-button-container');
//This function displays Smart Payment Buttons on your web page.