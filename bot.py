# Import delle librerie necessarie
import telebot
from random import randint
import csv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Token del bot Telegram (da sostituire con il proprio token)
TOKEN = "TOKEN"
# Inizializzazione del bot con il token e impostazione del parse mode HTML
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Percorso del file CSV contenente i dati per il bot
myfilepath = "out.csv"
# Variabili globali per tenere traccia della linea casuale e della risposta
random_line = 0
response = ""

# Funzione per creare e restituire la tastiera personalizzata
def keyboard(key_type="Scramble"):
    # Inizializza la tastiera con larghezza di riga 1 (default)
    markup = ReplyKeyboardMarkup(row_width=1)
    
    # Configura la tastiera a seconda del tipo specificato
    if key_type == "Scramble":
        markup = ReplyKeyboardMarkup(row_width=2)
        markup.add(KeyboardButton("Scramble"), KeyboardButton("Done"))
    elif key_type == "Solution":
        markup = ReplyKeyboardMarkup(row_width=2)
        markup.add(KeyboardButton("Solution"), KeyboardButton("Done"))
    elif key_type == "Done":
        markup = ReplyKeyboardMarkup(row_width=2)
        markup.add(KeyboardButton("Scramble"), KeyboardButton("Done"))
    else:
        markup.add(KeyboardButton("Start"))
    
    return markup

# Gestore dei messaggi per il comando /start
@bot.message_handler(commands=["start"])
def start_message(message):
    # Invia un messaggio di benvenuto con la tastiera iniziale
    bot.send_message(message.chat.id, "Welcome to HTR trainer.", reply_markup=keyboard())

# Gestore dei messaggi per qualsiasi messaggio ricevuto
@bot.message_handler(func=lambda message: True)
def all_messages(message):
    # Gestione del comando /done per interrompere il training
    if message.text == "Done" or message.text == "/done":
        # Rimuove la tastiera e invia un messaggio di conferma
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "Done training.", reply_markup=markup)
    
    # Gestione del comando /scramble per generare un nuovo stato
    elif message.text == "Scramble" or message.text == "/scramble":
        global random_line
        # Genera un numero casuale per selezionare una riga nel file CSV
        random_line = randint(0, 275)
        global response
        response = ''
        # Apre il file CSV e cerca la riga corrispondente al numero casuale
        with open(myfilepath) as cards:
            csv_reader = csv.reader(cards)
            for index, row in enumerate(csv_reader):
                if index == random_line:
                    # Costruisce la risposta formattata con dati dal CSV
                    response = 'Optimal HTR: <span class=\"tg-spoiler\">' + str(row[2]).zfill(2) + '</span>\n'
                    response += 'Solutions found: <span class=\"tg-spoiler\">' + str(row[3]).zfill(3) + '</span>\n\n'
                    response += 'Scramble: ' + row[0] + '\nPress to see the solution.'
        # Invia la risposta al mittente con la tastiera per visualizzare la soluzione
        bot.send_message(message.from_user.id, response, reply_markup=keyboard("Solution"))
    
    # Gestione del comando /solution per ottenere la soluzione dello scramble
    elif message.text == "Solution" or message.text == "/solution":
        # Apre il file CSV e cerca la riga corrispondente al numero casuale
        with open(myfilepath) as cards:
            csv_reader = csv.reader(cards)
            for index, row in enumerate(csv_reader):
                if index == random_line:
                    # Estrae e formatta la soluzione dal CSV
                    response2 = row[1]
                    response2 = response2.replace("\\n", "\n")
                    response2 += '\nPress to continue.'
        # Invia la soluzione al mittente con la tastiera per terminare
        bot.send_message(message.from_user.id, response2, reply_markup=keyboard("Done"))
    
    # Gestione del comando /start per iniziare un nuovo training
    elif message.text == "Start" or message.text == "/start":
        # Invia un messaggio per generare un nuovo scramble con la relativa tastiera
        bot.send_message(message.from_user.id, "Press to get new scramble.", reply_markup=keyboard("Scramble"))
    
    # Gestione del comando /help per mostrare le istruzioni
    elif message.text == "Help" or message.text == "/help":
        # Invia un messaggio di aiuto con le istruzioni per l'uso del bot
        bot.send_message(message.chat.id, "This bot is going to help you practice HTR solutions given a DR state.\n\n"
                                          "Write /start to start training.\n"
                                          "Write /scramble to generate new DR state.\n"
                                          "Write /solution to get the solutions of the previous scramble.\n"
                                          "Write /done if you are done training.")
    else:
        # Se il messaggio non corrisponde a nessun comando noto, lo invia al mittente
        bot.send_message(message.chat.id, message.text)

# Avvia il bot in modalità polling infinita con timeout e long polling timeout specificati
bot.infinity_polling(timeout=10, long_polling_timeout=5)
