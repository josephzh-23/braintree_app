import dropin from 'braintree-web-drop-in';


import { useEffect, useRef, useState } from 'react';

const BraintreeDropIn = () => {
  const dropinInstance = useRef(null);
  const dropinContainer = useRef(null);
  const [amount, setAmount] = useState('');
  const [cvv, setCvv] = useState('');

  useEffect(() => {
    fetch('/client_token')
      .then(res => res.json())
      .then(data => {
        dropin.create({
          authorization: data.token,
          container: dropinContainer.current,
        }, (err, instance) => {
          if (err) {
            console.error(err);
            return;
          }
          dropinInstance.current = instance;
        });
      });
  }, []);

  const handlePayment = async (e) => {
    e.preventDefault();
    if (!dropinInstance.current) return;

    try {
      const { nonce } = await dropinInstance.current.requestPaymentMethod();
      const formData = new FormData();
      formData.append('amount', amount);
      formData.append('payment_method_nonce', nonce);
      formData.append('cvv', cvv);

      const response = await fetch('/checkout', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      if (result.success) {
        alert(`Payment successful! Transaction ID: ${result.transaction_id}`);
      } else {
        alert(`Payment failed: ${result.error}`);
      }
    } catch (err) {
      console.error('Payment error:', err);
      alert('Failed to complete payment.');
    }
  };

  return (
      <div className="payment-wrapper">

    <form onSubmit={handlePayment} className="payment-form">
  <h2 className="payment-title">Pay with Braintree</h2>

  <div ref={dropinContainer} className="dropin-container"></div>

  <input
    type="number"
    name="amount"
    placeholder="Amount"
    required
    value={amount}
    onChange={(e) => setAmount(e.target.value)}
    className="input-field"
  />

  <input
    type="text"
    name="cvv"
    placeholder="CVV"
    value={cvv}
    onChange={(e) => setCvv(e.target.value)}
    required
    className="input-field"
  />

  <button type="submit" className="pay-button">Pay</button>
</form>
</div>
  );
};

export default BraintreeDropIn;