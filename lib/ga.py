#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import requests
import string
import random

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

class ga():
  def __init__ (self):
    self.__addon = xbmcaddon.Addon('script.module.garepobg')
    self.__payload = {
        'v': '1',
        'tid': 'UA-61449088-3',
      }
    self.__url = 'http://www.google-analytics.com/collect?payload_data'
    if self.__addon.getSetting("firstrun") == "true":
      self.__addon.setSetting("firstrun", "false")
      self.__addon.setSetting("uid", self.__rnd_gen(size=32))
    

  def __get_platform(self):
    platforms = {
      "Linux": "X11; Linux",
      "Windows": "Windows NT %d.%d",
      "OSX": "Macintosh; Intel Mac OS X",
      "IOS": "iPad; CPU OS 6_1 like Mac OS X",
      "android": "Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K"
      }

    for platform, ua_platform_name in platforms.items():
      if xbmc.getCondVisibility("System.Platform.%s" % platform):
        if platform == "Windows":
          import sys
          version = sys.getwindowsversion()
          ua_platform_name %= (version[0], version[1])
        return ua_platform_name

  def __mkua(self):
     return "KODI/%s (%s)" % (xbmc.getInfoLabel("System.BuildVersion").split(" ")[0], self.__get_platform())

  def __rnd_gen(self, size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

  def update(self, data):
    if self.__addon.getSetting("ga") != 'true':
      return
    data.update(self.__payload)
    data['z'] = self.__rnd_gen()
    data['ua'] = self.__mkua()
    data['cid'] = self.__addon.getSetting("uid")
    return requests.post(self.__url, data=data)