import asyncio
import os

import discord
import pygame
from pygame.locals import *
import mazehenerator
import random


class Player:
    def __init__(self, id, name, start):
        global colori, colors
        self.id = id
        self.name = str(name)[:str(name).index("#")]
        self.lastmessage = -1
        self.pozice = start
        self.color = colors[colori]
        colori += 1

    def __str__(self):
        return f"<@{self.id}> {self.pozice}"


def vyhodnotpohyby():
    global players, pole
    for p in players:
        newpozice = p.pozice
        print(f"lastmassage je {p.lastmessage:}")
        if p.lastmessage == "w":    newpozice = (p.pozice[0], p.pozice[1] - 1)
        if p.lastmessage == "a":    newpozice = (p.pozice[0] - 1, p.pozice[1])
        if p.lastmessage == "s":    newpozice = (p.pozice[0], p.pozice[1] + 1)
        if p.lastmessage == "d":    newpozice = (p.pozice[0] + 1, p.pozice[1])
        print(newpozice)
        if pole[newpozice[1]][newpozice[0]] in ['1', "S", "C"]:
            p.pozice = newpozice
            p.lastmessage = "-1"


client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_message(message):
    global kanal, pole, playerid, players, N, M, starts, colori
    if message.author == client.user and message.content != "!tick": return
    print(f"{message.author} napsal: {message.content}")
    id = message.author.id
    if id in playerid and message.content != "!tick":
        players[playerid.index(id)].lastmessage = message.content

    if message.content.startswith("!startgame"):
        await message.channel.send("!netickej")
        players = []
        playerid = []
        colori = 0
        await message.delete()

        kanal = message.channel
        #size = random.randrange(3, )#//3
        size = 4
        starts = (random.randrange(1, size*3-2), random.randrange(1, size*3 - 2))
        cils = starts
        while cils == starts:
            cils = (random.randrange(1, size*3-2), random.randrange(1, size*3 - 2))

        pole = mazehenerator.genmaze(size, starts)
        pole[cils[1]][cils[0]] = 'C'
        print(pole)
        z = ""

        for i in pole:
            i = map(str, i)
            z += "".join(i)
            z += '\n'
        await message.channel.send("!start 1")
        await asyncio.sleep(5)
        await message.channel.send(f"!zadani {size} {size}")
        await message.channel.send(f"!zadani {z}")
        await message.channel.send("!zacnitickat")

    if message.content.startswith('!login'):
        id = message.author.id
        if id not in playerid:
            playerid.append(id)
            players.append(Player(id, message.author, starts))

    if message.content.startswith('!tick'):
        await message.delete()
        if all([p.lastmessage == -1 for p in players]):
            await message.channel.send("!netickej")
        vyhodnotpohyby()
        draw()
        await kanal.send(list(map(str, players)))
        await kanal.send("!move")
    draw()


def draw():
    global players, width, height, N, M, pole
    N = len(pole)
    M = len(pole)

    screen.fill('black')
    sirkapolicka = min(width - 250, height) / N

    plna = {}
    for i, player in enumerate(players):
        x, y = player.pozice
        print(player.color)
        pygame.draw.rect(screen, player.color, [x*sirkapolicka, y*sirkapolicka, sirkapolicka, sirkapolicka])
        r = font1.render(str(player.name), True, player.color)
        screen.blit(r, (width-250, i*sirkapolicka))
        if (x, y) in plna:
            plna[(x,y)] += 1
            r = font1.render(str(plna[(x, y)]), True, 'black')
            screen.blit(r, [x*sirkapolicka + sirkapolicka//2 - r.get_width()/2, y*sirkapolicka + sirkapolicka//2 - r.get_height()/2])
        else:
            plna[(x,y)] = 1

    for x in range(N):
        for y in range(M):
            if pole[y][x] == "S":
                pygame.draw.rect(screen, 'lime', (x*sirkapolicka, y * sirkapolicka, sirkapolicka, sirkapolicka))
            if pole[y][x] == "C":
                pygame.draw.rect(screen, 'red', (x * sirkapolicka, y * sirkapolicka, sirkapolicka, sirkapolicka))
            if pole[y][x] == '0':
                pygame.draw.rect(screen, 'white', (x * sirkapolicka, y * sirkapolicka, sirkapolicka, sirkapolicka))

    for y in range(1, M+1):
        pygame.draw.line(screen, 'gray', (0, y*sirkapolicka), (N*sirkapolicka, y*sirkapolicka), 4)
    for x in range(1, N+1):
        pygame.draw.line(screen, 'gray', (x*sirkapolicka, 0), (x*sirkapolicka, M*sirkapolicka), 4)

    pygame.display.update()

colors = ['forestgreen', 'darkblue', 'maroon3', 'orangered', 'yellow', 'burlywood', 'lime', 'aqua', 'fuchsia', 'green', 'blue', 'forestgreen']
colori = 0
pygame.init()
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
font1 = pygame.font.SysFont(None, 40)
starts = -1
N = -1
M = -1
playerid = []
players = []
kanal = -1
pole = []

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')

client.run(TOKEN)