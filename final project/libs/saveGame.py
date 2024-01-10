from libs.vector import Vec3
from OpenGL.GLUT import *
from tkinter import *

def saveAll(game):
    w = _savePlayer(game.player)
    x = _saveCam(game.player.camera)
    y = _saveGun(game.player.gun)
    z = _saveEnemies(game.enemies)
    return [w, x, y, z]

def loadAll(game, data):
    _loadPlayer(game.player, data[0])
    _loadCam(game.player.camera, data[1])
    _loadGun(game.player.gun, data[2])
    _loadEnemies(game.enemies, data[3])


def _savePlayer(player):
    dic = dict(player.__dict__)
    for i in ["sounds", "camera", "terrain", "gun", "motionTimer"]:
        del dic[i]
    return dic


def _loadPlayer(player, data):
    for i in data.keys():
        player.__dict__[i] = data[i]


def _saveCam(camera):
    dic = dict(camera.__dict__)
    for i in ["cam_pos", "cam_fr", "cam_up", "cam_ri"]:
        dic[i] = dic[i].tuple()
    return dic


def _loadCam(camera, data):
    camera.__dict__ = dict(data)
    for i in ["cam_pos", "cam_fr", "cam_up", "cam_ri"]:
        camera.__dict__[i] = Vec3(*data[i])


def _saveGun(gun):
    dic = dict(gun.__dict__)
    for i in ["animation", "sounds", "muzzle"]:
        del dic[i]
    if dic["shootingDir"]:
        dic["shootingDir"] = dic["shootingDir"].tuple()
    return dic


def _loadGun(gun, data):
    for i in data.keys():
        gun.__dict__[i] = data[i]
    if data["shootingDir"]:
        gun.shootingDir = Vec3(*data["shootingDir"])


def _saveEnemies(lstOfEnemies):
    outDicLst = []
    for i in lstOfEnemies:
        tmp = dict(i.__dict__)
        for j in tmp.keys():
            if j in ["initialPos", "prevPos", "pos", "front", "forces"]:
                tmp[j] = tmp[j].tuple()
        for j in ["player", "texture", "dyingSounds", "animation"]:
            del (tmp[j])
        outDicLst.append(tmp)
    return outDicLst


def _loadEnemies(lstOfEnemies, data):
    for i in range(len(lstOfEnemies)):
        for j in data[i].keys():
            lstOfEnemies[i].__dict__[j] = data[i][j]
            if j in ["initialPos", "prevPos", "pos", "front", "forces"]:
                lstOfEnemies[i].__dict__[j] = Vec3(*data[i][j])