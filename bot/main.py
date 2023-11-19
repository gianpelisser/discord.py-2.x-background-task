# Imports
import settings
import discord
from discord.ext import commands
import mysql.connector
import asyncio
from datetime import datetime, timedelta
import json
# import os
# import schedule
# import time
# import sqlalchemy

# Log (Logger)
logger = settings.logging.getLogger("bot")


# MySQL: Verificar Players Online
def check_sql_players_on():
    myconexao = mysql.connector.connect(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_pass,
        database=settings.mysql_mydb)

    # Criar uma sessão para o mysql
    mycursor = myconexao.cursor()

    # consulta SQL
    mycursor.execute("SELECT isAvailable, usersOnline FROM teraapi.server_info WHERE serverId = 2800")
    # mycursor.execute("SELECT * FROM teraapi.server_info WHERE serverId = 2800")

    # Obter nomes das colunas
    columns = [column[0] for column in mycursor.description]

    # Resultado(s) da consulta
    row_resultados = mycursor.fetchone()

    # Combina os nomes das colunas com os valores
    resultado_dict = dict(zip(columns, row_resultados))

    myconexao.close()
    return resultado_dict


def check_players_on():
    sql_result = check_sql_players_on()

    try:
        # Carregar os dados atuais do JSON: storage_data.json
        data = load_data_from_json()

        # Atualizar os valores
        data['vortex_tera']['server_status'] = 'Online' if sql_result['isAvailable'] else 'Offline'
        data['vortex_tera']['players_online'] = sql_result['usersOnline']

        # Salvar os dados atualizados
        save_data_to_json(data)
    except Exception as e:
        print(e)
        pass

    if sql_result['isAvailable'] == 1:
        players_online = sql_result['usersOnline']
        ch_name_att = f"Players Online: {players_online}"
        print(ch_name_att)
        return ch_name_att
    else:
        ch_name_att = f"Servidor Offline: 0"
        print(ch_name_att)
        return ch_name_att


# Função para salvar os dados no arquivo JSON
def save_data_to_json(data):
    with open('storage_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)
    print("Dados atualizados em storage_data.json")


# Função para obter os dados do arquivo JSON
def load_data_from_json():
    with open('storage_data.json', 'r') as json_file:
        data = json.load(json_file)
    return data


class Clientbot(commands.Bot):
    def __init__(self, *args, **kwargs):

        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=settings.bot_prefix, intents=intents, help_command=None)
        # super().__init__(*args, **kwargs)
        self.synced = False  # we use this so the bot doesn't sync commands more than once
        self.bg_task = None

        # Start empty Cogs
        self.initial_extensions = []

        # Carregar as cogs
        for cog_file in settings.COGS_DIR.glob("*.py"):
            if not cog_file.name.startswith("__"):
                try:
                    cog = f'cogs.{cog_file.name[:-3]}'
                    self.initial_extensions.append(cog)
                    print(f"COG encontrada: [ {cog_file.name[:-3]} ]")
                except Exception as e:
                    print(f"COG erro: [ {cog_file.name[:-3]} ] Error: {e}")

    async def setup_hook(self) -> None:
        self.bg_task = self.loop.create_task(self.my_background_task())

        try:
            for extension in self.initial_extensions:
                await self.load_extension(extension)
                print(f'Cog Loaded: {extension}')
            if not self.synced:
                try:
                    synced_count = await self.tree.sync()
                    # synced_count = await self.tree.sync(guild=discord.Object(id=guild_id))  # for specific guild
                    print(f"[ {len(synced_count)} ] synchronized command(s).")
                except Exception as e:
                    print(f"Error syncing command(s): {e}")
                self.synced = True
        except Exception as e:
            print(e)

    async def my_background_task(self):
        await self.wait_until_ready()
        try:
            ch_id_players_on = settings.discord_ch_id_players_on
            channel_players_online = self.get_channel(int(ch_id_players_on))  # pega o chat pelo id
            if channel_players_online:
                while not self.is_closed():
                    # novo nome
                    att_ch_name = check_players_on()

                    # Edita o nome do chat
                    await channel_players_online.edit(name=att_ch_name)
                    print(f"Canal ID: {ch_id_players_on} Atualizado:")
                    print(att_ch_name)

                    # Obter a data e hora atual
                    now = datetime.now()
                    future_time = now + timedelta(minutes=10)  # referente ao proximo update

                    # Formatar a data e hora no formato desejado (dia/mês/ano - hora:minuto)
                    formatted_datetime = now.strftime("%d/%m/%Y - %H:%M:%S")

                    # Formatar a nova hora no formato desejado
                    formatted_future_time = future_time.strftime("%d/%m/%Y - %H:%M:%S")

                    # Imprimir os resultados no console
                    print("Atualizado agora:", formatted_datetime)
                    print(f"Próximo update: {formatted_future_time}")

                    # Aguarda 10 minutos para atualizar: em segundos
                    await asyncio.sleep(600)
            else:
                print(f"Canal ID: {ch_id_players_on} Não encontrado.")
        except Exception as e:
            print(e)

    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral=True)

    async def on_ready(self):
        await self.wait_until_ready()

        print('-=-' * 7, '[ VORTEX LAB - Development ]', '-=-' * 7)
        logger.info(f"User: {self.user} | ID: {self.user.id}")
        print(f"BOT: {self.user.name} | Online.")
        print('-=-' * 10, '[ Vortex TERA ]', '-=-' * 10)
        print()

        # Carregar CMDS (Comandos)
        for cmd_file in settings.CMDS_DIR.glob("*.py"):
            if cmd_file.name != "__init__.py":
                try:
                    await self.load_extension(f"cmds.{cmd_file.name[:-3]}")
                    print(f"CMD carregado: [ {cmd_file.name[:-3]} ]")
                except Exception as e:
                    print(f"CMD erro: [ {cmd_file.name[:-3]} ] Error: {e}")


bot = Clientbot()


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return


@bot.command()
async def load(ctx, cog: str):
    try:
        await bot.load_extension(f"cogs.{cog.lower()}")
        await ctx.send(f"**Cog:** ``{cog.lower()}`` Carregada com sucesso!")
    except:
        await ctx.send(f"**A cog:** ``{cog.lower()}`` já esta carregada.\n"
                       f"Use o comando ``!unload {cog.lower()}`` para remover.")


@bot.command()
async def unload(ctx, cog: str):
    try:
        await bot.unload_extension(f"cogs.{cog.lower()}")
        await ctx.send(f"**Cog:** ``{cog.lower()}`` Removida com sucesso!")
    except:
        await ctx.send(f"**A cog:** ``{cog.lower()}`` não esta carregada.\n"
                       f"Use o comando ``!load {cog.lower()}`` para carregar.")


@bot.command()
async def reload(ctx, cog: str):
    try:
        await bot.reload_extension(f"cogs.{cog.lower()}")
        await ctx.send(f"**Cog:** ``{cog.lower()}`` Re-carregando com sucesso!")
    except Exception as e:
        await ctx.send(f"erro ao re-carregar a cog: ``{cog.lower()}``"
                       f"\nErro: {e}")


@bot.command(
    aliases=['p'],
    help="Responde com Pong!",
    description="Descrição do comando ping",
    enabled=True,
    hidden=True
)
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command(
    aliases=['say'],
    help="Responde (fala) com sua mensagem",
    description="Descrição do comando fale",
    enabled=True,
    hidden=True
)
async def fale(ctx, *what):
    await ctx.send(" ".join(what))


if __name__ == "__main__":
    # Inicia o BOT
    bot.run(settings.discord_api_token, root_logger=True)
