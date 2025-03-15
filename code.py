import os
import PyPDF2
from openai import OpenAI

def ler_pdf(caminho_arquivo):
    # Abrir o arquivo PDF em modo de leitura binária
    with open(caminho_arquivo, 'rb') as arquivo:
        leitor_pdf = PyPDF2.PdfReader(arquivo)
        
        # Inicializar uma string vazia para o texto do PDF
        texto_completo = ''
        
        # Iterar sobre cada página do PDF
        for pagina in leitor_pdf.pages:
            # Extrair o texto da página
            texto_pagina = pagina.extract_text()
            texto_completo += texto_pagina if texto_pagina is not None else ''
        
        return texto_completo

def enviar_para_openai(mensagem, contexto, client):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": contexto},
            {"role": "user", "content": mensagem}
        ],
        model="gpt-3.5-turbo", # Selecione o modelo de LLM da OpenAI que irá utilizar
    )
    return chat_completion.choices[0].message.content

def iniciar_conversa(resumo):
    client = OpenAI(api_key="XXXXXXXX") # Insira sua própria API KEY da OpenAI
    contexto = "O seguinte é um resumo do documento:\n\n" + resumo

    print("Resumo do documento:\n")
    print(resumo)
    print("\nVocê pode agora fazer perguntas sobre o documento.")

    while True:
        pergunta = input("\nFaça uma pergunta sobre o documento (ou digite 'sair' para encerrar): ")
        if pergunta.lower() == 'sair':
            break
        resposta = enviar_para_openai(pergunta, contexto, client)
        print("\nResposta:", resposta)
   

# Exemplo de uso
caminho_do_pdf = 'C:/apolice.pdf'  # Substitua com o caminho do seu arquivo
texto_pdf = ler_pdf(caminho_do_pdf)
resumo = enviar_para_openai("Resuma o seguinte texto:\n\n" + texto_pdf, "", OpenAI(api_key="XXXXXXXX")) # Insira sua própria API KEY da OpenAI
iniciar_conversa(resumo)
