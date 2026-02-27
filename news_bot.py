import smtplib, requests, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from openai import OpenAI

NAVER_ID = os.environ.get("NAVER_ID")
NAVER_PW = os.environ.get("NAVER_PW")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def get_smart_news():
domains = "techcrunch.com,wired.com,theverge.com"
url = f" Intelligence&domains={domains}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
articles = requests.get(url).json().get('articles', [])[:3]

def send_mail(content):
msg = MIMEMultipart()
msg['Subject'] = f"✉️ AI 뉴스 리포트 ({datetime.now().strftime('%m/%d')})"
msg['From'] = f"{NAVER_ID}@naver.com"
msg['To'] = RECEIVER_EMAIL
msg.attach(MIMEText(content, 'html'))
with smtplib.SMTP_SSL("smtp.naver.com", 465) as server:
server.login(NAVER_ID, NAVER_PW)
server.sendmail(msg['From'], msg['To'], msg.as_string())

if name == "main":
send_mail(get_smart_news())
