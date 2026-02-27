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
    # 함수(def) 아래는 스페이스 4칸 들여쓰기
    domains = "techcrunch.com,wired.com,theverge.com"
    url = f"https://newsapi.org/v2/everything?q=Artificial Intelligence&domains={domains}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    articles = requests.get(url).json().get('articles', [])[:3]
    
    # (참고: 기존 코드에 뉴스 요약 로직이 빠져있어서 간단히 추가했습니다)
    news_html = "<h1>AI News</h1>"
    for art in articles:
        news_html += f"<p>{art['title']}</p>"
    return news_html

def send_mail(content):
    # 함수(def) 아래는 스페이스 4칸 들여쓰기
    msg = MIMEMultipart()
    msg['Subject'] = f"✉️ AI 뉴스 리포트 ({datetime.now().strftime('%m/%d')})"
    msg['From'] = f"{NAVER_ID}@naver.com"
    msg['To'] = RECEIVER_EMAIL
    msg.attach(MIMEText(content, 'html'))
    
    # with 문 아래는 한 번 더(총 8칸) 들여쓰기
    with smtplib.SMTP_SSL("smtp.naver.com", 465) as server:
        server.login(NAVER_ID, NAVER_PW)
        server.sendmail(msg['From'], msg['To'], msg.as_string())

# if문은 맨 앞에, 그 아래 실행문은 들여쓰기
if __name__ == "__main__":
    content = get_smart_news()
    send_mail(content)
