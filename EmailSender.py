import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load email credentials from .env
load_dotenv()
from_email = os.getenv("EMAIL_ADDRESS")
app_password = os.getenv("APP_PASSWORD")

# Email template
def send_promotional_email(to_email, customer_id, clv_value):
    subject = "🌟 Special Offer Just for You!"

    body = f"""
Hi Customer #{int(customer_id)},

We’re excited to offer you an exclusive **40% off** just for being a valued part of our community.

🛍️ Shop now and enjoy big savings on your next order.

💻 Visit our website to explore limited-time deals and personalized offers just for you!

Let’s make your next shopping experience even better.

Best regards,  
Your E-Commerce Team
"""

    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, app_password)
        server.send_message(message)
        server.quit()
        print(f"✅ Email sent to: {to_email}")
    except Exception as e:
        print(f"❌ Failed to send to {to_email}: {e}")

# Load data
df = pd.read_csv("final_outputs.csv")

# Filter customers with churn ≥ 60% AND valid email
target_customers = df[df["Churn_Prob"] >= 0.60].copy()
target_customers = target_customers.dropna(subset=["Email"])

# Loop and send email only to valid emails
for _, row in target_customers.iterrows():
    email = str(row["Email"]).strip()
    if email and "@" in email:
        send_promotional_email(
            to_email=email,
            customer_id=row["Customer_Id"],
            clv_value=row["Predicted_CLV"]
        )
    else:
        print(f"⚠️ Skipping invalid email: {email}")
