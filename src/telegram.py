import os
import argparse
from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterVideo

# Configuração para captura de parâmetros via linha de comando
parser = argparse.ArgumentParser(description='Baixar vídeos de um canal do Telegram')
parser.add_argument('--api_id', required=True, type=int, help='ID da API do Telegram')
parser.add_argument('--api_hash', required=True, type=str, help='Hash da API do Telegram')
parser.add_argument('--phone_number', required=True, type=str, help='Número de telefone associado à conta do Telegram')
parser.add_argument('--channel_username', required=True, type=str, help='Nome de usuário ou ID do canal do Telegram')
args = parser.parse_args()

# Captura dos valores a partir das flags
api_id = args.api_id
api_hash = args.api_hash
phone_number = args.phone_number
channel_username = args.channel_username

# Diretório para salvar os vídeos
save_path = 'videos/'

# Crie o diretório se não existir
os.makedirs(save_path, exist_ok=True)

# Inicie o cliente
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone_number)

    # Obtenha o ID do canal
    channel = await client.get_entity(channel_username)

    # Baixe as mensagens com arquivos de mídia (vídeos)
    async for message in client.iter_messages(channel, filter=InputMessagesFilterVideo, reverse=True):
        if message.video:
            file_path = await client.download_media(message, save_path)
            print(f'Video baixado em: {file_path}')

with client:
    client.loop.run_until_complete(main())
