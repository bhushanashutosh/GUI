# Install the necessary dependencies
!pip install streamlit pyngrok


# Import the necessary libraries
import streamlit as st
import random
from datetime import datetime
from pyngrok import ngrok

# Set up the Streamlit page
st.set_page_config(page_title="CommBank Pay", layout="centered")
st.title("\U0001F4B3 CommBank Pay")

st.markdown("### Pay Someone")

# Input fields
recipient_name = st.text_input("Recipient Name", "")
recipient_id = st.text_input("Mobile number or PayID", "")
amount = st.text_input("Amount (AUD)", "")
description = st.text_input("Description (optional)", "")

# Quick amount buttons
quick_amount = st.radio("Quick Amounts", ["$50", "$100", "$200", "Other"], horizontal=True)
if quick_amount != "Other":
    amount = quick_amount.strip("$")

# Submit button
if st.button("Pay"):
    if not recipient_name:
        st.error("Please enter recipient name")
    elif not recipient_id:
        st.error("Please enter mobile number or PayID")
    else:
        try:
            float(amount)
            # Show confirmation
            st.success("\U00002705 Payment Successful")
            st.markdown("---")
            st.markdown(f"**Amount:** ${amount}")
            st.markdown(f"**To:** {recipient_name}")
            st.markdown(f"**Account:** {recipient_id}")
            if description:
                st.markdown(f"**Description:** {description}")
            st.markdown(
                f"**The recipient should receive the payment immediately.**"
            )
            st.markdown("---")
            st.markdown(f"**Receipt #:** {random.randint(1000000, 9999999)}")
            st.markdown(f"**Date:** {datetime.now().strftime('%d %b %Y at %I:%M %p')}")
        except ValueError:
            st.error("Please enter a valid amount")

# Run your Streamlit app
!streamlit run /content/commbank_web.py &

# Set up a tunnel to the Streamlit app
public_url = ngrok.connect(port='8501')

# Display the public URL
print(f"Streamlit app is running at: {public_url}")
