import smtplib, requests, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from openai import OpenAI

# 환경 변수 로드
NAVER_ID = os.environ.get("NAVER_ID")
NAVER_PW = os.environ.get("NAVER_PW")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def get_smart_news():
    domains = "techcrunch.com,wired.com,theverge.com"
    url = f"https://newsapi.org/v2/everything?q=Artificial Intelligence&domains={domains}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    # JSON 응답에서 기사 3개를 가져옴
    articles = requests.get(url).json().get('articles', [])[:3]
    
    # 💡 참고: 현재 코드에는 이 데이터를 HTML로 변환하거나 요약하는 로직이 필요합니다.
    # 예시로 제목만 합쳐서 반환하도록 구성했습니다.
    content = "<ul>"
    for a in articles:
        content += f"<li><a href='{a['url']}'>{a['title']}</a></li>"
    content += "</ul>"
    return content

def send_mail(content):
    msg = MIMEMultipart()
    msg['Subject'] = f"✉️ AI 뉴스 리포트 ({datetime.now().strftime('%m/%d')})"
    msg['From'] = f"{NAVER_ID}@naver.com"
    msg['To'] = RECEIVER_EMAIL
    msg.attach(MIMEText(content, 'html'))
    
    with smtplib.SMTP_SSL("smtp.naver.com", 465) as server:
        server.login(NAVER_ID, NAVER_PW)
        server.sendmail(msg['From'], msg['To'], msg.as_string())

if __name__ == "__main__":
    news_content = get_smart_news()
    send_mail(news_content)
