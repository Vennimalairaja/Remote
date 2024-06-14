from os import remove
from api import api_key
from telegram import Update
import checkout
from telegram.ext import ApplicationBuilder,ContextTypes,CommandHandler,MessageHandler,filters
user_pswd=""
conn=checkout.Connection
is_connected=False
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi just checking out!")
async def connect(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if len(update.message.text)<=8:
        await update.message.reply_text("Use the connect command like '/connect username password' ")
    else:
        data = update.message.text.split(" ")
        global user_pswd
        user_pswd = data[1:]
        print(user_pswd)
        var = conn.remote_connect(ip="ip_address", username=user_pswd[0], password=user_pswd[1])
        global is_connected
        is_connected=True
        await update.message.reply_text(var)
async def data(update:Update,context:ContextTypes.DEFAULT_TYPE):
    print(update.message.text)


async def list(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if not is_connected:
        await update.message.reply_text("Connect panitu vada punda!")
    else:
        data = handler("list")
        for i in data:
            await update.message.reply_text(i)

async def close(update:Update,context:ContextTypes.DEFAULT_TYPE):
    global is_connected
    if not is_connected:
        await update.message.reply_text("Connect pannama ena maithuku close panna vantha")
    else:
        await update.message.reply_text(handler("close"))

        is_connected=False

async def change(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if not is_connected:
        await update.message.reply_text("Connect panitu vada ")
    else:
        if len(update.message.text) <= 7:
            await update.message.reply_text("Use the command like '/change Foldername' ")
        else:
            directory = update.message.text.split(" ")
            val = handler(directory[0], directory[1])
            await update.message.reply_text(val)


async def download(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if not is_connected:
        await update.message.reply_text("Otha connect panitu vada!")
    else:
        if len(update.message.text) <= 9:
            await update.message.reply_text("Use the command in the format '/download filename' ")
        else:
            filename = update.message.text[10:]
            var = conn.get_file(filename)
            if var == False:
                await update.message.reply_text("Check your filename and check the current directory!")
            else:
                await update.message.reply_document(filename)
                remove(filename)

    #await update.message.reply_document(filename)
    #remove(filename)

def handler(text:str,directory:str=None):
    if text=="list":
        data=conn.list_dir()
        return data
    elif text=="close":
        conn.close()
        return "Closed successfully!"
    elif text=="/change" and directory!=None:
        return conn.change(directory)




# conn=checkout.Connection("192.168.9.204",user_pswd[0],user_pswd[1])
if __name__=="__main__":
    app=ApplicationBuilder().token(api_key).build()
    app.add_handler(CommandHandler('start',start))
    app.add_handler(CommandHandler('connect',connect))
    app.add_handler(CommandHandler('list',list))
    app.add_handler(CommandHandler('close',close))
    app.add_handler(CommandHandler('change',change))
    app.add_handler(CommandHandler('download',download))
    app.add_handler(MessageHandler(filters.TEXT,data))
    #app.add_handler(MessageHandler(filters.TEXT,data))
    app.run_polling()
    print(user_pswd)
