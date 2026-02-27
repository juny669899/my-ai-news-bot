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
    url = f"https://newsapi.org/v2/everything?q=Artificial Intelligence&domains={domains}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    
    response = requests.get(url)
    articles = response.json().get('articles', [])[:3]
    
    # 이메일 디자인 시작
    news_html = f"""
    <div style="font-family: 'Malgun Gothic', sans-serif; max-width: 600px; margin: auto; background-color: #f4f7fa; padding: 30px; border-radius: 20px;">
        <h2 style="color: #1a73e8; text-align: center; border-bottom: 2px solid #1a73e8; padding-bottom: 15px;">🤖 오늘의 AI 기술 뉴스 번역본</h2>
        <p style="text-align: center; color: #666; font-size: 14px;">{datetime.now().strftime('%Y년 %m월 %d일')} 리포트</p>
    """

    for art in articles:
        # GPT에게 더 상세한 번역과 요약을 요청하는 프롬프트
        prompt = f"""
        당신은 전문 번역가이자 기술 요약가입니다. 다음 뉴스 정보를 바탕으로 뉴스레터 내용을 작성해 주세요.
        
        1. 제목: 한국어로 멋지게 번역해줘.
        2. 내용 요약: 핵심 내용을 3~4문장 정도의 한글로 상세히 설명해줘.
        3. 주요 키워드: 뉴스에서 중요한 단어 2~3개를 뽑아줘.

        뉴스 제목: {art['title']}
        뉴스 내용: {art['description']}
        """
        
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        summary_result = res.choices[0].message.content.replace("\n", "<br>")

        # 뉴스 카드 디자인 (상세 내용 포함)
        news_html += f"""
        <div style="background: white; padding: 20px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
            <div style="font-size: 15px; color: #333; line-height: 1.8;">
                {summary_result}
            </div>
            <div style="margin-top: 15px; border-top: 1px solid #eee; padding-top: 15px;">
                <a href="{art['url']}" style="color: #1a73e8; text-decoration: none; font-weight: bold; font-size: 14px;">기사 원문 읽기 (영어) →</a>
            </div>
        </div>
        """
    
    return news_html + "</div>"

def send_mail(content):
    msg = MIMEMultipart()
    msg['Subject'] = f"✉️ [한글번역] AI 뉴스 리포트 ({datetime.now().strftime('%m/%d')})"
    msg['From'] = f"{NAVER_ID}@naver.com"
    msg['To'] = RECEIVER_EMAIL
    msg.attach(MIMEText(content, 'html'))
    
    with smtplib.SMTP_SSL("smtp.naver.com", 465) as server:
        server.login(NAVER_ID, NAVER_PW)
        server.sendmail(msg['From'], msg['To'], msg.as_string())

if __name__ == "__main__":
    try:
        email_body = get_smart_news()
        send_mail(email_body)
        print("✅ 한글 뉴스레터 발송 성공!")
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
