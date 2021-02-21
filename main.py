from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle,Color
from kivy.app import App

from PIL import Image, ImageFont, ImageDraw
from progam import *
from kivy.config import Config
from kivy.clock import mainthread
Config.set('graphics', 'width', '332')
Config.set('graphics', 'height', '720')
# Config.set('graphics', 'width', '720')
# Config.set('graphics', 'height', '1560')
# Config.set('graphics', 'resizable', False)
from kivy import Config
Config.set('graphics', 'multisamples', '0')
from itertools import chain
import kivy.app
import os
import glob
import PIL
import progam
import numpy as np
import time
import itertools

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    def selected(self,filename):
        self.ids["ban"].opacity = 1
        a = str (filename)[1:-1]
        b = a.replace("'", "")
        gambar = b.replace("/datatest_gbesar/datatest_gbesar", "/datatest_gbesar")
        try:
            self.ids["ban"].source = gambar
        except:
            pass

class Kamera(FloatLayout):
    cancel = ObjectProperty(None)
    def capture(self):
        self.ids["pembatas"].opacity = 0
        camera = self.ids['camera']
        # foto = camera.export_to_png("foto_ban.png") #pc
        foto = camera.export_to_png("/sdcard/foto_ban.png") #android
        img = Image.open("/sdcard/foto_ban.png") #android
        # img = Image.open("foto_ban.png") #pc
        # crop = img.crop((75, 266, 525, 866)) #android
        crop = img.crop((75, 279, 525, 879))
        draw = ImageDraw.Draw(crop)
        kotak1 = draw.rectangle(((0, 00), (100, 600)), fill="white")
        kotak2 = draw.rectangle(((350, 00), (450, 600)), fill="white")
        rgb = crop.convert('RGB').save("/sdcard/foto_ban.jpg","JPEG") #android
        # rgb = crop.convert('RGB').save("foto_ban.jpg","JPEG") #pc

