from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
import os
#from fp.fp import FreeProxy

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/elpais", methods=['GET', 'POST'])
def elpais():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
    url = request.args['url']
    if url.startswith("https://www."):
        url = url
    else:
        url = url[:8] + "www." + url[8:]
    source = requests.get(url, headers=headers)
    html_text = source.text
    soup = BeautifulSoup(html_text,"lxml")

    if url.split(".")[1] == "elpais":
        logo = os.listdir('/home/adriansdls/mysite/static/images')
        article = soup.find("article")
        titulo = article.header.div.h1.text
        subtitulo = article.header.div.h2.text
        img_url = soup.find("head").find_all("meta", attrs={'property': 'og:image'})[0]["content"]
        parrafos = article.find_all("p")
        textos = []
        for i in parrafos:
            texto = i.text
            textos.append(texto)
        return render_template('elpais.html', titulo = titulo, subtitulo = subtitulo, img_url = img_url, textos = [(i.text + os.linesep) for i in parrafos][:-1], autor = [(i.text + os.linesep) for i in parrafos][-1],len = len(textos), texto = texto )

    elif url.split(".")[1] == "lavanguardia":
        logo = os.listdir('/home/adriansdls/mysite/static/images')
        article = soup.main.find("div", class_="main-article-container").article
        titulo = article.div.find("div", class_="row").header.div.div.h1.text
        subtitulo = article.div.find("div", class_="row").header.div.find("div", class_="epigraph-container").h2.text
        img_url = soup.find("head").find_all("meta", attrs={'property': 'og:image'})[0]["content"]
        parrafos = soup.find("div", class_="article-modules").find_all("p")
        textos = []
        for i in parrafos:
            texto = i.text
            textos.append(texto)
        return render_template('lavanguardia.html', logo = logo, titulo = titulo, subtitulo = subtitulo, img_url = img_url, textos = [(i.text + os.linesep) for i in parrafos],len = len(textos), texto = texto )

    else:
        pass