from PIL import Image
from PIL import ImageFilter
from kivy import Config
Config.set('graphics', 'multisamples', '0')

import argparse
import json
import os
import numpy as np
import glob
import PIL

def parse_args():
    parser = argparse.ArgumentParser(description="Skripsi Bro")
    parser.add_argument(
        "--hasil",
        dest="hasil",
        type=str,
        default="/sdcard/identifikasi.json" #android
        # default="./datatraining_hasil/identifikasi.json" #pc
    )
    args = parser.parse_args()
    return args

def identifikasi():
    with open("/sdcard/identifikasi.json") as t: #android
    # with open("datatraining_hasil/identifikasi.json") as t: #pc
        data=json.load(t)
    return data

def info_ban():
    with open("Kategori_Ban.json") as t:
        data=json.load(t)
    return data

def rescale_gamb(img):
    basewidth = 27
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    return img

def rescale_templ(img):
    basewidth = 9
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    return img

def inpo(ban):
    global woke
    woke = ban
    return woke

def ncc(gambar, citra_templat):
    list_sum_t = []
    list_sum_g = []
    list_sum1 = []
    list_sum2 = []
    list_sum3 = []
    tutu = []
    sum_templat = 0
    sum_gambar = 0
    x_templat = len(citra_templat[0]) #panjang pixel gambar templat
    y_templat = len(citra_templat[:]) #lebar pixel gambar templat
    for i in np.arange(y_templat): #looping berdasarkan panjang nilai y_templat
        for j in np.arange(x_templat): #looping berdasarkan panjang nilai x_templat
            list_sum_t.append(citra_templat[i][j])
            list_sum_g.append(gambar[i][j])
    sum_templat = sum(list_sum_t)
    sum_gambar = sum(list_sum_g)
    mean_templat = sum_templat/(y_templat*x_templat) #nilai tengah templat
    mean_gambar = sum_gambar/(x_templat*x_templat) #nilai tengah gambar
    sum1 = 0
    sum2 = 0
    sum3 = 0
    sss = 0
    for a in np.arange(y_templat): #looping berdasarkan panjang nilai y_templat
        for b in np.arange(x_templat): #looping berdasarkan panjang nilai x_templat
            list_sum1.append((citra_templat[a][b] - mean_templat) * (gambar[a][b] - mean_gambar))
            list_sum2.append((citra_templat[a][b] - mean_templat) ** 2)
            list_sum3.append((gambar[a][b] - mean_gambar) ** 2)
    sum1 = sum(list_sum1)
    sum2 = sum(list_sum2)
    sum3 = sum(list_sum3)
    ncc = sum1/((sum2*sum3) ** 0.5) #sum1 dibagi akar dari sum2 yg dikalikan dgn sum3
    return ncc

def tm(citra_gambar, citra_templat):
    x_gambar = len(citra_gambar[0]) #panjang pixel gambar uji
    y_gambar = len(citra_gambar[:]) #lebar pixel gambar uji
    x_templat = len(citra_templat[0]) #panjang pixel gambar templat
    y_templat = len(citra_templat[:]) #lebar pixel gambar templat
    akurasi = 0
    for i in range(y_gambar-y_templat): #proses komputasi berjalan sebanyak selisih
        for j in range(x_gambar-x_templat): #proses komputasi berjalan sebanyak selisih
            gambar = [m[j:j+x_templat] for m in citra_gambar[i:i+y_templat]] # menentukan titik citra templat di dalam citra gambar
            max_val = ncc(gambar,citra_templat)
            if (max_val > akurasi): #dicari nilai kecocokan yg terbesar dari proses ncc
                akurasi = max_val #nilai akurasi tertinggi
                x = j #posisi x
                y = i #posisi y
    return x,y,akurasi

def pil2cv(image): #convert ke float
    new_image = np.array(image, dtype=np.float64) #buat array
    new_image /= 255.0 #desimal
    return new_image

