import os
import requests
from flask import current_app

def enviar_email_cadastro(username):
    prontuario = "PT3026159"
    nome_aluno = "André Rufino Papaleo"
    
    destinatarios = [
        "flaskaulasweb@zohomail.com",
        "a.papaleo@aluno.ifsp.edu.br"
    ]
    
    assunto = f"Novo Usuário Cadastrado: {username}"
    conteudo = f"""
    Novo usuário cadastrado na aplicação Flasky!
    
    - Aluno: {nome_aluno}
    - Prontuário: {prontuario}
    - Usuário cadastrado: {username}
    """
    
    sendgrid_api_key = os.environ.get('SENDGRID_API_KEY') or current_app.config.get('SENDGRID_API_KEY')
    remetente = os.environ.get('MAIL_DEFAULT_SENDER') or current_app.config.get('MAIL_DEFAULT_SENDER', 'flaskaulasweb@zohomail.com')
    
    if not sendgrid_api_key:
        print("Erro: SENDGRID_API_KEY não configurada.")
        return

    url = "https://api.sendgrid.com/v3/mail/send"
    
    for dest in destinatarios:
        payload = {
            "personalizations": [
                {
                    "to": [{"email": dest}],
                    "subject": assunto
                }
            ],
            "from": {"email": remetente},
            "content": [
                {
                    "type": "text/plain",
                    "value": conteudo
                }
            ]
        }
        
        headers = {
            "Authorization": f"Bearer {sendgrid_api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code not in [200, 201, 202]:
                print(f"Erro ao enviar e-mail para {dest}: {response.text}")
        except Exception as e:
            print(f"Exceção ao enviar e-mail: {e}")