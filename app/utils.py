
import json
from fpdf import FPDF
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv

load_dotenv()

email = os.getenv("email")
senha = os.getenv("senha")

def gerar_pdf(presentes):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Lista de Presença - COLETIVO DE ARTES INTEGRADAS OPERÁRIOS PELA ARTE", ln=True, align='C')

    data_atual = datetime.now().strftime('%d-%m-%Y %H h %M min %S s')
    pdf.set_font('Arial', '', 12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Data: {data_atual}", ln=True, align='L')

    for presente in presentes:
        nome = presente.get('nome', 'Desconhecido')
        data = data_atual
        pdf.cell(200, 10, txt=f"{nome} - {data}", ln=True, align='L')

    pasta_pdf = 'app/static/pdf'

    if not os.path.exists(pasta_pdf):
        os.makedirs(pasta_pdf)

    caminho_pdf = os.path.join(pasta_pdf, f"presencas_{data_atual.replace(' ', '_').replace(':', '-')}.pdf")
    pdf.output(caminho_pdf)
    return caminho_pdf

def enviar_email(pdf_path):
    with open('app/static/json/email.json', 'r') as f:
        emails = json.load(f)

    sender_email = email
    sender_password = senha
    data_atual = datetime.now().strftime('%d-%m-%Y %H h %M min %S s')

    for recipient_email in emails:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Lista de Presença - {data_atual}"

        body = f"Segue em anexo o PDF confirmando os presentes do dia: {data_atual}"
        msg.attach(MIMEText(body, 'plain'))

        with open(pdf_path, "rb") as f:
            attach_part = MIMEApplication(f.read(), _subtype="pdf")
            attach_part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_path))
            msg.attach(attach_part)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f"E-mail enviado para {recipient_email}!")
        except Exception as e:
            print(f"Erro ao enviar e-mail para {recipient_email}: {e}")

def carregar_membros():
    caminho_json = 'app/static/json/membros.json'
    with open(caminho_json, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)['membros']