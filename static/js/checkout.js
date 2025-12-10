/**
 * checkout.js
 * gets selected plan and creates card payment element
 */
// update selected plan
const plan = document.getElementById("item")
const selectedPrice = document.getElementById("selected-price")
// set price on pageload
let planText = plan.options[plan.selectedIndex].innerText
selectedPrice.innerText = planText.split('£')[1];
// add listener for any changes
plan.addEventListener("change", () => {
    let planText = plan.options[plan.selectedIndex].innerText
    newPrice = planText.split('£')[1];
    selectedPrice.innerText = newPrice;
})

// Stripe checkout
const stripePublicKey = JSON.parse(
    document.getElementById("id_stripe_public_key").textContent
);
const clientSecret = JSON.parse(
    document.getElementById("id_client_secret").textContent
);

const stripe = Stripe(stripePublicKey);
const elements = stripe.elements();

// Create card element with style options
const card = elements.create("card", {
  style: {
    base: {
      iconColor: '#c4f0ff',
      color: '#fff',
      fontWeight: '500',
      fontFamily: 'Roboto, Open Sans, Segoe UI, sans-serif',
      fontSize: '16px',
      fontSmoothing: 'antialiased',
      ':-webkit-autofill': {
        color: '#fce883',
      },
      '::placeholder': {
        color: '#87BBFD',
      },
    },
    invalid: {
      iconColor: '#f44c36ff',
      color: '#f44336',
    },
  },
});
card.mount("#card-element");

// Display card errors
card.on("change", function (event) {
    if (event.error) {
        showMessage(event.error.message);
    }
});

const form = document.getElementById("payment-form");
form.addEventListener("submit", async function (e) {
    e.preventDefault();    
    // Disable button to prevent duplicate charges
    setLoading(true);
    const result = await stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            billing_details: {
                name: document.getElementById("id_full_name").value,
                email: document.getElementById("id_email").value,
                phone: document.getElementById("id_phone_number").value,
            },
        },
    });
    if (result.error) {
        // Show error and re-enable button
        showMessage(result.error.message);
        setLoading(false);        
    } else {
        if (result.paymentIntent.status === "succeeded") {
            // Submit the form to Django
            form.submit();
        }
    }
});

// ------- UI helpers -------

function showMessage(messageText) {
  const messageContainer = document.getElementById("card-errors");
  messageContainer.classList.remove("hidden");
  messageContainer.textContent = messageText;
  setTimeout(function () {
    messageContainer.classList.add("hidden");
    messageContainer.textContent = "";
  }, 4000);
}

// Show a spinner on payment submission
function setLoading(isLoading) {
  if (isLoading) {
    // Disable the button and show a spinner
    document.querySelector("#submit-button").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("#submit-button").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
}