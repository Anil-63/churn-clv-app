import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ⚠️ Demo credentials — DO NOT use in production
from_email = "anil.kanakadandila630@gmail.com"
app_password = "jirk wrlc lvic mkqq"  # This must be your app-specific password (not Gmail password)

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

# Load final_outputs.csv
df = pd.read_csv("final_outputs.csv")

# Filter customers with churn probability ≥ 0.60 AND a valid email
target_customers = df[(df["Churn_Prob"] >= 0.60) & (df["Email"].notna())]

# Send emails
for _, row in target_customers.iterrows():
    send_promotional_email(
        to_email=row["Email"],
        customer_id=row["Customer_Id"],
        clv_value=row["Predicted_CLV"]
    )
