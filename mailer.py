import smtplib
from email.message import EmailMessage
import pandas as pd

EMAIL = "yourgmail@gmail.com"
PASSWORD = "your_app_password"

df = pd.read_csv("jobs.csv")

for index, row in df.iterrows():

    recruiter_email = row["recruiter_email"]

    msg = EmailMessage()

    msg["Subject"] = f"Application for {row['title']}"

    msg["From"] = EMAIL

    msg["To"] = recruiter_email

    msg.set_content(f"""
Hello Recruiter,

I hope you are doing well.

I am interested in the {row['title']} role at {row['company']}.

Please find my resume attached.

Regards,
Justin Joseph
""")

    with open("resume.pdf", "rb") as f:

        file_data = f.read()

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="pdf",
        filename="resume.pdf"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login(EMAIL, PASSWORD)

        smtp.send_message(msg)

    print(f"Email sent to {recruiter_email}")