def perbandingan(citra_gambar):
    global informasi
    global kiri
    global kanan
    global not_found
    global st_x
    global st_y
    global en_x
    global en_y
    global v
    global tt
    global hasil
    global outvut
    global nilai
    global kr3
    global kr4
    global kr5
    global kr6
    global kr7
    global kr8
    global kr9
    global kr10
    global kn3
    global kn4
    global kn5
    global kn6
    global kn7
    global kn8
    global kn9
    global kn10
    global status

    outvut = []
    args = parse_args()
    info=info_ban()
    templat=[]
    list_templat=[]
    files= sorted( glob.glob('dataset_tbesar/*.jpg') )
    for file in files:
        tmpl = Image.open(file).convert('L')
        tkecil = rescale_templ(tmpl)
        tkecilv2 = pil2cv(tkecil)
        templat.append(tkecilv2)
        list_templat.append(tkecilv2)
    i=0
    j=0
    sebelumnya = 0
    status = 0
    show = False
    for citra_templat in list_templat:
        x, y, akurasi = tm(citra_gambar, citra_templat)
        t = i+1
        outvut.append([t,akurasi])
        print ("templat ke: ",t," akurasi: ",akurasi)
        if (akurasi>sebelumnya):
            sebelumnya = akurasi
            if (akurasi>0.9):
                j=i
                show = True
                revskala = 16.666666667
                st_x = x*revskala
                st_y = y*revskala
                y1 = len(citra_templat[1])*revskala
                x1 = len(citra_templat[0])*revskala
                en_x = st_x+x1
                en_y = st_y+y1
                hasil = akurasi
                status = 1
            else:
                status = 0
                j=i
                show = False
                revskala = 16.666666667
                st_x = x*revskala
                st_y = y*revskala
                y1 = len(citra_templat[1])*revskala
                x1 = len(citra_templat[0])*revskala
                en_x = st_x+x1
                en_y = st_y+y1
                hasil = akurasi
        i = i+1
    if show == True:
        tt = j+1
        kategori_ban = info["ban"][j]["kategori"]
        nomor_seri_ban = info["ban"][j]["noseri"]
        ukuran_ban = info["ban"][j]["ukuran"]
        drygrip = info["ban"][j]["drygrip"]
        wetgrip = info["ban"][j]["wetgrip"]
        braking = info["ban"][j]["braking"]
        handling = info["ban"][j]["handling"]
        treadwear = info["ban"][j]["treadwear"]
        with open(args.hasil, "w") as file:
            json.dump({"titik kecocokan x": st_x, "titik kecocokan y": st_y, "akurasi": hasil, "kategori ban": kategori_ban, "No. templat :": tt}, file)
        kr3 = "No.Seri"
        kr4 = "Kategori Ban"
        kr5 = "Ukuran Ban"
        kr6 = "DRY GRIP"
        kr7 = "WET GRIP"
        kr8 = "BRAKING"
        kr9 = "HANDLING"
        kr10 = "TREADWEAR"
        kn3 = nomor_seri_ban
        kn4 = kategori_ban
        kn5 = ukuran_ban
        kn6 = drygrip
        kn7 = wetgrip
        kn8 = braking
        kn9 = handling
        kn10 = treadwear
    if show == False:
        tt = j+1
        kategori_ban = info["ban"][j]["kategori"]
        nomor_seri_ban = info["ban"][j]["noseri"]
        ukuran_ban = info["ban"][j]["ukuran"]
        drygrip = info["ban"][j]["drygrip"]
        wetgrip = info["ban"][j]["wetgrip"]
        braking = info["ban"][j]["braking"]
        handling = info["ban"][j]["handling"]
        treadwear = info["ban"][j]["treadwear"]
        with open(args.hasil, "w") as file:
            json.dump({"titik kecocokan x": st_x, "titik kecocokan y": st_y, "akurasi": hasil, "kategori ban": kategori_ban, "No. templat :": tt}, file)
        kr3 = ""
        kr4 = ""
        kr5 = "Tidak"
        kr6 = ""
        kr7 = ""
        kr8 = ""
        kr9 = ""
        kr10 = ""
        kn3 = ""
        kn4 = ""
        kn5 = "Ketemu"
        kn6 = ""
        kn7 = ""
        kn8 = ""
        kn9 = ""
        kn10 = ""
    v = i
    return citra_gambar

def waktu(sec):
    global lama_banget
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    lama_banget = "{1} menit {2} detik".format(int(hours),int(mins),int(sec))
