import imaplib
import email
import smtplib
import time
import os
import re
from email.header import decode_header
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.generativeai as genai

# Load credentials from environment variables for security
EMAIL = os.getenv("GMAILAI_EMAIL", "")
APP_PASSWORD = os.getenv("GMAILAI_APP_PASSWORD", "")
GEMINI_API_KEY = os.getenv("GMAILAI_GEMINI_API_KEY", "")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Default Prompt Template
DEFAULT_PROMPT_TEMPLATE = """
You are GmailAI.

Draft ONLY the email content between <p>...</p> tags without <html> or <body> tags.

Start with:
- Dear {sender_name},

End with:
- Regards,
- GmailAI

Do NOT include any <html>, <head>, or <body> tags.

Here is the email to reply to:

{email_body}
"""

def clean_subject(subject):
    decoded = decode_header(subject)[0]
    if isinstance(decoded[0], bytes):
        return decoded[0].decode(decoded[1] or "utf-8", errors="ignore")
    return decoded[0]

def extract_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition"))
            if "attachment" in disposition:
                continue  # Skip attachments
            try:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    decoded_payload = payload.decode(charset, errors="ignore")
                    if content_type == "text/html":
                        return BeautifulSoup(decoded_payload, "html.parser").get_text()
                    elif content_type == "text/plain" and not body:
                        body = decoded_payload
            except Exception as e:
                continue
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            body = payload.decode(charset, errors="ignore")
    return body.strip()

def get_sender_name(sender):
    name, _ = email.utils.parseaddr(sender)
    return name if name else "there"

def get_html_response_from_gemini(email_body, sender_name):
    prompt = DEFAULT_PROMPT_TEMPLATE.format(sender_name=sender_name, email_body=email_body)

    try:
        response = model.generate_content(prompt)
        ai_message = response.text.strip()

        # Clean unwanted markdown
        ai_message = re.sub(r"^```(?:html)?", "", ai_message, flags=re.IGNORECASE).strip()
        ai_message = re.sub(r"```$", "", ai_message).strip()

        html_template = f"""
        <html>
        <head>
        <style>
            :root {{
                --bg-light: #f4f4f7;
                --bg-dark: #1e1e2f;
                --text-light: #333;
                --text-dark: #ddd;
                --container-light: #fff;
                --container-dark: #2c2c3e;
                --accent: #4f46e5;
                --button-light: #4f46e5;
                --button-dark: #8f94fb;
                --gradient-light: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
                --gradient-dark: linear-gradient(135deg, #4e54c8 0%, #8f94fb 100%);
            }}
            @media (prefers-color-scheme: dark) {{
                body {{ background-color: var(--bg-dark); color: var(--text-dark); }}
                .email-container {{ background: var(--container-dark); }}
                p {{ color: var(--text-dark); }}
                .email-header {{ background: var(--gradient-dark); }}
                .email-button {{ background-color: var(--button-dark); }}
                .email-footer {{ background-color: #1c1c2e; }}
            }}
            body {{
                font-family: 'Helvetica Neue', Arial, sans-serif;
                background-color: var(--bg-light);
                margin: 0;
                padding: 0;
                color: var(--text-light);
            }}
            .email-container {{
                max-width: 600px;
                margin: 40px auto;
                background: var(--container-light);
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}
            .email-header {{
                background: var(--gradient-light);
                padding: 20px 30px;
                text-align: center;
            }}
            .email-header img {{
                max-width: 120px;
                height: auto;
            }}
            .email-header h1 {{
                margin: 10px 0 0 0;
                font-size: 24px;
                color: white;
            }}
            .email-body {{
                padding: 30px 40px;
            }}
            p {{
                font-size: 17px;
                line-height: 1.6;
            }}
            .email-button {{
                display: inline-block;
                background-color: var(--button-light);
                color: white;
                padding: 12px 24px;
                border-radius: 6px;
                text-decoration: none;
                margin-top: 20px;
                font-weight: bold;
            }}
            .email-footer {{
                background-color: #f0f0f5;
                text-align: center;
                padding: 20px 10px;
                font-size: 14px;
            }}
            .social-icons {{
                margin: 10px 0;
            }}
            .social-icons a {{
                margin: 0 8px;
            }}
            .social-icons img {{
                width: 28px;
                height: 28px;
                transition: transform 0.3s;
            }}
            .social-icons img:hover {{
                transform: scale(1.2);
            }}
        </style>
        </head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <img src="https://raw.githubusercontent.com/tempgit6969/GmailAILogo/main/WhatsApp%20Image%202025-04-20%20at%2018.08.10_67815e29.jpg
                    " alt="Company Logo">
                    <h1>GmailAI</h1>
                </div>
                <div class="email-body">
                    {ai_message}
                    <div style="text-align: center;">
                        <a href="#" class="email-button">View More</a>
                    </div>
                </div>
                <div class="email-footer">
                    <div class="social-icons">
                        <a href="#"><img src="https://cdn-icons-png.flaticon.com/512/733/733635.png" alt="Twitter"></a>
                        <a href="#"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn"></a>
                        <a href="#"><img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" alt="Facebook"></a>
                    </div>
                    <p>© 2025 GmailAI. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_template

    except Exception as e:
        print("❌ Gemini Error:", e)
        return """
        <html><body>
        <p><b>Sorry, the AI could not generate a proper response.</b></p>
        </body></html>
        """

def send_html_reply(to_email, subject, html_content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Re: " + subject
    msg["From"] = f"GmailAI <{EMAIL}>"
    msg["To"] = to_email

    html_part = MIMEText(html_content, "html")
    msg.attach(html_part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, APP_PASSWORD)
            server.sendmail(EMAIL, to_email, msg.as_string())
        print(f"✅ Replied to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")

def fetch_unread_emails():
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(EMAIL, APP_PASSWORD)
        imap.select("inbox")

        status, messages = imap.search(None, "UNSEEN")
        email_ids = messages[0].split()

        if email_ids:
            print(f"\n📬 Found {len(email_ids)} unread emails.")

            for eid in email_ids:
                _, msg_data = imap.fetch(eid, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])

                sender = msg["From"]
                sender_email = email.utils.parseaddr(sender)[1]
                sender_name = get_sender_name(sender)
                subject = clean_subject(msg["Subject"] or "")
                body = extract_body(msg)

                print("\n====== New Unread Email ======")
                print("From:", sender)
                print("Subject:", subject)
                print("Body Preview:", body[:150])

                if sender_email.endswith("@gmail.com"):
                    print("✅ Gmail sender detected. Generating reply...")
                    html_reply = get_html_response_from_gemini(body, sender_name)
                    send_html_reply(sender_email, subject, html_reply)
                else:
                    print("⏭️ Skipping non-Gmail sender:", sender_email)

        imap.logout()
    except Exception as e:
        print("❌ Error fetching emails:", e)

if __name__ == "__main__":
    print("\n🚀 GmailAI Auto-Responder Running...\n")
    while True:
        fetch_unread_emails()
        time.sleep(5)  # Check every 5 seconds