class FirstApp(kivy.app.App):

    def dismiss_popup(self):
        self._popup.dismiss()

    def foto(self):
        self.dismiss_popup()
        global siap
        global namafile
        global b
        global owi
        global gbesar_print
        self.root.ids["btn"].disabled = False
        self.root.ids["image"].opacity = 1
        self.root.ids["templ"].opacity = 0
        owi = Image.open("/sdcard/foto_ban.jpg").convert('L') #android
        # owi = Image.open("foto_ban.jpg").convert('L') #pc
        siap = progam.rescale_gamb(owi)
        namafile = "hasil kamera"
        # gbesar_print = Image.open("foto_ban.jpg") #pc
        gbesar_print = Image.open("/sdcard/foto_ban.jpg") #android
        self.root.ids["image"].source = "/sdcard/foto_ban.jpg" #android
        # self.root.ids["image"].source = "foto_ban.jpg" #pc
        self.root.ids["btn"].disabled = False
        self.root.ids["btn"].canvas.before.add(Color(1,0,0,1))
        self.root.ids["btn"].canvas.before.add(Rectangle(size=(self.root.ids["btn"].size),pos=(self.root.ids["btn"].pos)))
        self.root.ids["status"].text = "KLIK 'SCAN'"
        self.root.ids["status"].color = 0.164,0.831,0.462, 1
        self.root.ids["kr1"].text = ""
        self.root.ids["kr3"].text = ""
        self.root.ids["kr4"].text = ""
        self.root.ids["kr5"].text = "Nama File ="
        self.root.ids["kr5"].halign = "right"
        self.root.ids["kr6"].text = ""
        self.root.ids["kr7"].text = ""
        self.root.ids["kr8"].text = ""
        self.root.ids["kr9"].text = ""
        self.root.ids["kr10"].text = ""
        self.root.ids["kr2"].text = ""
        self.root.ids["kr11"].text = ""
        self.root.ids["kr12"].text = ""
        self.root.ids["kn1"].text = ""
        self.root.ids["kn3"].text = ""
        self.root.ids["kn4"].text = ""
        self.root.ids["kn5"].text = namafile
        self.root.ids["kn5"].halign = "left"
        self.root.ids["kn6"].text = ""
        self.root.ids["kn7"].text = ""
        self.root.ids["kn8"].text = ""
        self.root.ids["kn9"].text = ""
        self.root.ids["kn10"].text = ""
        self.root.ids["kn2"].text = ""
        self.root.ids["kn11"].text = ""
        self.root.ids["kn12"].text = ""
        self.root.ids["image"].opacity = 1
        self.root.ids["templ"].opacity = 1
        self.root.ids["templ"].source = "ikon/empty.png"

    def show_kamera(self):
        content = Kamera(cancel=self.dismiss_popup)
        self._popup = Popup(title="Kamera", title_font='DejaVuSans',content=content,
                            size_hint=(0.9, 0.9),background='bg.png')
        self._popup.open()

    def show_load(self):
        content = LoadDialog(cancel=self.dismiss_popup)
        self._popup = Popup(title="Import File", title_font='DejaVuSans',content=content,
                            size_hint=(0.9, 0.9),background='bg.png')
        self._popup.open()

    def load(self,input):
        self.root.ids["image"].source = ""
        self.dismiss_popup()
        global siap
        global namafile
        global gbesar_print
        global gbesar
        a = str (input)[1:-1]
        b = a.replace("'", "")
        # gkecil = b.replace("/datatest_gkecil/datatest_gkecil", "/datatest_gkecil")
        gbesar = b.replace("/datatest_gbesar/datatest_gbesar", "/datatest_gbesar")
        gamb = Image.open(gbesar).convert('L')
        siap = progam.rescale_gamb(gamb)
        gbesar_print = Image.open(gbesar)
        namafile = os.path.basename(gbesar)
        self.root.ids["image"].source = gbesar
        self.root.ids["btn"].disabled = False
        self.root.ids["btn"].canvas.before.add(Color(1,0,0,1))
        self.root.ids["btn"].canvas.before.add(Rectangle(size=(self.root.ids["btn"].size),pos=(self.root.ids["btn"].pos)))
        self.root.ids["status"].text = "KLIK 'SCAN'"
        self.root.ids["status"].color = 0.164,0.831,0.462, 1
        self.root.ids["kr1"].text = ""
        self.root.ids["kr3"].text = ""
        self.root.ids["kr4"].text = ""
        self.root.ids["kr5"].text = "Nama File ="
        self.root.ids["kr5"].halign = "right"
        self.root.ids["kr6"].text = ""
        self.root.ids["kr7"].text = ""
        self.root.ids["kr8"].text = ""
        self.root.ids["kr9"].text = ""
        self.root.ids["kr10"].text = ""
        self.root.ids["kr2"].text = ""
        self.root.ids["kr11"].text = ""
        self.root.ids["kr12"].text = ""
        self.root.ids["kn1"].text = ""
        self.root.ids["kn3"].text = ""
        self.root.ids["kn4"].text = ""
        self.root.ids["kn5"].text = namafile
        self.root.ids["kn5"].halign = "left"
        self.root.ids["kn6"].text = ""
        self.root.ids["kn7"].text = ""
        self.root.ids["kn8"].text = ""
        self.root.ids["kn9"].text = ""
        self.root.ids["kn10"].text = ""
        self.root.ids["kn2"].text = ""
        self.root.ids["kn11"].text = ""
        self.root.ids["kn12"].text = ""
        self.root.ids["image"].opacity = 1
        self.root.ids["templ"].opacity = 1
        self.root.ids["templ"].source = "ikon/empty.png"

    @mainthread
    def classify_image(self):
        start_time = time.time()
        res = progam.pil2cv(siap)
        matching = progam.perbandingan(res)
        end_time = time.time()
        durasi = end_time - start_time
        progam.waktu(durasi)
        if (progam.status==1):
            posisi=progam.identifikasi()
            titik_x = posisi["titik kecocokan x"]
            titik_y = posisi["titik kecocokan y"]
            draw = ImageDraw.Draw(gbesar_print)
            poss = (int(round(titik_x)), int(round(titik_y)), int(round(titik_x))+150, int(round(titik_y))+150)
            ketebalan = 5
            for i in range(ketebalan):
                draw.rectangle(poss, outline="red")
                poss = (poss[0]+1,poss[1]+1, poss[2]+1,poss[3]+1)
            gbesar_print.save("/sdcard/hasil.png") #android
            # gbesar_print.save("hasil.png") #pc
            self.root.ids["image"].source = "/sdcard/hasil.png" #android
            # self.root.ids["image"].source = "hasil.png" #pc
            self.root.ids["image"].reload()
            self.root.ids["kr1"].text = "File"
            self.root.ids["kr3"].text = progam.kr3
            self.root.ids["kr4"].text = progam.kr4
            self.root.ids["kr5"].text = progam.kr5
            self.root.ids["kr6"].text = progam.kr6
            self.root.ids["kr5"].halign = "left"
            self.root.ids["kr7"].text = progam.kr7
            self.root.ids["kr8"].text = progam.kr8
            self.root.ids["kr9"].text = progam.kr9
            self.root.ids["kr10"].text = progam.kr10
            self.root.ids["kr2"].text = "No. Templat"
            self.root.ids["kr11"].text = "Nilai Akurasi"
            self.root.ids["kr12"].text = "Durasi Komputasi"
            self.root.ids["kn1"].text = namafile
            self.root.ids["kn3"].text = progam.kn3
            self.root.ids["kn4"].text = progam.kn4
            self.root.ids["kn5"].text = progam.kn5
            self.root.ids["kn6"].text = progam.kn6
            self.root.ids["kn5"].halign = "left"
            self.root.ids["kn7"].text = progam.kn7
            self.root.ids["kn8"].text = progam.kn8
            self.root.ids["kn9"].text = progam.kn9
            self.root.ids["kn10"].text = progam.kn10
            self.root.ids["kn2"].text = str("{:03d}".format(progam.tt))
            self.root.ids["kn11"].text = str(progam.hasil)[:7]
            self.root.ids["kn12"].text = progam.lama_banget
            self.root.ids["templ"].opacity = 1
            self.root.ids["templ"].source = os.getcwd() + "/dataset_tbesar/tm" + str("{:03d}".format(progam.tt)) + ".jpg"
            self.root.ids["status"].text = "HASIL IDENTIFIKASI"
            self.root.ids["xy"].text = "x = " + str(int(round(titik_x))) + " y = " + str(int(round(titik_y)))
            self.root.ids["status"].color = 0.988, 0.701, 0.29, 1
        else:
            self.root.ids["image"].source = gbesar
            self.root.ids["image"].reload()
            self.root.ids["kr1"].text = "File"
            self.root.ids["kr3"].text = "Hasil"
            self.root.ids["kr4"].text = "Durasi Komputasi"
            self.root.ids["kr5"].text = ""
            self.root.ids["kr6"].text = ""
            self.root.ids["kr5"].halign = "left"
            self.root.ids["kr7"].text = ""
            self.root.ids["kr8"].text = ""
            self.root.ids["kr9"].text = ""
            self.root.ids["kr10"].text = ""
            self.root.ids["kr2"].text = ""
            self.root.ids["kr11"].text = ""
            self.root.ids["kr12"].text = ""
            self.root.ids["kn1"].text = namafile
            self.root.ids["kn3"].text = "Tidak Ditemukan"
            self.root.ids["kn4"].text = progam.lama_banget
            self.root.ids["kn5"].text = ""
            self.root.ids["kn6"].text = ""
            self.root.ids["kn5"].halign = "left"
            self.root.ids["kn7"].text = ""
            self.root.ids["kn8"].text = ""
            self.root.ids["kn9"].text = ""
            self.root.ids["kn10"].text = ""
            self.root.ids["kn2"].text = ""
            self.root.ids["kn11"].text = ""
            self.root.ids["kn12"].text = ""
            self.root.ids["templ"].opacity = 1
            self.root.ids["templ"].source = "ikon/empty.png"
            self.root.ids["status"].text = ""
            self.root.ids["xy"].text = "x = ... y = ..."
            self.root.ids["status"].color = 0.988, 0.701, 0.29, 1


firstApp = FirstApp(title="Identifikator Kategori Ban")
firstApp.run()
