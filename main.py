from telegram.ext import *
#from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import requests
import pandas as pd
import mplfinance as mpf
import os
import yfinance as yf
from apscheduler.schedulers.blocking import BlockingScheduler
import sys
import random
import time

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

lista_empresas=["BOVA11.SA"]

if len(sys.argv) > 1:
  lista_empresas[0] = sys.argv[1]
else:
  print("Erro: nenhum argumento foi passado")

#sched = BlockingScheduler()
#@sched.scheduled_job("cron", day_of_week="sun", hour=14, minute=25)
#@sched.scheduled_job("cron", day_of_week="mon-fri", hour=21)
#def scheduled_job():

data=yf.download(lista_empresas, start="2023-10-01", interval="1wk")
#ticker = "BOVA11.SA"
#ativo = yf.Ticker(ticker)
#dados_semanais = ativo.history(period="max", interval="1wk")

df = pd.DataFrame.from_records(data)
#df = pd.DataFrame.from_dict(data, orient='index')
#df.index = pd.to_datetime(df.index)
first_values = df.tail(25).head(24).iloc[::1]

# Calcular o MACD
exp1 = first_values['Close'].ewm(span=12, adjust=False).mean()
exp2 = first_values['Close'].ewm(span=26, adjust=False).mean()
macd = exp1 - exp2
signal = macd.ewm(span=9, adjust=False).mean()
histogram = macd - signal

# Adicionar o MACD e o sinal ao DataFrame
first_values['MACD'] = macd
first_values['Signal'] = signal
first_values['Histogram'] = histogram

# Criar o gráfico
title = f"Histórico de Preços: {lista_empresas[0]}"
# Adicionar o MACD e o sinal ao gráfico com legendas
apds = [
    mpf.make_addplot(first_values[["Histogram"]], type="bar", panel=2, color="dimgray"),
    mpf.make_addplot(first_values[["MACD", "Signal"]],panel=0)
]

mpf.plot(
    first_values,
    type="candle",
    style="charles",
    title=title,
    volume=True,
    addplot=apds,
    savefig=f"/tmp/{lista_empresas[0]}.png",
)

time.sleep(random.randint(5, 30))

url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
files = {'photo': open(f"/tmp/{lista_empresas[0]}.png", 'rb')}
response = requests.post(url, files=files, data={'chat_id': TELEGRAM_CHAT_ID})
print(response.json())

#sched.start()
