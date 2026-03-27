# Stripe Payment Intent

This example demonstrates creating payment intents using Stripe's API with propact.

## Content

```json
{
  "amount": 1999,
  "currency": "usd",
  "payment_method_types": ["card"],
  "description": "Propact Universal Transport License",
  "metadata": {
    "via": "propact-md-transport",
    "product": "propact-license",
    "version": "1.0.0"
  },
  "automatic_payment_methods": {
    "enabled": true
  }
}
```

## Expected Output

The response will include:
- Payment intent ID
- Client secret for frontend
- Payment status
- Amount and currency

## Run Command

```bash
propact README.md \
  --endpoint "https://api.stripe.com/v1/payment_intents" \
  --header "Authorization: Bearer $STRIPE_SECRET_KEY"
```

## Environment Variables

```bash
STRIPE_SECRET_KEY=<YOUR_STRIPE_SECRET_KEY>
```

## Requirements

- Stripe account (test mode recommended)
- Secret key from Stripe Dashboard
- Proper API permissions enabled

## Next Steps

Use the returned `client_secret` in your frontend with Stripe.js to complete the payment.
