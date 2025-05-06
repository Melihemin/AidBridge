from fastapi import FastAPI, APIRouter, Depends, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from starlette import status
from sqlalchemy.orm import Session
from typing import Optional, Annotated, List
from datetime import datetime, timedelta, timezone

from starlette.responses import RedirectResponse

from database.settings import SessionLocal
from database.models import Person
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import Field, BaseModel, ConfigDict
import markdown
from bs4 import BeautifulSoup
from fastapi.responses import StreamingResponse
import csv
from io import StringIO
from datetime import datetime
from typing import Optional


class Aid_request(BaseModel):
    name: str
    surname: str
    age: int
    phone: str
    email: str
    address: str
    patients: int
    needs: str
    health_status: str
    shelter_status: str

    # Bu Pydantic modelini FastAPI'ye uygun hale getirmek için Form kullanacağız
    def __init__(
        self,
        name: str = Form(..., max_length=100, min_length=1),
        surname: str = Form(..., max_length=100, min_length=1),
        age: int = Form(..., gt=0, lt=120),
        phone: str = Form(..., max_length=100, min_length=1),
        email: str = Form(..., max_length=100, min_length=1),
        address: str = Form(..., min_length=10),
        patients: int = Form(..., gt=-1),
        needs: str = Form(..., min_length=1),
        health_status: str = Form(...),
        shelter_status: str = Form(...),
    ):
        super().__init__(
            name=name,
            surname=surname,
            age=age,
            phone=phone,
            email=email,
            address=address,
            patients=patients,
            needs=needs,
            health_status=health_status,
            shelter_status=shelter_status,
        )

templates = Jinja2Templates(directory="templates")

def connect():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(connect)]

router = APIRouter(
    prefix="/aid",
    tags=["Aid"],
)

def markdown_to_text(markdown_text):
    html = markdown.markdown(markdown_text)
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    return text

def calculate_score(request: Aid_request) -> int:
    load_dotenv()
    genai.configure(api_key=os.getenv("GENAI_API_KEY"))
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    response = llm.invoke(
        [
            HumanMessage(content=f"""
                    Aşağıdaki yardım talebini değerlendir ve 1-100 arasında bir öncelik skoru ver:
                
                    Yaş: {request.age}
                    Sağlık Durumu: {request.health_status}
                    Barınma Durumu: {request.shelter_status}
                    Yanındaki Kişi Sayısı: {request.patients}
                    İhtiyaçlar: {request.needs}
                    Adres: {request.address}
                
                    Değerlendirme kriterleri:
                    0. Adrese göre araştırma yap eğer son büyük depremlerden bir tanesi cok yakın zamanda orada olduysa öncelik tanı.
                    1. Yaş (18 yaş altı ve 65 yaş üstü daha yüksek öncelik)
                    2. Sağlık durumu (kronik hastalık, engel, acil durumlar daha yüksek öncelik)
                    3. Barınma durumu (hasarlı, güvensiz, dışarıda olanlar daha yüksek öncelik)
                    4. Yanındaki kişi sayısı (özellikle çocuk ve yaşlı varsa daha yüksek öncelik)
                    5. İhtiyaçlar (gıda, su, ilaç gibi temel ihtiyaçlar daha yüksek öncelik)
                    
                    Not: Net ve kesin bilgiler düşün boş bırakılan alanlar ile ilgili öncelik tanıma.
                
                    Lütfen sadece 1-100 arasında bir sayı döndür ve kısa bir açıklama yap.
                    """),

         ]
    )
    return markdown_to_text(response.content)

@router.get("/")
async def aid(request: Request ,db: db_dependency):
    try:

        result = db.query(Person).all()
        return templates.TemplateResponse("aid_list.html", {"result" : result, "request" : request})

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/create")
async def create_aid(request: Request):
    return templates.TemplateResponse("new_aid.html", {"request" : request})

