import discord
from discord import app_commands
import logging
import voxrequest
import getenv


global settings
settings={}



#intents取得
intents = discord.Intents.default()
intents.message_content=True
intents.voice_states=True

#voicevox接続
voicevox = voxrequest.vox(getenv.voxurl)

class myClient(discord.Client):
    async def on_ready(self):
       print(f'接続成功\nユーザー名は {self.user}(id:{self.user.id})です。')
       await tree.sync()
       for i in range(len(client.guilds)):
           guild = client.guilds[i]
           await guild.voice_client.disconnect()
    async def on_app_command_completion(self, interaction:discord.Interaction, command:app_commands.Command):
        print(command.name)
        if command.name=="summon":
            self.ch=interaction.channel_id
            print(self.ch)
    async def on_message(self, message:discord.Message):
        filename = "./"+str(message.guild.id)+".wav"
        if message.channel.id==self.ch:
            voicevox.audio_query(text=message.content,speaker=1)
            with open(file=filename,mode="wb") as f:
                f.write(voicevox.synthesis(1))
            message.guild.voice_client.play(discord.FFmpegPCMAudio(source=filename))

client=myClient(intents=intents)
#commandtree
tree = app_commands.CommandTree(client=client)

#ログ設定
log_handler=logging.FileHandler(filename= './discord.log',mode='w', encoding='utf-8')

@tree.command()
async def summon(interaction:discord.Interaction):
    '''summon
        botをボイスチャンネルに呼びます。
    Parameters
    -----------
    vc: discord.VoiceChannel
        ボイスチャンネルを選択。
    '''
    vc=interaction.user.voice.channel
    if vc==None:
        await interaction.response.send_message(content="ボイスチャンネルに参加してください。",ephemeral=True)
    else:
        await vc.connect(timeout=60.0)
        await interaction.response.send_message(content=f"{vc.name}に参加しました。",ephemeral=True)
async def chara(interaction:discord.Interaction,charaid:int):
    '''chara
        キャラクターを選択します。
    Parameters
    -----------
    charaid:int
        キャラid
    '''
    global settings
    userid=interaction.user.id
    guildid=interaction.guild.id
    chara={
        'userid':userid,
        'charaid':charaid
    }
    settings[guildid][chara].append(chara)

client.run(token=getenv.token,log_handler=log_handler,log_level=logging.DEBUG)