@router.post("/new")
async def new_aid(db: db_dependency, aid_request: Aid_request):
    try:
        # Burada gelen verileri kullanarak Person modelini oluşturabilirsiniz
        request = Person(
            name=aid_request.name,
            surname=aid_request.surname,
            age=aid_request.age,
            phone=aid_request.phone,
            patients=aid_request.patients,
            email=aid_request.email,
            address=aid_request.address,
            needs=aid_request.needs,
            health_status=aid_request.health_status,
            shelter_status=aid_request.shelter_status
        )
        db.add(request)
        db.commit()

        return templates.TemplateResponse("aid_list.html", {"request": request})

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/create_request")
async def create_new_aid(db: db_dependency,
                         name: str = Form(...),
                         surname: str = Form(...),
                         age: int = Form(...),
                         phone: str = Form(...),
                         email: str = Form(...),
                         address: str = Form(...),
                         patients: int = Form(...),
                         needs: str = Form(...),
                         health_status: str = Form(...),
                         shelter_status: str = Form(...)):
    try:
        # Creating a new aid request entry in the database
        new_request = Person(
            name=name,
            surname=surname,
            age=age,
            phone=phone,
            email=email,
            address=address,
            patients=patients,
            needs=needs,
            health_status=health_status,
            shelter_status=shelter_status,
            score=None,  # Not calculated here, but can be set later
            explanation=None,  # Not calculated here, but can be set later
            date_created=datetime.now()
        )

        response_text = calculate_score(new_request)
        # Skoru ve açıklamayı ayır
        score_text = response_text.split('\n')[0]
        explanation = '\n'.join(response_text.split('\n')[1:])

        new_request.score = score_text
        new_request.explanation = explanation
        # Adding and committing the new request to the database
        db.add(new_request)
        db.commit()
        db.refresh(new_request)

        # Redirect to the list of aid requests after successful submission
        return RedirectResponse(url="/aid", status_code=303)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error processing the request")


@router.get("/high_priority")
async def high_priority(db: db_dependency):

    hp_data = db.query(Person).filter(Person.score >= 70).all()
    return hp_data


@router.get("/donate")
async def donate(request: Request,db: db_dependency):
    return templates.TemplateResponse("donate.html", {"request": request})

@router.get("/export-csv")
async def export_aid_requests_csv(db: db_dependency):
    requests = db.query(Person).all()

    # UTF-8 BOM ile başlat (Excel'de Türkçe karakter problemi çözülür)
    output = StringIO()
    output.write('\ufeff')  # <-- BOM EKLENDİ

    writer = csv.writer(output)

    # CSV başlıkları (tam Türkçe ve okunabilir şekilde)
    writer.writerow([
        'ID',
        'İsim',
        'Soyisim',
        'Yaş',
        'Telefon',
        'E-posta',
        'Adres',
        'Sağlık Durumu',
        'Barınma Durumu',
        'Kişi Sayısı',
        'İhtiyaçlar',
        'Durum',
        'Öncelik Skoru',
        'Açıklama',
        'Oluşturulma Tarihi'
    ])

    # Her talep için satır ekle
    for request in requests:
        writer.writerow([
            request.id,
            request.name,
            request.surname,
            request.age,
            request.phone,
            request.email,
            request.address,
            request.health_status,
            request.shelter_status,
            request.patients,
            request.needs,
            request.status,
            request.score,
            request.explanation,
            request.date_created.strftime('%Y-%m-%d %H:%M:%S'),
        ])

    output.seek(0)
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            'Content-Disposition': f'attachment; filename=yardim_talepleri_{current_time}.csv'
        }
    )

"""
{
  "name": "Melih Emin",
  "surname": "Kilicoglu",
  "age": 20,
  "phone": "5050083766",
  "email": "melihemin10@gmail.com",
  "address": "Gaziantep Sahinbey akkent mahallesi",
  "patients": 3,
  "needs": "su bot giysi ekmek",
  "health_status": "fanenjit astim reflu",
  "shelter_status": "evimiz saglam ama korkuyorum"
}


1. **İçerik Moderasyonu**:
    - Uygunsuz içerikleri tespit eder
    - Spam ve dolandırıcılık girişimlerini engeller
"""

