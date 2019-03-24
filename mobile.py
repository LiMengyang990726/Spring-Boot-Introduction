################################################################################
#
#
# MOBILE DATA
#
#
################################################################################
import pandas as pd
import numpy as np
import nltk
import pytesseract
from PIL import Image
from translate import Translator
import math
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
sb.set()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
import pickle

################################################################################
#
# Get Input
#
################################################################################
data = pd.read_csv("mobile_data_info_train_competition.csv")
data.isna().sum()
data.head()
data.shape

def save_new_dataset(dataset, name):
    dataset.to_csv(name)

################################################################################
#
# Stage 0: Image Text Extraction
#
################################################################################
pytesseract.pytesseract.tesseract_cmd = r"/usr/local/Cellar/tesseract/4.0.0_1/bin/tesseract"
DATADIR = "/Users/eric/Workspaces/NDSC/mobile_image"        #Location of your images
config = ('-l eng --oem 1 --psm 3')

def get_text_from_images(dataset):
    translator= Translator(from_lang="malay", to_lang="english")
    total = len(dataset.index)
    for index, row in dataset.iterrows():
        #Get text from image
        text = pytesseract.image_to_string(Image.open("data/" + row["image_path"]), config=config)
        text = text.replace("\n", " ")
        dataset.loc[index,"title"] = str(dataset.loc[index,"title"]) + " " + text
        #Percentage indicator
        percent = index/total
        print(percent)

get_text_from_images(data)
save_new_dataset(data, "mobile_data_stage_0.csv")

################################################################################
#
# Stage 1 (Basic Filling): Fill in according to a single word in title
#
################################################################################
# fill in and correct the values that can be found in the title
# the dictionary here only contains single word (Stage 1: single word filling)
brandDic = {"google": 0, "htc": 1, "apple": 2, "wiko": 3, "polytron": 4, "huawei": 21, "gionee": 5, "leagoo": 6, "brandcode": 7, "luna": 8, "sharp": 10, "acer": 9, "blackview": 11, "prince": 12, "lg": 13, "spc": 14, "coolpad": 15, "smartfren": 16, "infinix": 17, "blaupunkt": 18, "lava": 19, "aldo": 20, "icherry": 32, "advan": 22, "leeco": 23, "nexcom": 24, "zyrex": 25, "axioo": 26, "elephone": 27, "himax": 28, "hp": 29, "nokia": 30, "nuu mobile": 31, "xiaomi": 33, "pixcom": 34, "mito": 35, "huang mi": 36, "maxtron": 37, "sony": 38, "indosat": 39, "philips": 40, "lenovo": 41, "alcatel": 42, "samsung": 43, "zyo": 44, "doogee": 45, "vivo": 46, "evercoss": 47, "strawberry": 48, "ifone": 49, "fujitsu": 50, "blackberry": 51, "asus": 52, "oneplus": 53, "honor": 54, "oppo": 55}
featureDic = {"touchscreen": 0, "dustproof": 6, "waterproof": 1, "wifi": 2,"gps": 5}
networkDic = {"4g": 0, "2g": 1, "3g": 2, "3.5g": 3}
colorDic = {"blue": 4, "gold": 0, "brown": 14, "navy": 15, "yellow": 1, "neutral": 16, "silver": 19, "pink": 2, "gray": 20, "army": 21,  "purple": 6, "rose": 7, "multicolor": 24, "black": 10, "apricot": 23, "orange": 11, "green": 25, "white": 12, "red": 13}
memDic = {"4gb": 5, "2gb": 6, "1.5gb": 0, "16gb": 9, "512mb": 1, "8gb": 3,"3gb": 7, "10gb": 2, "1gb": 8, "6gb": 4}
storageDic = {"256gb": 16, "1.5gb": 0, "128gb": 1, "512mb": 2, "64gb": 3, "512gb": 4, "8gb": 5, "4mb": 10, "6gb": 7, "4gb": 9, "2gb": 6, "128mb": 11, "32gb": 12, "256mb": 13, "10gb": 14, "3gb": 15, "1gb": 8, "16gb": 17}
for index, row in data.iterrows():
    title = row['title']
    words = title.split()
    for word in words:
        # Brand, fill in 3 more
        if word in brandDic.keys():
            data.loc[index,'Brand'] = brandDic[word]
            print(word+" "+str(brandDic[word]))
        elif data.loc[index,'Brand'] == None:
            data.loc[index,'Brand'] == None
        #
        # Feature
        if word in featureDic.keys():
            data.loc[index,'Features'] = featureDic[word]
            print(word+" "+str(featureDic[word]))
        elif data.loc[index,'Features'] == None:
            data.loc[index,'Features'] == None
        #
        # Network, fill in 252
        if word in networkDic.keys():
            data.loc[index,'Network Connections'] = networkDic[word]
            print(word+" "+str(networkDic[word]))
        elif data.loc[index,'Network Connections'] == None:
            data.loc[index,'Network Connections'] == None
        #
        # Color, fill in 227
        if word in colorDic.keys():
            data.loc[index,'Color Family'] = colorDic[word]
            print(word+" "+str(colorDic[word]))
        elif data.loc[index,'Color Family'] == None:
            data.loc[index,'Color Family'] == None
        #
        # Mem
        if (word in memDic.keys()) and (word not in storageDic.keys()):
            data.loc[index,'Memory RAM'] = memDic[word]
            print(word+" "+str(memDic[word]))
        elif data.loc[index,'Memory RAM'] == None:
            data.loc[index,'Memory RAM'] == None
        #
        # Storage
        if (word in storageDic.keys()) and (word not in memDic.keys()):
            data.loc[index,'Storage Capacity'] = storageDic[word]
            print(word+" "+str(storageDic[word]))
        elif data.loc[index,'Storage Capacity'] == None:
            data.loc[index,'Storage Capacity'] == None

save_new_dataset(data, "mobile_data_stage_1.csv")


################################################################################
#
# Stage 2 (Relationship Filling): Fill according to known fact
#
################################################################################
# fill in the missing values (Operating system) according to the relationship
for index, row in data.iterrows():
    if any(mobileOS in row["title"] for mobileOS in ["asha"]):
        data.loc[index,"Operating System"] = 0
    if any(mobileOS in row["title"] for mobileOS in ["apple", "ios", "iphone", "ipad", "ipod"]):
        data.loc[index,"Operating System"] = 1
    if any(mobileOS in row["title"] for mobileOS in ["nokia 3", "nokia 5", "nokia 6", "nokia e", "nokia n", "samsung sgh", "lg kt"]):
        data.loc[index,"Operating System"] = 2
    if any(mobileOS in row["title"] for mobileOS in ["lumia", "microsoft"]):
        data.loc[index,"Operating System"] = 3
    if any(mobileOS in row["title"] for mobileOS in ["samsung gear", "samsung z", "samsung nx"]):
        data.loc[index,"Operating System"] = 4
    if any(mobileOS in row["title"] for mobileOS in ["blackberry"]):
        data.loc[index,"Operating System"] = 5
    if any(mobileOS in row["title"] for mobileOS in ["android", "google", "huawei", "oneplus", "xiaomi", "honor", "galaxy", "vivo"]):
        data.loc[index,"Operating System"] = 6

save_new_dataset(data, "mobile_data_stage_2.csv")


################################################################################
#
# Stage 3 (Similairity Filling / Multiple words Filling): Fill according to the jaccard similarity between multiple words
#
################################################################################
Model_label = {
        "samsung gear sport": 1142,
        "sony xperia xa ultra": 0,
        "samsung ua55mu6300": 1998,
        "apple ipad mini wi fi cellular": 1224,
        "coocaa 55s3a12g": 1144,
        "hp elite x2 1012": 2,
        "lenovo ideapad s2": 3,
        "asus x540ya": 4,
        "drypers drypantz mega pack l 48": 5,
        "apple watch series 2": 27,
        "merries pants good skin l 20": 31,
        "apple watch series 4": 1148,
        "hp omen 15 ce503tx": 1149,
        "apple macbook pro mr9r2": 1150,
        "sony 48w700c": 7,
        "lg 65sk8500": 1514,
        "hp 14 bs745tu": 1151,
        "huawei honor 10": 463,
        "xiaomi redmi pro": 1152,
        "samsung ua49mu6300": 9,
        "asus e402ma": 2079,
        "sony kd 49x8000e": 10,
        "sony kd 49x8000c": 11,
        "dell latitude 3390": 1900,
        "hp 14 bw504au": 13,
        "lenovo vibe k5": 747,
        "oppo r11s": 15,
        "asus zenfone 4 pro": 359,
        "nikon coolpix l840": 1154,
        "aqua le32s6500": 17,
        "hp 14 bs741tu": 1155,
        "philips 39pha4251s": 1156,
        "wiko robby 2017": 18,
        "lenovo legion y720": 1157,
        "asus zenfone c zc451cg": 1790,
        "oppo a57": 19,
        "apple watch sport 38mm 1st gen": 20,
        "ichiko s6558": 1576,
        "asus x454la": 1590,
        "lenovo k5 note": 21,
        "samsung 65q8cn": 1158,
        "asus zenbook ux331un": 22,
        "asus pro p2440ua": 1159,
        "huawei p10 plus": 1517,
        "apple ipad 4 wi fi": 1160,
        "lenovo thinkpad w550s": 1161,
        "huawei y3": 1162,
        "samsung 43nu7100": 2160,
        "sony kdl 49w660e": 23,
        "huawei y7": 1163,
        "huawei y6": 1164,
        "huawei y5": 1165,
        "sharp pi": 364,
        "lenovo thinkpad t460": 25,
        "samsung ua24h4150": 1166,
        "changhong 50d3000i": 1167,
        "panasonic th 49ex400g": 1168,
        "apple watch series 1": 1145,
        "sharp m1": 1169,
        "asus ux461un": 26,
        "goo.n smile baby pants l30": 1146,
        "goo.n smile baby pants m34": 28,
        "canon powershot sx620 hs": 29,
        "asus zenpad c 7": 30,
        "apple watch series 3": 1147,
        "sharp lc 40le380x": 32,
        "huawei honor play": 1173,
        "pampers premium care pants xl 54": 2082,
        "xiaomi mi mix 2s 6": 1883,
        "brandcode b3310": 33,
        "hp pavilion 14 d040tu": 1702,
        "acer aspire es1 421": 1174,
        "acer aspire es1 420": 1175,
        "nikon d500": 1176,
        "xiaomi redmi s2": 34,
        "huawei mediapad t3 7.0": 35,
        "acer predator g9 593": 1177,
        "aqua le32aqt9000t": 36,
        "samsung gear s3 classic lte": 1178,
        "aqua le40aqt6900": 2016,
        "changhong 22c2600": 38,
        "lg 86sj957t": 1179,
        "lenovo a6000": 39,
        "asus zenfone max pro zb602kl 6": 1522,
        "ichiko s1928": 40,
        "lenovo ideapad 300s": 1181,
        "nikon coolpix a100": 41,
        "polytron pld32d1550": 42,
        "fitti gold pants xl42": 43,
        "samsung ua32j4303": 1182,
        "xiaomi mi 8 se": 1531,
        "hp 14 bw005au": 44,
        "acer aspire es1 431": 1330,
        "vivo v9 youth": 1183,
        "baby happy pants l 20": 1184,
        "asus s410un eb067t": 1832,
        "dell latitude 5490": 1185,
        "hp 14 bw502au": 45,
        "evercoss s55 elevate y2 power": 2189,
        "xiaomi redmi 3x 2": 1187,
        "sony cybershot dsc h400": 1188,
        "olympus pen e pl8": 2084,
        "apple ipad 2": 46,
        "apple ipad 3": 47,
        "nepia genki pants xl 26": 48,
        "lenovo thinkpad yoga 370": 2154,
        "asus zenfone go": 49,
        "huawei mediapad m3 lite 8": 1189,
        "mamypoko extra dry pants xl 26": 1190,
        "asus rog strix gl504gm hero ii": 1792,
        "canon eos 6d mark ii": 1191,
        "samsung 49k5100": 1192,
        "sensi dry s12": 50,
        "ichiko st6596": 51,
        "dell vostro 5471": 310,
        "nikon coolpix l340": 52,
        "panasonic th 43d305g": 53,
        "lg 43uj652t": 1331,
        "xiaomi mi 8 6": 2180,
        "nepia genki pants xxl 18": 54,
        "canon eos 2000d": 1196,
        "akari le 5099t2sb": 2205,
        "asus zenpad 8 z380m": 55,
        "huawei honor 8 pro 6": 1198,
        "samsung gear s3 frontier lte": 56,
        "changhong 40d2100t": 57,
        "coocaa 55e2a12g": 1199,
        "ichiko s1718": 1774,
        "samsung galaxy a8 2016 3": 1787,
        "apple ipad 2018": 58,
        "mito 168": 1705,
        "sharp lc 60le275x": 1332,
        "drypers drypantz mega pack xxl 36": 59,
        "asus zenfone 4 selfie zb553kl": 1200,
        "huawei y3ii": 60,
        "apple ipad 2017": 61,
        "xiaomi redmi 4 prime": 1201,
        "infinix note 4": 1202,
        "asus pu451ld": 1203,
        "vivo y51": 366,
        "toshiba 55l3750vj": 62,
        "hp spectre 13 v022tu": 63,
        "lenovo a6010": 1204,
        "lg 65uj652t": 64,
        "toshiba 40l3750": 406,
        "aqua le32aqt9100t": 1707,
        "sony dsc qx10": 407,
        "canon ixus 185": 65,
        "xiaomi redmi 3s": 1207,
        "apple iphone 6s": 1208,
        "goo.n slim pants xxl36": 1170,
        "pokana pants surprise design s 22": 66,
        "sharp lc 24sa4000i": 67,
        "gigabyte p57x v7": 68,
        "mamypoko extra soft pants m 34": 1211,
        "mito 128": 69,
        "motorola moto z2 play": 1212,
        "sony a7 mark ii": 1213,
        "mito 122": 70,
        "polytron pld32t1500": 1214,
        "sharp lc 40sa5500i": 71,
        "msi gl62m 7rex": 1215,
        "sweety silver pants l 28": 1216,
        "polysonic 2400": 755,
        "coocaa 32e2000t": 1217,
        "asus zenfone pegasus 3": 73,
        "mamypoko x tra dry pants xl 38": 74,
        "sony cybershot dsc rx10 iv": 75,
        "asus zenfone 2 ze550ml": 1218,
        "sony xperia xa2 plus": 76,
        "apple ipad mini 4 wifi": 1219,
        "gigabyte sabre 15 p45w": 78,
        "lenovo a7000 plus": 79,
        "sharp lc 50ua6800x": 80,
        "huawei nova 2 4": 189,
        "lg 65uj632t": 81,
        "mamypoko extra dry tape m 72": 1221,
        "ichiko s3968": 1222,
        "huawei mate 9 pro": 82,
        "mamypoko extra dry tape xxl 28": 83,
        "gigabyte sabre 15 p45g": 84,
        "samsung galaxy tab 4 7.0 1.5": 85,
        "lenovo yoga 700": 375,
        "drypers drypantz convenient pack s 24": 87,
        "huawei mediapad t1 7.0 1": 1226,
        "mamypoko x tra dry pants m 20": 88,
        "wiko view max": 1227,
        "sanken sle 321hdj": 1228,
        "dell latitude e7450": 1229,
        "strawberry st11": 1303,
        "sweety silver pants xxl 36": 1230,
        "samsung galaxy a5 2017": 1231,
        "samsung galaxy a5 2016": 1232,
        "changhong 40d3000i": 566,
        "nokia 8": 90,
        "hp 14 bs705tu": 91,
        "asus a442uf": 1234,
        "polytron 40v853": 92,
        "samsung galaxy note 9 6": 1622,
        "huawei y5ii": 93,
        "nokia 1": 94,
        "nokia 3": 95,
        "nokia 2": 96,
        "nokia 5": 97,
        "ichiko s2218": 1236,
        "panasonic lumix dc gf10": 1237,
        "panasonic th 32c304g": 1238,
        "xiaomi mi 4s 3": 1239,
        "apple macbook air mmgf2": 1240,
        "samsung 40n5000": 1241,
        "asus a442ur": 1242,
        "lenovo z5": 614,
        "sony klv 32r302c": 1313,
        "pokana pants surprise design m 20": 99,
        "lenovo flex 11": 101,
        "acer aspire e1 471": 102,
        "honor 5c": 1916,
        "toshiba 43l5650": 104,
        "mamamia pants m20": 105,
        "coocaa 43e2a12g": 1246,
        "hp pavilion 11 f105tu": 1247,
        "hp omen 15 ce523tx": 107,
        "smartfren andromax a2": 667,
        "fitti tape rainbow xl 34": 108,
        "samsung ua40m5000ak": 1249,
        "happy diapers l 26": 109,
        "nepia genki pants m 32": 2095,
        "sony alpha a9": 685,
        "hp spectre x360 13 ae520tu": 1251,
        "xiaomi mi 6": 1252,
        "fitti daypants l 48": 110,
        "xiaomi mi 8": 1253,
        "apple macbook pro mpxw2": 1254,
        "apple ipad air 2 lte": 1255,
        "asus zenfone live": 111,
        "lg 43lj550t": 112,
        "coocaa 40e2a22g": 113,
        "ichiko s5588": 114,
        "mito 3211": 1258,
        "mito 3218": 718,
        "canon ixus 285 hs": 115,
        "lenovo phab plus": 116,
        "samsung ua55nu7300": 2199,
        "panasonic th 43f306g": 1260,
        "hp 14 af115au": 117,
        "sweety bronze pants m 34+4": 118,
        "merries pants good skin xl 38": 1261,
        "samsung ua65nu8000": 1262,
        "samsung 32j4003": 749,
        "ichiko st4879": 1264,
        "xiaomi redmi 4a": 119,
        "sony a6300": 120,
        "brandcode l1f": 121,
        "oppo r9s plus": 2236,
        "akari le 32m89ab": 1265,
        "dell latitude 7280": 122,
        "xiaomi redmi 4x": 123,
        "sensi dry m40": 124,
        "acer aspire e5 552g": 125,
        "samsung 49k6300": 1508,
        "mamamia pants xl26": 126,
        "nikon d850": 127,
        "canon eos m10": 1267,
        "samsung galaxy on7": 128,
        "samsung galaxy on5": 129,
        "goon smile baby night pants m22": 1720,
        "asus rog gl503vs": 130,
        "sharp lc 32le265m": 196,
        "sensi regular pants xl 24": 704,
        "lenovo yoga 310": 1271,
        "samsung galaxy tab a 8.0 2017": 1272,
        "apple iphone x": 197,
        "sony kdl 40w660e": 806,
        "wiko jerry 3": 1275,
        "motorola moto c plus": 1722,
        "sharp lc 32le179i": 132,
        "hp 14 bs711tu": 133,
        "asus rog gl503vm": 134,
        "oppo a73s": 2103,
        "ichiko s5058": 135,
        "hp pavilion 14 bf004tx": 136,
        "evercoss jump tv": 1277,
        "asus rog gl503vd": 137,
        "ichiko st3276": 1278,
        "goo.n pants m32": 842,
        "advan i5c plus": 1280,
        "msi gt72 6qd dominator g": 1281,
        "canon powershot sx240 hs": 1282,
        "apple ipad": 1283,
        "apple watch series 3 gps+lte": 139,
        "huawei nova 2": 1284,
        "huawei nova 3": 1285,
        "panasonic lumix dmc tz110": 140,
        "asus vivobook a405uq": 1286,
        "akari le 24k88": 141,
        "mamypoko soft sensation tape nb62": 1540,
        "lenovo yoga 500": 1724,
        "fujifilm x t20": 142,
        "apple macbook pro mr962": 1287,
        "asus n552vx": 1288,
        "lg 65uk6300": 1541,
        "sharp fhd 40sa5100i": 143,
        "apple watch series 3 gps": 144,
        "lenovo b40": 1542,
        "fujifilm x pro2": 145,
        "asus x453ma": 146,
        "asus rog fx502vm": 147,
        "huawei y7 prime": 198,
        "toshiba 32l2605vj": 1292,
        "xiaomi redmi 4 prime 3": 1349,
        "samsung galaxy xcover 4": 1293,
        "lg 49lk5400": 925,
        "ichiko st3976": 149,
        "philips 32pht4002": 1924,
        "xiaomi mi 4 3": 1295,
        "changhong 32g4a": 1296,
        "ichiko s4878": 151,
        "samsung 65mu6100": 152,
        "samsung 48j5100": 1350,
        "sharp lc 58ue630x": 1297,
        "samsung galaxy on5 2016": 2178,
        "samsung qa55q7f": 1727,
        "akari le 65d88": 1298,
        "baby happy pants m20": 153,
        "coocaa 32a4": 154,
        "goo.n smile baby pants l20": 1301,
        "apple macbook pro mr9q2": 1302,
        "akari le 55d88sb": 155,
        "pampers premium care pants xl 21": 955,
        "ichiko st3996": 157,
        "sony xperia x": 158,
        "huawei porche design mate 10": 1304,
        "toshiba 49l3750vj": 1305,
        "msi gt73evr titan": 159,
        "merries pants good skin s 40": 160,
        "samsung galaxy tab s2 9.7": 1307,
        "nikon coolpix s1200pj": 161,
        "nokia 6.1 plus": 1544,
        "lenovo miix 720": 1308,
        "apple iphone 7 plus": 1309,
        "panasonic lumix dc gf9k": 203,
        "changhong 19d1000": 163,
        "niko nkled1902": 164,
        "huawei honor 7x": 1649,
        "huawei y5 ii": 1311,
        "dell inspiron 7577": 1424,
        "polytron pld32t106": 165,
        "hp 14 bs091tx": 2107,
        "asus x555dg": 1493,
        "polytron pld32t100": 166,
        "samsung galaxy alpha": 1314,
        "hp pro x2 612 g2": 167,
        "oppo a77 4": 1315,
        "samsung galaxy s9 4": 1971,
        "toshiba 24s2500": 168,
        "hp pavilion 11 f103tu": 1317,
        "huawei honor 8": 959,
        "samsung galaxy s6": 1888,
        "xiaomi mi tv 4c": 1959,
        "acer aspire 6 captain america edition": 169,
        "asus zenfone 3 zoom ze553kl": 170,
        "sony cybershot dsc rx100 ii": 171,
        "asus zenfone 3 ze552kl": 1931,
        "itel s11": 1319,
        "asus vivobook flip tp410ur": 172,
        "sony a5000": 1320,
        "polytron pld24t8511": 173,
        "samsung galaxy a8 2016": 1321,
        "asus padfone s": 1172,
        "oppo f1 plus": 1939,
        "lenovo z41": 1322,
        "ichiko st3296": 1143,
        "lenovo thinkpad t470": 175,
        "samsung galaxy a8 2018": 1324,
        "apple iphone 5": 176,
        "apple iphone 4": 177,
        "apple iphone 7": 178,
        "apple iphone 6": 179,
        "asus pegasus 2": 1325,
        "xiaomi redmi 3s 2": 1326,
        "advan itab": 181,
        "apple iphone 8": 182,
        "samsung galaxy note 9": 1476,
        "alcatel 1054d": 1328,
        "acer aspire es1 432": 1329,
        "msi gp62 7rex": 183,
        "sony cybershot dsc rx1r ii": 184,
        "panasonic th 49f306g": 1732,
        "pampers premium care pants l 62": 185,
        "xiaomi redmi 5a 2": 186,
        "aqua le24aqt6500t": 187,
        "toshiba portege x20w": 1333,
        "canon powershot sx740 hs": 1334,
        "mamypoko x tra dry pants xxl18": 188,
        "dell inspiron 5368": 965,
        "hp probook 240 g4": 1335,
        "xiaomi mi mix 2s": 1336,
        "hp probook 240 g6": 1337,
        "samsung ua43m5100dk": 190,
        "coocaa 55g2": 2111,
        "asus x550ze": 1338,
        "baby happy pants m 34": 1339,
        "lenovo vibe k5 plus": 191,
        "polytron 24d8520": 1340,
        "apple iphone xs max": 192,
        "sony kd 65x8500f": 283,
        "sony kd 65x8500e": 194,
        "huawei p10 4": 1342,
        "motorola moto z force": 2194,
        "asus zenfone 2 laser ze601kl": 1734,
        "mamypoko x tra dry pants l 44": 195,
        "xiaomi redmi 2 prime": 1552,
        "huawei mediapad t2 7.0": 1343,
        "toshiba satellite l15": 1031,
        "asus zenfone 3 deluxe": 1364,
        "sony a99 ii": 1346,
        "asus zenfone 5z zs620kl 8": 1347,
        "dell vostro 5468": 1348,
        "acer aspire e5 571g": 2232,
        "sony a7": 1344,
        "akari le25b88": 1290,
        "samsung 32k4100": 199,
        "fujifilm gfx 50s": 200,
        "sony klv 32r302": 201,
        "asus zenfone 5z zs620kl 4": 1351,
        "brandcode b1 legenda": 1352,
        "nikon coolpix b500": 1353,
        "akari le 50d88sb": 855,
        "acer aspire one 14": 1310,
        "huawei y6 2018": 204,
        "hp elitebook 1040": 1356,
        "acer aspire one 10": 1357,
        "changhong le40d1200": 1735,
        "xiaomi redmi 3 2": 1358,
        "lg 55uj632t": 1359,
        "panasonic th 55e306g": 1504,
        "ichiko s4998": 2260,
        "ichiko s1988": 1360,
        "pampers premium care pants xxl 17": 206,
        "hp pavilion 14 ab133tx": 1362,
        "nikon coolpix l610": 1363,
        "lg 60uh650t": 207,
        "hp pavilion 14 ab127tx": 1345,
        "asus zenfone 2 laser ze500kl": 209,
        "fitti daypants m 18": 210,
        "coocaa 32e28w": 1365,
        "polytron pld24d811": 1737,
        "mamypoko pants airfit l 44": 211,
        "hp elitebook 1030": 212,
        "hp zbook 14": 1859,
        "asus s410uf eb023t": 2183,
        "sharp 24le170": 213,
        "olympus om d e m1 mark ii": 1366,
        "sweety silver pants l 36": 1367,
        "mamypoko soft sensation tape m54": 1368,
        "apple ipad 9.7 2018": 1369,
        "mito 135": 214,
        "apple ipad 9.7 2017": 1370,
        "sony dsc rx100 iv": 1962,
        "samsung galaxy a7 2017": 216,
        "samsung galaxy a7 2016": 217,
        "changhong 50e6000hft": 218,
        "asus rog gl702vm": 1372,
        "sharp lc 50ue630x": 1373,
        "ichiko s3978": 1374,
        "oppo f9 pro": 2027,
        "mamypoko extra soft pants s 70": 219,
        "hp 14 bw512au": 1376,
        "mamypoko x tra dry pants xl 26": 220,
        "apple ipad mini": 221,
        "asus rog g551jw": 1377,
        "samsung galaxy e7": 222,
        "dell alienware 18": 223,
        "hp omen 15 ce087tx": 1378,
        "meizu m3s": 224,
        "happy nappy smart pantz m 34": 1379,
        "hp 14 bs001tu": 226,
        "sweety bronze pants s 36+4": 1381,
        "samsung 49mu8000": 227,
        "dell alienware 17": 228,
        "apple macbook pro mptv2": 1382,
        "dell alienware 15": 229,
        "evercoss s45 xtream 1": 1383,
        "mamypoko extra dry pants xxl 22": 230,
        "polytron pld40ts853": 1385,
        "samsung galaxy j4 plus": 231,
        "evercoss winner x glow r45": 232,
        "polytron pld40s153": 1941,
        "sony xperia xz": 234,
        "samsung galaxy tab a 7.0 2016": 1388,
        "toshiba 32l3750": 235,
        "dell latitude e7440": 1389,
        "sanken sle 24": 236,
        "mamypoko x tra dry pants m 34": 237,
        "fujifilm x e3": 1390,
        "acer aspire e5 474g": 1391,
        "apple ipad 3 wi fi": 238,
        "dell inspiron 3552": 239,
        "asus zenfone 3 max zc553kl": 240,
        "nikon d5300": 1393,
        "xiaomi redmi 6 4": 2254,
        "apple macbook mnyg2": 241,
        "fujifilm x a10": 1180,
        "aqua lc32le180i": 2186,
        "msi gt72 6qe dominator pro": 1395,
        "lg 55uk6300": 242,
        "changhong l39g3": 174,
        "apple ipad mini 2": 243,
        "apple ipad mini 3": 244,
        "apple ipad mini 4": 245,
        "aqua aqt6900f": 1396,
        "toshiba 43l3750vj": 1397,
        "acer aspire es1 132": 1399,
        "acer aspire es1 131": 1400,
        "changhong 40g5i": 1401,
        "xiaomi mi max": 246,
        "asus transformer 3 pro t303ua": 247,
        "huawei y5 2017": 2121,
        "acer aspire e5 473g": 248,
        "canon powershot g7x mark ii": 1418,
        "apple iphone 5s": 1402,
        "sony dsc rx1r": 249,
        "mamamia pants l30": 1404,
        "nokia 105": 250,
        "lg 55sk8000": 251,
        "sony dsc wx220": 252,
        "lenovo k6 power": 253,
        "samsung galaxy j3 2017": 1746,
        "mamamia pants m34": 254,
        "samsung 49ks7000": 255,
        "sharp lc 40sa5100i": 256,
        "mito t55": 1408,
        "asus x555qg": 1409,
        "coocaa 32a212t": 1410,
        "dell alienware m15x": 257,
        "apple ipad 2017 lte": 1411,
        "polytron pld32d710": 2122,
        "asus x555qa": 1412,
        "lenovo yoga 520": 1413,
        "samsung galaxy tab s2 8.0": 2123,
        "oppo find x": 1415,
        "asus a407ua": 258,
        "asus a407ub": 259,
        "lg 43lw300c": 1416,
        "lg 49uj632t": 260,
        "huawei watch": 261,
        "lg 55uk6540": 262,
        "asus zenpad 10 z301m": 263,
        "ichiko s5596": 264,
        "polytron pld32ts1503": 265,
        "apple macbook pro mpxt2": 1420,
        "sweety silver pants s 66": 1421,
        "acer aspire e5 573g": 266,
        "huawei mediapad t1": 2271,
        "xiaomi redmi note 3": 267,
        "xiaomi redmi note 2": 268,
        "motorola moto g6": 763,
        "merries pants m 28": 270,
        "acer predator helios 500": 271,
        "xiaomi redmi note 5": 272,
        "xiaomi redmi note 4": 273,
        "philips 39pht4002": 1749,
        "merries pants good skin xl 26": 1425,
        "lg 49lj510t": 1426,
        "sharp lc 40le185i": 274,
        "huawei nova 3e": 1506,
        "polytron pld32t7511": 2092,
        "sony kd 75x8500f": 1428,
        "lg 65uh650t": 1429,
        "sharp lc 24le170i": 1430,
        "dell inspiron 3179": 275,
        "sony kdl 49w750d": 1431,
        "xiaomi redmi 3s prime 3": 276,
        "canon powershot n2": 277,
        "dell inspiron 13 7348": 1432,
        "apple ipad wi fi 3g": 1433,
        "sony cybershot dsc w710": 278,
        "coocaa 32e2a12g": 279,
        "samsung galaxy tab s3 lte": 280,
        "asus zenpad c 7.0": 1371,
        "dell inspiron 7373": 1436,
        "huawei y7 pro 2018": 1437,
        "samsung galaxy a8 2018 4": 1438,
        "hp 14 bs702tu": 1439,
        "samsung galaxy a9 pro": 1440,
        "changhong le19d1000": 1186,
        "coocaa 32e2a12t": 281,
        "samsung galaxy tab s 8.4": 282,
        "mito 5011": 1441,
        "asus zenfone 4 selfie lite": 1951,
        "sony klv 40r352c": 1442,
        "asus x555la": 1611,
        "dell inspiron 7353": 1755,
        "fitti gold pants s58": 1443,
        "xiaomi mi a1 4": 284,
        "acer aspire z1401": 285,
        "toshiba 32p2400": 1444,
        "huawei y6 ii": 286,
        "acer aspire z1402": 287,
        "sharp lc 60le580x": 1445,
        "ichiko s3278": 288,
        "hp 14 an002ax": 1446,
        "sony xperia xa1 ultra": 1447,
        "lenovo phab plus 2": 289,
        "apple ipad 2 wi fi": 1449,
        "lg 22mt48af": 290,
        "huawei y3 2017": 2227,
        "samsung galaxy j5 prime": 291,
        "mamypoko junior night pants xxl 14": 1398,
        "pampers premium care pants m 46": 1451,
        "apple ipad 4": 293,
        "asus zenfone max pro": 1452,
        "hp 240 g5": 1375,
        "samsung ua32j4005dk": 294,
        "goon smile baby night pants xl26": 295,
        "dell inspiron 7359": 1757,
        "ichiko s1518": 1453,
        "samsung ua43k5005": 1454,
        "sensi dry nb12": 296,
        "pokana pants surprise design xl 42": 2118,
        "mobiistar e selfie": 297,
        "samsung galaxy gear": 298,
        "asus zenbook ux410uq": 1456,
        "lenovo vibe k6 note": 1457,
        "lenovo thinkpad x240": 1458,
        "oppo r17 pro": 299,
        "asus zenfone 2 laser": 1460,
        "panasonic th 32d305g": 300,
        "coocaa 32e21": 1461,
        "merries pants xl 19": 1462,
        "huawei p9": 301,
        "motorola moto z play": 1464,
        "canon powershot sx540 hs": 302,
        "changhong g3a": 2077,
        "asus a45vd": 2128,
        "sweety silver pants m 18+2": 1549,
        "samsung 55k6300": 2250,
        "sweety silver pants xl 26": 303,
        "sony klv 32r302e": 1312,
        "samsung galaxy c7 pro": 304,
        "goo.n smile baby pants xxl24": 1466,
        "htc desire 650": 1467,
        "panasonic th 40f305g": 305,
        "panasonic th 43e302g": 306,
        "samsung galaxy tab s 8.4 lte": 1468,
        "sanken sle 328dhs": 1469,
        "asus a456ur": 1459,
        "mito 199": 1193,
        "alcatel a5": 1470,
        "lg 65uh61": 307,
        "asus x441na": 308,
        "sweety silver pants xl 44": 1014,
        "huawei honor 5a": 2102,
        "lenovo thinkpad x1 carbon": 309,
        "lg 24mt48": 1194,
        "samsung ua32eh4003mxxd": 1958,
        "dell inspiron 7460": 311,
        "coocaa 24e100": 1471,
        "sweety silver pants l 18+2": 312,
        "hp pavilion 14 bf155tx": 1472,
        "panasonic lumix dc g9": 2109,
        "fitti gold pants xxl38": 313,
        "samsung 65q8c": 1474,
        "pampers premium care pants m 30": 1602,
        "xiaomi mi a2 lite redmi 6 pro 3": 314,
        "sweety pants gold s 36": 1475,
        "asus rog zephyrus gx501vi": 788,
        "samsung ua49j5200akpxd": 316,
        "baby happy pants l 30": 1341,
        "xiaomi mi a2 lite redmi 6 pro 4": 317,
        "hp envy 13 ad139tx": 318,
        "samsung galaxy note 8": 1477,
        "toshiba 32l2605": 1570,
        "lg 24mt48af": 1195,
        "evercoss winner z extra": 1478,
        "mamamia baby soft magic tape m20": 1380,
        "nikon coolpix a900": 320,
        "samsung galaxy note 3": 1479,
        "polytron pld22d1150": 321,
        "samsung galaxy note 5": 1480,
        "samsung galaxy note 4": 1481,
        "samsung galaxy note 7": 1482,
        "sweety bronze pants s 20+2": 1483,
        "polytron pld24d9501": 322,
        "nikon coolpix l810": 323,
        "huawei mediapad m3 8.4": 1485,
        "asus transformer t100ha": 2033,
        "toshiba 22l2800": 324,
        "sony xperia xz1 compact": 325,
        "vivo v5 lite": 1975,
        "panasonic th 55ex400g": 790,
        "asus rog gl552vx": 327,
        "evercoss one x": 328,
        "dell latitude e5430": 1487,
        "arsenal vr one": 329,
        "lenovo ideapad s2 1": 1488,
        "sony kdl 32r300e": 873,
        "samsung galaxy j2 pro 2016 2": 1490,
        "samsung ua32j4003": 1961,
        "asus rog gl552vw": 330,
        "apple watch series 4 aluminum": 1701,
        "sony cybershot dsc rx100 va": 331,
        "pampers premium care pants s 26": 1257,
        "oppo r7 plus": 1492,
        "itel s31": 1629,
        "hp envy 13 ad001tu": 1384,
        "sony xperia xa1 plus": 333,
        "asus a405uq": 1197,
        "lg oled55b8pta": 334,
        "merries tape m 22": 1494,
        "lg 55uj652t": 335,
        "asus zenfone ar": 336,
        "lenovo thinkpad yoga 14": 337,
        "canon powershot g9 x mark ii": 338,
        "xiaomi pocophone f1": 1574,
        "sweety silver pants m 60": 1496,
        "mito a39": 340,
        "evercoss winner y smart plus": 1498,
        "polytron pld32t710": 341,
        "asus vivobook flip tp201sa": 342,
        "mamypoko x tra dry pants l 30": 343,
        "huawei nova 3i": 1500,
        "asus zenfone 3 deluxe zs570kl": 1501,
        "asus a555lf": 344,
        "samsung galaxy tab 3 v": 345,
        "panasonic th 24e302g": 1502,
        "evercoss winner y smart": 1503,
        "samsung galaxy tab s3": 412,
        "oppo a71": 347,
        "oppo a77": 348,
        "oppo a75": 349,
        "huawei nova 2 plus": 350,
        "xiaomi mi max 2 4": 351,
        "panasonic th 32ds500g": 1484,
        "hp envy 13 ad001tx": 1507,
        "lg 43uk6500": 352,
        "samsung ua49m5100": 1509,
        "canon eos 6d": 353,
        "asus zenpad 8.0 z380kl 2": 354,
        "samsung galaxy tab s 10.5": 355,
        "mito 333": 1512,
        "lenovo ideapad 300": 413,
        "dell latitude 5289": 357,
        "nikon coolpix s5300": 6,
        "nikon coolpix l320": 358,
        "panasonic th 43es630g": 8,
        "samsung galaxy j7 2016": 205,
        "lenovo k6 note": 16,
        "toshiba 23s2400vj": 360,
        "philips 50put6002": 361,
        "polytron pld55uv5900": 1516,
        "huawei y5 prime 2018": 362,
        "infinix zero 5": 363,
        "huawei nova 3 6": 24,
        "merries pants good skin l 44": 800,
        "asus zenfone max pro zb602kl 3": 1518,
        "panasonic th 43e305g": 1519,
        "xiaomi mi 5c 3": 1520,
        "ichiko s1998": 37,
        "aqua le40aqt8300": 367,
        "vivo y53": 368,
        "canon eos 700d": 1523,
        "pampers premium care adhesive nb 52": 2177,
        "sharp lc 40sa5200i": 487,
        "coocaa 40e6": 1524,
        "coocaa 40s3a12g": 801,
        "asus zenpad 8.0": 371,
        "apple iphone 4s": 1526,
        "lg oled65c7t": 1527,
        "asus zenfone 4 pro zs551kl 6": 1767,
        "lenovo tab3 7": 1528,
        "sony kdl 55w650d": 374,
        "xiaomi redmi 4a 2": 1529,
        "ichiko s3998": 86,
        "acer aspire e5 575g": 1530,
        "huawei honor 9 lite": 1768,
        "lg 55sk8500": 1776,
        "hp probook 430 g5": 802,
        "canon eos r": 1004,
        "xiaomi mi mix": 1532,
        "mamypoko extra soft pants l 28": 100,
        "apple ipad 3 wi fi cellular": 1392,
        "sony a7r mark iii": 377,
        "msi gp62mvr 7rfx": 1581,
        "pampers premium care adhesive nb 26": 378,
        "polytron pld24d8511": 1534,
        "panasonic th 22f302g": 1535,
        "pokana pants surprise design m 58": 2210,
        "huawei mate 10 pro 4": 1536,
        "huawei mate 10 pro 6": 1537,
        "sony dsc rx100 ii": 1969,
        "sweety pants gold s 66": 2279,
        "hp 14 bs710tu": 1538,
        "toshiba satellite c55": 1539,
        "toshiba 55l3750": 1738,
        "toshiba 43u7750vj": 379,
        "huawei watch 2": 380,
        "mito 2461": 381,
        "samsung galaxy j5 2016": 382,
        "panasonic lumix dmc g7": 383,
        "asus rog g551vw": 384,
        "lenovo thinkpad l380": 1134,
        "motorola moto e4 plus": 385,
        "pokana pants surprise design xl 20": 805,
        "drypers drypantz convenient pack xl 14": 387,
        "genki moko pants m19": 1545,
        "htc desire 12": 2185,
        "mamypoko junior night pants xxxl 24": 388,
        "sanken sle 32": 390,
        "canon eos 80d": 391,
        "asus k401uq": 1548,
        "samsung 43j5202": 392,
        "hp 14 bw511au": 393,
        "dell latitude e7470": 1550,
        "acer aspire z476": 1551,
        "dell latitude 3180": 394,
        "fitti tape rainbow s 26": 1553,
        "panasonic th 24e303g": 1582,
        "akari le 40p88": 1680,
        "msi gf63 8rc": 1973,
        "huggies little swimmer s 12": 2212,
        "alcatel pixi 4": 1554,
        "akari le 20k88": 433,
        "changhong 55e6000i": 1555,
        "coocaa 55g7200": 395,
        "canon powershot sx60 hs": 1557,
        "huawei nova 3i 4": 2146,
        "samsung galaxy tab 3 v 1": 1558,
        "mito 151": 1559,
        "asus x540la": 1560,
        "acer switch alpha 12": 1561,
        "sweety pants gold l 28": 2207,
        "sharp lc 24le175": 1562,
        "samsung ua32n4300": 397,
        "mobiistar lai zumbo s 2017": 418,
        "asus zenfone 3 zoom": 399,
        "changhong e6000hf": 400,
        "huawei p9 lite": 401,
        "lg 55sj850t": 1905,
        "hp 14 bw500au": 1563,
        "nokia 130": 402,
        "ichiko st5596": 403,
        "hp spectre x360 13 ae518tu": 404,
        "mamamia pants l20": 1565,
        "hp 14 an017au": 405,
        "xiaomi redmi 3x": 1205,
        "acer aspire e5 476g": 1700,
        "apple macbook air mqd42": 292,
        "dell latitude e5250": 1772,
        "toshiba 32l1600vj": 1797,
        "akari le 32p88": 1206,
        "lenovo thinkpad e31": 408,
        "lenovo yoga 530": 1568,
        "dell inspiron 3467": 1569,
        "apple ipad pro 12.9": 1491,
        "dell inspiron 3462": 545,
        "asus x555ba": 1572,
        "asus a442uq": 409,
        "asus transformer t300 chi": 332,
        "sony kdl 48w650d": 1977,
        "samsung 40k6300": 1587,
        "apple macbook pro mpxu2": 339,
        "nepia genki pants l 30": 410,
        "samsung galaxy tab s4": 411,
        "panasonic th 32f305g": 346,
        "asus x555bp": 1575,
        "pampers premium care pants s 48": 356,
        "panasonic th 32d306g": 2145,
        "lenovo ideapad 305": 414,
        "sweety pants gold m 60": 1578,
        "hp omen 15 ce086tx": 1978,
        "canon powershot g7 x": 372,
        "brandcode b81": 1580,
        "hp elitebook 840": 1,
        "sony kd 55a8f": 415,
        "lenovo vibe shot": 1588,
        "xiaomi redmi 6a": 416,
        "nepia genki tape s 72": 417,
        "hp 14 am015tx": 1583,
        "sony alpha 77": 1584,
        "lg 32lj500d": 398,
        "canon powershot a810": 1209,
        "sharp lc 45ua6800x": 1585,
        "acer aspire e5 475g": 1586,
        "canon powershot sx720 hs": 1210,
        "lg 55uh770t": 419,
        "asus zenfone 3 max zc520tl": 1739,
        "dell inspiron 3168": 420,
        "lenovo a6600 plus": 421,
        "samsung 65ls003": 1589,
        "apple macbook pro mpxr2": 422,
        "msi gs63vr stealth pro": 423,
        "samsung 43n5003": 424,
        "ichiko s1598": 425,
        "hp 14 an004au": 1405,
        "asus zenfone 4 selfie lite zb553kl 2": 426,
        "samsung 43m5100": 427,
        "oppo find x 8": 428,
        "samsung 40ku6300": 1860,
        "apple macbook mnyj2": 429,
        "coocaa 24d1a": 1644,
        "coocaa 24w3": 1780,
        "coocaa 43e6": 2247,
        "asus zenbook ux360ua": 477,
        "asus rog g752vy": 697,
        "hp omen 15 ce501tx": 2101,
        "asus zenpad 3 8.0": 430,
        "ichiko s4098": 431,
        "asus zenwatch 3": 1593,
        "asus zenwatch 2": 1594,
        "apple ipad 2018 wifi": 2009,
        "lg 43uj632t": 1595,
        "lenovo yoga 370": 2224,
        "asus rog phone": 815,
        "panasonic th 43e306": 825,
        "samsung 49m5050": 434,
        "sharp lc 32le185i": 1597,
        "hp envy x360": 1753,
        "apple macbook pro mlw72": 435,
        "coocaa 24e2000t": 1598,
        "dell inspiron 11 3180": 2151,
        "lg 49sj800t": 436,
        "sony kd 65x9000e": 437,
        "sony kd 65x9000f": 438,
        "goon excellent dry tape s44": 1600,
        "xiaomi mi notebook pro": 439,
        "mamypoko extra dry tape nb 52": 440,
        "goon smile baby night pants xl17": 441,
        "oppo a83 2018 4": 442,
        "philips 43pft4002": 1403,
        "oppo a83 2018 2": 443,
        "oppo a83 2018 3": 444,
        "toshiba 32l5650": 818,
        "toshiba 32l2800vj": 1603,
        "samsung 55mu8000": 446,
        "vivo v5": 1605,
        "polysonic 3200": 447,
        "lenovo thinkpad x250": 1607,
        "strawberry flip 1272": 448,
        "polytron pld32t1506": 449,
        "hp spectre x360 13 ae077tu": 450,
        "polysonic 1777": 451,
        "polytron pld43v863": 1610,
        "dell latitude 7390": 2061,
        "mito 366 slim elite": 452,
        "asus zenfone selfie": 453,
        "samsung 55mu7000": 1783,
        "goo.n pants xxl19": 1434,
        "sony kd 55a1": 454,
        "asus x453sa": 455,
        "asus x555lf": 1612,
        "baby happy tape xl20": 456,
        "goo.n smile baby pants xxl18": 1614,
        "xiaomi mi notebook air": 1615,
        "strawberry st188": 457,
        "sweety silver pants xl 34": 458,
        "niko nk1702": 459,
        "apple ipad mini 3 wifi": 1592,
        "sony a6500": 460,
        "sony cybershot dsc w800": 483,
        "lenovo vibe c": 1616,
        "sharp lc 32le295i": 1617,
        "apple ipad air 2 wifi": 1618,
        "samsung galaxy note 9 8": 1619,
        "drypers drypantz mini jumbo pack m 30": 461,
        "ichiko s3298": 1620,
        "mamypoko extra dry pants m 32": 1621,
        "asus transformer tp300lj": 462,
        "apple watch sport 42mm 1st gen": 839,
        "oppo f5 youth": 464,
        "huawei mate 10 pro": 675,
        "mito 1770": 466,
        "oppo f7 6": 467,
        "oppo a71 2018": 1624,
        "oppo f7 4": 468,
        "sony a6000": 2217,
        "apple macbook air mqd32": 1406,
        "samsung ku6300": 689,
        "sony xperia l2": 1626,
        "sony kd 65a8f": 820,
        "asus a455lf": 471,
        "nikon d7500": 699,
        "asus a455lb": 473,
        "apple iphone 5c": 1407,
        "asus vivobook flip 14 tp410ur": 1628,
        "asus a455la": 474,
        "asus a455ln": 475,
        "wiko jerry 2": 1274,
        "asus a455lj": 476,
        "apple iphone se": 1591,
        "canon eos 7d": 478,
        "samsung 55nu7100": 927,
        "xiaomi mi note 3": 480,
        "xiaomi mi note 2": 481,
        "hp 14 bs747tu": 482,
        "mamypoko extra soft pants l 52": 77,
        "samsung galaxy tab a 8.0": 1632,
        "coocaa 50e700": 484,
        "lg 32lk500d": 1633,
        "nokia 105 2017": 1634,
        "oppo r15 pro": 485,
        "hp 14 bs503tx": 972,
        "fujifilm x t1 gs": 486,
        "toshiba 22l2800vj": 1543,
        "sweety pants gold m 34": 530,
        "lg 65sk8000": 758,
        "samsung 65ku6000": 760,
        "niko nkled2302wa": 1636,
        "nikon coolpix s01": 489,
        "baby happy pants xl 26": 1220,
        "nikon coolpix s02": 490,
        "huawei mate 10 lite 4": 491,
        "smartfren andromax b se": 492,
        "dell precision 5510": 1639,
        "evercoss winner y star plus": 493,
        "apple ipad pro 2017 10.5": 783,
        "polytron pld40d100": 495,
        "samsung 49mu6300": 1641,
        "panasonic th l32b6g": 1642,
        "lenovo thinkpad p51": 1643,
        "lenovo thinkpad x1 c5": 496,
        "oneplus 6": 1645,
        "polysonic ps 1892i": 497,
        "ichiko s1918": 498,
        "huawei mate 10 lite": 499,
        "sony kd 65x7000f": 2156,
        "panasonic th 40d302g": 1648,
        "pampers premium care pants l 42": 500,
        "lenovo thinkpad 1": 501,
        "sweety bronze pants xl 26+4": 824,
        "lenovo thinkpad e465": 503,
        "changhong 32e6000i": 830,
        "fujifilm x a20": 1651,
        "lenovo thinkpad e460": 505,
        "samsung z2": 506,
        "toshiba 24l2615": 507,
        "huawei honor 8 pro": 508,
        "lenovo thinkpad t440": 1986,
        "happy nappy smart pantz xl26": 844,
        "acer aspire vx 15": 1653,
        "akari le 50d881d": 1654,
        "apple watch edition series 2 38mm": 1655,
        "hp 14 bw083tu": 1656,
        "mamypoko soft sensation tape s 58": 510,
        "mamamia baby soft magic tape l36": 1658,
        "olympus om d e m10": 1659,
        "apple iphone 8 plus": 1556,
        "akari le 3289t2": 511,
        "aqua 32aqt7000t": 1596,
        "sharp lc 40le185": 512,
        "polytron pld32d1500": 513,
        "asus x455dg": 1662,
        "goo.n pants l26": 1601,
        "asus x441ma": 514,
        "asus zenpad c 7.0 1": 515,
        "sweety bronze pants xxl 24+2": 767,
        "dell precision m3800": 1663,
        "sony kdl 43w660f": 517,
        "strawberry voxy st1": 518,
        "sony dsc wx350": 2222,
        "motorola moto c": 519,
        "asus rog g701vi": 520,
        "apple watch series 2 nike": 521,
        "toshiba satellite l745": 1666,
        "motorola moto g": 522,
        "aqua le49aqt1000u": 523,
        "toshiba 32l2615": 1667,
        "acer aspire e5 575": 2165,
        "motorola moto m": 524,
        "lg 49uk6300": 1223,
        "canon eos 5d mark iv": 1417,
        "sony dsc rx10": 1495,
        "hp probook 440 g4": 525,
        "hp probook 440 g5": 526,
        "hp probook 440 g2": 940,
        "hp probook 440 g3": 528,
        "motorola moto z": 529,
        "sharp lc 32le180i": 822,
        "lenovo flex 3": 531,
        "huawei y9 2018 3": 1671,
        "panasonic th 32d400g": 971,
        "brandcode b5": 1323,
        "hp pavilion 15 af109ax": 1674,
        "lg 65uk6540": 532,
        "lg 49uj652t": 533,
        "samsung galaxy j2 pro": 534,
        "samsung galaxy a3 2016": 1676,
        "motorola moto g6 plus": 1677,
        "lg 70uk6540": 535,
        "huawei honor 6x": 1993,
        "coocaa 40d3a": 537,
        "alcatel 4034f": 1822,
        "toshiba 55u9650vj": 538,
        "evercoss winner t ultra r40a": 539,
        "panasonic th 32e305g": 1024,
        "mito 3221": 1419,
        "lenovo vibe k4 note": 2261,
        "dell latitude 3380": 2049,
        "samsung 55k5100": 1963,
        "samsung 40ku6000": 1678,
        "wiko u feel go": 541,
        "xiaomi mi 4c": 2158,
        "mamypoko extra dry pants l30": 542,
        "samsung galaxy c5 pro": 543,
        "olympus om d e m1": 1681,
        "nikon coolpix w100": 1682,
        "samsung galaxy j1 ace": 1714,
        "olympus om d e m5": 1062,
        "canon eos rebel t6": 544,
        "changhong 43d3000i": 2159,
        "acer aspire s3 391": 1685,
        "mamamia baby soft magic tape l20": 1497,
        "asus x505za": 1687,
        "hp pavilion 14 ab033tx": 1103,
        "dell vostro 3478": 1801,
        "mamypoko pants airfit xl 38": 1689,
        "huawei nova 2i": 1690,
        "motorola moto z2 force": 546,
        "samsung 58nu7103": 1802,
        "changhong 32d3000i": 547,
        "panasonic th 32e302g": 1692,
        "coocaa 39w3": 1125,
        "apple macbook pro mptt2": 1693,
        "hp elitebook folio 1040": 1140,
        "lg 43lk5000": 549,
        "nikon coolpix b700": 1696,
        "toshiba 32p1400vj": 550,
        "huawei p9 plus": 2029,
        "gigabyte aero 15 x": 551,
        "gigabyte aero 15 w": 552,
        "hp 14 bs010tu": 553,
        "oppo f3 plus": 1697,
        "asus x541sa": 1698,
        "ichiko s5568": 1699,
        "changhong 55d2200": 554,
        "nepia genki tape l 54": 269,
        "infinix hot 6": 556,
        "lenovo yoga 3 14": 1703,
        "xiaomi redmi 3s prime": 1623,
        "dell inspiron 3576": 557,
        "fitti daynight xl 44": 558,
        "samsung keystone 3": 559,
        "hp 14 an029au": 1704,
        "tecno camon cx": 560,
        "akari le 32v89": 561,
        "polytron pld32d9505": 562,
        "samsung 65ks9000": 1423,
        "mamypoko extra dry tape s 50": 563,
        "asus zenfone live l1 za550kl 2": 1805,
        "coocaa 43e2a22g": 225,
        "sony xperia xz1": 1708,
        "xiaomi mi 4s": 2161,
        "lg g7 thinq": 564,
        "sony xperia xz2": 1710,
        "acer aspire e5 475": 1711,
        "asus zenfone 4 selfie": 1712,
        "sensi dry s48": 548,
        "canon eos 750d": 565,
        "vivo v7": 1604,
        "sensi regular pants xxl 22": 1713,
        "mamamia pants l54": 89,
        "coocaa 50e2a12g": 1715,
        "samsung galaxy note fe": 1716,
        "asus fx553vd": 2162,
        "acer aspire switch 12": 1717,
        "acer aspire switch 10": 1718,
        "samsung 55q6fn": 567,
        "huawei p20 pro": 568,
        "hp envy 17t": 1719,
        "goo.n smile baby pants s40": 569,
        "olympus pen f": 1606,
        "goo.n smile baby pants xl20": 1233,
        "xiaomi mi a2": 570,
        "huawei nova 2 lite": 571,
        "huawei y6 prime 2018": 572,
        "xiaomi mi a1": 573,
        "toshiba 40l5650": 574,
        "samsung 43j5100": 575,
        "genki moko pants m8": 1723,
        "huawei porche design mate rs 6": 2218,
        "goo.n smile baby pants xl26": 1235,
        "changhong 40e2100": 576,
        "asus transformer t100chi": 1726,
        "vivo v9": 1608,
        "fujifilm x h1": 577,
        "samsung galaxy note 8 6": 1807,
        "sony kd 75x8500e": 1427,
        "dell inspiron 3476": 1728,
        "samsung galaxy s8 4": 1808,
        "lenovo ideapad 120s": 1911,
        "alcatel touch 890d": 1729,
        "samsung ua32n4003": 578,
        "mito 2231": 843,
        "sony xperia xzs": 1730,
        "canon powershot g9": 1731,
        "sony cybershot dsc rx100 v": 580,
        "lenovo v310": 1609,
        "asus zenfone max pro zb602kl 4": 1521,
        "canon powershot sx430 is": 1733,
        "infinix note 4 pro": 581,
        "canon eos 1200d": 1041,
        "lenovo ideapad 310": 582,
        "acer switch one 10": 583,
        "niko nk1903": 1736,
        "merries pants l 22": 584,
        "asus zenfone 3": 585,
        "asus zenfone 2": 586,
        "apple ipad pro 9.7": 587,
        "asus zenbook flip s ux370ua": 588,
        "asus zenfone 5": 589,
        "asus zenfone 4": 590,
        "asus zenfone go zb450kl": 1741,
        "sony xperia z1 compact": 1742,
        "nokia 6": 98,
        "genki moko pants xl15": 1743,
        "huawei p10": 591,
        "nikon d3200": 1744,
        "samsung galaxy j3 2016": 1745,
        "drypers drypantz convenient pack m 20": 592,
        "drypers drypantz mega pack m 60": 593,
        "hp pavilion 14 bf196tx": 594,
        "toshiba 32l3650": 1748,
        "panasonic th 40c304g": 2172,
        "sweety silver pants s 32": 595,
        "huawei y6 2": 1750,
        "huawei y6 1": 1751,
        "xiaomi mi a2 6x 6": 1752,
        "samsung gear s3": 596,
        "samsung gear s2": 597,
        "sony kd 55x8000e": 1566,
        "samsung 43m5500": 1754,
        "lg 55uk6100": 598,
        "sony xperia z4": 599,
        "sony xperia z5": 600,
        "samsung ua40j5250": 1756,
        "sony xperia z1": 601,
        "sony xperia z2": 602,
        "sony xperia z3": 603,
        "asus zenfone c": 604,
        "samsung 55m6300": 605,
        "asus a456uq": 606,
        "asus zenwatch 2 wi502q": 607,
        "coocaa 39e20w": 608,
        "coocaa 43e390": 609,
        "mamypoko extra soft pants xl 24": 610,
        "nokia x6": 180,
        "nokia x5": 1759,
        "asus x555da": 611,
        "hp x360 convertible 11 ab035tu": 1760,
        "wiko u pulse": 612,
        "panasonic th 43f302g": 613,
        "xiaomi mi pad 2": 1243,
        "panasonic th 24e305g": 615,
        "brandcode b68": 616,
        "lg 32lj510d": 617,
        "asus zenbook ux305ca": 618,
        "huggies little swimmer l 10": 1763,
        "asus zenfone 4 max zc520kl": 1613,
        "msi ps42": 1510,
        "panasonic lumix dc tz220": 1765,
        "mamamia baby soft magic tape s20": 619,
        "dell inspiron 5468": 1813,
        "huggies little swimmer m 11": 1766,
        "xiaomi black shark": 620,
        "genki moko pants xl6": 621,
        "canon eos m50": 622,
        "huawei y9 2018": 623,
        "huawei y9 2019": 624,
        "aqua le24aqt8300": 848,
        "strawberry st22": 2276,
        "panasonic th 32f306g": 626,
        "canon eos m100": 627,
        "asus zenbook ux303ub": 628,
        "sony xperia zr": 629,
        "drypers drypantz convenient pack l 18": 1770,
        "dell latitude 7480": 1771,
        "nokia 3.1": 630,
        "oppo f1s": 1773,
        "oppo r9s pro": 631,
        "lenovo thinkpad k2450": 1573,
        "apple ipad 2018 lte": 632,
        "sweety silver comfort l22": 633,
        "sony kd 55x7000f": 1435,
        "changhong 24e2000": 1777,
        "lenovo thinkpad x280": 1778,
        "philips 50pft4002": 1779,
        "toshiba 43u7750": 516,
        "samsung gear s3 classic": 634,
        "huawei p8 lite": 2265,
        "hp 14 bw099tu": 2266,
        "apple macbook pro mr9v2": 1781,
        "mamypoko x tra dry pants l20": 202,
        "changhong 32d2100t": 635,
        "xiaomi redmi 3 pro": 1782,
        "acer swift 5": 636,
        "apple ipad air 2": 1784,
        "acer swift 7": 637,
        "samsung galaxy tab a 8.0 s pen": 2220,
        "acer swift 1": 638,
        "vivo y81i": 1785,
        "hp 14 bw023ax": 639,
        "mamypoko extra dry tape nb 84": 640,
        "mamypoko extra dry pants m 21": 1786,
        "nikon 1 j5": 968,
        "samsung galaxy tab s3 wifi": 641,
        "lenovo thinkpad x230": 642,
        "evercoss winner y smart pro": 643,
        "acer predator helios 300": 644,
        "htc u play": 645,
        "sharp lc 50sa5200x": 373,
        "lenovo thinkpad yoga 260": 646,
        "hp omen 15 ce088tx": 647,
        "ichiko s1788": 648,
        "nikon coolpix a10": 2044,
        "sony kd 49x7000e": 2006,
        "niko nk2102": 1793,
        "sony cybershot dsc h90": 650,
        "xiaomi mi 4c 3": 651,
        "samsung galaxy a8 2018 6": 1795,
        "mamypoko soft sensation tape s26": 652,
        "nikon coolpix p1000": 653,
        "alcatel u5": 1796,
        "toshiba 32l2800": 193,
        "lg oled65e8pta": 1798,
        "xiaomi redmi note 4x": 1799,
        "hp pavilion 15 cb530tx": 1800,
        "asus fx503vm e4139t": 654,
        "fitti gold pants l50": 655,
        "merries tape nb 24": 656,
        "nikon coolpix p900": 1803,
        "lenovo zuk z2": 2182,
        "coocaa 32e6": 1804,
        "canon eos 800d": 1706,
        "asus zenfone live l1 za550kl 1": 1806,
        "mobiistar zumbo j2": 657,
        "sony dsc rx100 iii": 658,
        "asus zenfone 3 laser zc551kl": 659,
        "asus zenfone selfie zd551kl": 660,
        "xiaomi mi a2 lite": 1809,
        "infinix hot 4 pro": 661,
        "mamypoko x tra dry pants s 40": 1794,
        "asus zenfone 4 selfie pro zd552kl": 1810,
        "samsung galaxy j7 prime": 1811,
        "asus x455la": 662,
        "apple macbook pro mpxy2": 2192,
        "asus x455lb": 663,
        "htc desire 10 lifestyle": 664,
        "asus transformer 3 pro t303": 1812,
        "polytron pld43ts153": 665,
        "sony xperia c4": 1740,
        "asus rog gl502vt": 1814,
        "asus x455lj": 666,
        "panasonic th 24f305g": 2243,
        "acer aspire v3 471g": 1248,
        "apple macbook pro mptr2": 2011,
        "asus x441ba": 2241,
        "lenovo a2010": 668,
        "samsung 55mu6100": 669,
        "hp envy 13 ad002tu": 670,
        "asus zenbook ux310uq": 1816,
        "panasonic lumix dmc lx10": 1817,
        "polytron pld22d9500": 2005,
        "canon eos 77d": 671,
        "asus a407ma": 1818,
        "nokia 130 2017": 672,
        "acer predator triton 700": 1819,
        "philips 24pha4100s": 673,
        "hp 14 bs009tu": 2187,
        "strawberry shoju": 1821,
        "vivo v11i": 674,
        "xiaomi mi 5 4": 1823,
        "canon eos 70d": 1824,
        "asus e402wa": 465,
        "philips 43put6002s": 1825,
        "evercoss u60": 1826,
        "samsung galaxy grand prime": 676,
        "sweety comfort gold s 26": 1827,
        "sharp r1": 677,
        "apple watch edition 38mm 1st gen": 2248,
        "asus x540sa": 678,
        "xiaomi redmi note 4 mediatek": 1828,
        "lenovo thinkpad 25": 679,
        "samsung galaxy c5": 2188,
        "samsung galaxy tab a 9.7 s pen": 680,
        "samsung 55nu7300": 1829,
        "asus zenfone go zb552kl": 1830,
        "brandcode b188": 1831,
        "samsung qa65q7fna": 681,
        "fitti daypants m 28": 682,
        "toshiba tecra a50": 683,
        "acer spin 3": 1901,
        "asus zenfone ares": 1833,
        "pokana pants surprise design l 48": 684,
        "xiaomi mi 4": 1250,
        "asus rog g501vw": 1769,
        "coocaa 24w1900": 1835,
        "hp elitebook 820": 686,
        "nepia genki tape nb 44": 687,
        "xiaomi mi 5": 688,
        "apple macbook pro mlw82": 1836,
        "dell inspiron 7472": 469,
        "apple watch 1st gen": 1837,
        "apple ipad air lte": 690,
        "samsung 40j5200": 691,
        "polytron pld40t105": 692,
        "pokana pants super l 26": 693,
        "acer predator g9 793": 1839,
        "hp spectre 13 v142tu": 1840,
        "samsung 49ku6300": 694,
        "nokia 7 plus": 1841,
        "lenovo vibe p1 turbo": 1842,
        "drypers drypantz mini jumbo pack xxl 22": 470,
        "samsung ua40mu6100": 695,
        "sony kd 55x9000e": 1844,
        "samsung q7f": 696,
        "sony kd 55x9000f": 1845,
        "apple macbook pro mptu2": 1846,
        "lenovo yoga 720": 698,
        "brandcode b230": 1847,
        "apple iphone 6s plus": 1848,
        "lenovo v510": 1256,
        "asus a455ld": 472,
        "merries pants good skin m 50": 1849,
        "dell latitude 3379": 1850,
        "dell latitude 3470": 700,
        "apple watch nike series 3 gps": 701,
        "sony kdl 50w660f": 1851,
        "vivo y55s": 702,
        "apple ipad mini wi fi 64": 2164,
        "mito 3212": 703,
        "polytron pld32d715": 2124,
        "apple macbook pro mr972": 1853,
        "polysonic ps 2295": 1854,
        "mamypoko extra dry tape m 26": 2018,
        "mamypoko extra soft pants m 64": 1709,
        "sony a7 mark iii": 1635,
        "sharp lc 50ua440x": 1855,
        "sensi regular pants m 34": 1316,
        "mamypoko extra soft pants xxl 38": 138,
        "hp zbook 15": 1448,
        "goo.n slim pants l50": 1858,
        "toshiba 40l3750vj": 1564,
        "samsung 50mu6100": 2195,
        "samsung galaxy j2 prime": 708,
        "asus vivobook e12": 1450,
        "lg 65uk6100": 1861,
        "fitti daypants xxl 20": 709,
        "asus zenfone live zb501kl": 1862,
        "philips 32pha4100s": 1863,
        "panasonic lumix dc gh5": 1864,
        "sony xperia xz2 premium": 1525,
        "samsung galaxy j7": 710,
        "samsung galaxy j6": 711,
        "polytron pld32t1550": 712,
        "samsung galaxy j4": 713,
        "samsung galaxy j3": 714,
        "samsung galaxy j2": 715,
        "samsung galaxy j1": 716,
        "lg 32lk500": 717,
        "asus zenfone 4 selfie pro": 1638,
        "sensi regular pants l36": 1868,
        "apple watch sport": 1259,
        "samsung galaxy j8": 719,
        "asus zenfone 5z zs620kl 6": 720,
        "genki moko pants s9": 721,
        "samsung galaxy a9": 1870,
        "oppo a71 2018 3": 1871,
        "oneplus 5t": 722,
        "xiaomi mi 5s plus 6": 1873,
        "sony cybershot dsc w830": 723,
        "akari le 32v90": 724,
        "infinix hot s3": 725,
        "sweety bronze pants l 20+2": 726,
        "samsung ua49nu7100": 1386,
        "samsung galaxy a5": 1877,
        "lenovo legion y920": 1878,
        "apple ipad 9.7": 727,
        "coocaa 19e510": 728,
        "asus x441sa": 156,
        "nikon coolpix w300": 2193,
        "mito 2928": 1881,
        "lg 43lh511t": 1882,
        "hp spectre x360 13 ac049tu": 730,
        "dell latitude 3480": 706,
        "acer aspire 3 a314": 1884,
        "samsung galaxy j2 pro 2018": 1885,
        "asus zenwatch 2 wi501q": 732,
        "samsung galaxy s5": 1887,
        "hp envy 13 ad003tx": 733,
        "samsung galaxy s7": 1889,
        "sony 49w660": 1890,
        "samsung galaxy s9": 1891,
        "changhong l43g3": 1892,
        "acer aspire e1 432": 734,
        "changhong le 29c2000": 735,
        "goon smile baby night pants m34": 1894,
        "lenovo yoga 510": 1895,
        "apple ipad 4 wi fi cellular": 736,
        "lenovo thinkpad helix 2": 737,
        "mamamia pants m60": 739,
        "merries pants good skin s 26": 2119,
        "coocaa 50g2": 1630,
        "mamypoko x tra dry pants xxl 34": 741,
        "asus a555lb": 1990,
        "dell inspiron 3567": 742,
        "asus zenbook ux430uq": 743,
        "xiaomi redmi note 6 pro": 744,
        "canon ixus 107": 1898,
        "mito 3255": 1899,
        "asus zenfone max zc550kl": 1486,
        "asus zenfone max plus m1 zb570tl": 745,
        "asus x541uj": 746,
        "sony a7s ii": 14,
        "canon powershot sx420 is": 1747,
        "acer spin 5": 1902,
        "samsung 49q6fna": 1903,
        "apple watch 42mm 1st gen": 1880,
        "hp 14 bs007tu": 2190,
        "philips 32pha3052": 2141,
        "samsung galaxy tab a 7.0": 748,
        "dell inspiron 7588": 1906,
        "apple ipad mini 2 lte": 1263,
        "samsung qa55q8camkpxd": 1907,
        "sony xperia m4": 1791,
        "sony cybershot dsc w690": 750,
        "sensi regular pants l 30": 751,
        "sony cybershot dsc wx500": 1909,
        "samsung 43k5500": 752,
        "lg 55uh650t": 2076,
        "changhong 40e2000": 753,
        "sweety pantz gold l 54": 1455,
        "goo.n pants xl22": 754,
        "panasonic lumix dmc g85": 72,
        "apple ipad wi fi": 756,
        "xiaomi redmi note 5a prime": 2206,
        "hp omen 17 an002tx": 1913,
        "acer swift 3": 1914,
        "apple macbook pro mluq2": 1567,
        "apple iphone 6 plus": 757,
        "oppo r9s": 1915,
        "lg 49lj550t": 1268,
        "panasonic lumix dc gf9": 103,
        "lenovo k6": 759,
        "honor 5a": 1917,
        "vivo y71": 1948,
        "fitti tape rainbow l 42": 1918,
        "sony cybershot dsc rx10": 1919,
        "apple macbook mnyk2": 1912,
        "philips 32pht4002s": 488,
        "goo.n smile baby pants s22": 1920,
        "hp 14 bs742tu": 761,
        "xiaomi note 5a prime": 762,
        "apple macbook mnyl2": 131,
        "wiko robby": 764,
        "hp 14 bs743tu": 765,
        "wiko view prime": 1921,
        "samsung ua49j5250": 1922,
        "huawei mediapad t1 7.0": 1923,
        "asus rog zephyrus gm501gs": 150,
        "xiaomi redmi note 5a": 1925,
        "coocaa 43s3a12g": 1926,
        "asus fonepad 7": 1927,
        "polytron pld32d100": 1928,
        "samsung 55ku6000": 1834,
        "aqua le32aqt6000t": 1929,
        "coocaa 32w4": 1789,
        "philips 49pft6100s": 1930,
        "asus zenbook ux430un": 768,
        "hp pavilion x2": 769,
        "lg 75uk6500": 770,
        "mamamia pants xl18": 1932,
        "brandcode b79": 771,
        "mamypoko extra dry tape xl 34": 1933,
        "oppo a75s": 772,
        "apple watch edition series 2 42mm": 1934,
        "changhong 40e6000": 1935,
        "hp 245 g6": 773,
        "asus a456uf": 1489,
        "sensi dry m10": 1936,
        "changhong 40e6000hft": 1937,
        "lenovo ideapad 100": 774,
        "changhong 40e6000i": 2106,
        "samsung 40k5100": 319,
        "asus zenfone max m1 zb555kl": 1533,
        "dell inspiron 11 3162": 775,
        "polytron pld43s883": 1982,
        "wiko u feel prime": 776,
        "oppo a39": 1980,
        "hp 14 bs122tx": 1904,
        "asus a441uf": 1940,
        "asus zenfone 2 laser ze550kl": 777,
        "dell latitude 7490": 233,
        "asus zenfone 3 ze520kl": 778,
        "samsung ua49nu7300": 779,
        "itel p32": 780,
        "lenovo v110": 1942,
        "panasonic th 55f306g": 1943,
        "brandcode b17c": 1640,
        "panasonic lumix dmc gf9": 1944,
        "panasonic lumix dmc gf8": 1945,
        "toshiba satellite radius p25w": 1244,
        "advan i10": 1463,
        "evercoss u50a max": 1946,
        "panasonic lumix dmc fz300": 1947,
        "toshiba 24l2600vj": 738,
        "asus bu401lg": 1865,
        "strawberry st99": 782,
        "hp 14 an030au": 1950,
        "sensi dry l8": 1465,
        "sharp lc 40sa5100": 1952,
        "merries tape l 18": 1953,
        "coocaa 32a2a11a": 494,
        "sharp lc 32sa4101i": 784,
        "vivo v11": 1954,
        "leica cl": 785,
        "asus rog gl503ge": 1955,
        "samsung 49nu7100": 1956,
        "lg 75uj657t": 1957,
        "oppo a37": 1981,
        "asus zenbook ux303lb": 2030,
        "hp 14 bw515au": 786,
        "mito 1930": 787,
        "nikon d3400": 315,
        "oppo r11s plus": 789,
        "xiaomi mi tv 4a": 1960,
        "asus zenfone go zb452kg": 326,
        "asus fx503vd": 791,
        "ichiko s1798": 792,
        "dell inspiron 5370": 793,
        "sharp lc 65ue630x": 794,
        "canon eos 5d": 795,
        "dell inspiron 5378": 796,
        "dell inspiron 5379": 797,
        "mamypoko x tra dry pants s 58": 1964,
        "sweety bronze comfort nb s 44": 2031,
        "samsung ku6500": 798,
        "sharp lc 32le265": 799,
        "hp pavilion 15 cb505tx": 365,
        "panasonic th 43e306g": 1966,
        "samsung galaxy tab a 9.7": 370,
        "dell vostro 3468": 1967,
        "panasonic lumix dmc gx8": 1968,
        "xiaomi redmi": 376,
        "hp probook 430 g4": 803,
        "philips 43pfa3002": 1273,
        "samsung galaxy s9 6": 1970,
        "hp probook 430 g3": 804,
        "hp probook 430 g2": 386,
        "goon excellent dry tape l32": 1972,
        "nikon coolpix a": 389,
        "goon excellent dry tape m38": 807,
        "niko nkled2302": 808,
        "apple macbook pro mr9u2": 1974,
        "asus memo": 809,
        "asus zenfone 2 ze551ml": 810,
        "fitti gold pants m44": 1976,
        "sharp z2": 1646,
        "dell inspiron 5570": 811,
        "asus zenfone 3 deluxe zs550kl": 1515,
        "canon eos 4000d": 812,
        "samsung 48j6300": 813,
        "asus rog gl552jx": 1987,
        "akari le 20v89": 814,
        "toshiba c55": 432,
        "asus x555ya": 816,
        "pampers premium care pants l 24": 817,
        "apple watch nike gps+lte": 445,
        "panasonic th 55es630g": 1422,
        "apple watch 38mm 1st gen": 819,
        "oppo a3": 215,
        "mito 120i": 821,
        "vivo v7 plus": 1276,
        "coocaa 24d3a": 479,
        "sony kdl 40r350e": 1983,
        "sony kd 55x7500f": 823,
        "changhong 32e6000t": 502,
        "oppo a83 2018": 1761,
        "merries tape m 38": 1650,
        "asus x550vq": 1985,
        "lenovo thinkpad e480": 1843,
        "apple iphone xr": 826,
        "apple iphone xs": 827,
        "mamypoko soft sensation tape s 38": 828,
        "fujifilm x t100": 829,
        "fitti daypants l18": 1988,
        "drypers drypantz mini jumbo pack l 28": 1989,
        "samsung 32fh4003": 504,
        "philips e570": 831,
        "panasonic th 55e306": 1991,
        "oppo a83": 832,
        "akari le20k88": 1992,
        "polytron pld20d901": 833,
        "sweety silver pants m 38": 536,
        "apple watch edition 42mm 1st gen": 1994,
        "samsung gear s": 2221,
        "nokia 6.1": 1996,
        "philips 55put6002s": 834,
        "sweety silver pants m 30": 1997,
        "nokia 3310": 835,
        "asus zenfone go zb500kl": 836,
        "lg 55eg9a7t": 837,
        "fitti daypants m 56": 838,
        "panasonic lumix dmc lx100": 555,
        "sanken sle 241hdj": 1999,
        "polytron pld32d7511": 1394,
        "xiaomi redmi note 4x 4": 840,
        "mito 366": 2000,
        "huawei p20 lite": 841,
        "evercoss winner t max": 1279,
        "sony kdl 55w800c": 1652,
        "asus zenfone 3 max": 579,
        "sony cybershot dsc rx100 mark iv": 2001,
        "huawei porche design mate rs": 2204,
        "lenovo a5000": 2002,
        "mito 3255t": 2003,
        "changhong 32e6000a": 509,
        "lg 28mt49vf": 845,
        "hp elitebook 830": 846,
        "vivo y65": 847,
        "sweety silver pants xl 18+2": 1838,
        "meizu m5 note": 2004,
        "lg 49sk8500": 625,
        "sony xperia xa1": 849,
        "sony xperia xa2": 850,
        "vivo y69": 851,
        "vivo v5 plus": 852,
        "samsung ua49mu8000": 2131,
        "samsung ua49m5000": 853,
        "gigabyte aero 14": 854,
        "gigabyte aero 15": 649,
        "sony kd 49x7000f": 2007,
        "happy diapers xl 22": 856,
        "apple ipad mini wi fi": 2008,
        "happy diapers m 30": 857,
        "samsung j7 duo": 2010,
        "samsung galaxy note 7 4": 1657,
        "nikon d5600": 2012,
        "brandcode b329": 858,
        "vivo x21": 2013,
        "samsung galaxy tab s 10.5 lte": 2014,
        "sony xperia z3 compact": 859,
        "samsung galaxy j1 mini prime": 2015,
        "vivo y81": 860,
        "canon eos 1300d": 2017,
        "vivo y85": 861,
        "huawei p10 lite": 862,
        "sweety pants gold xl 44": 863,
        "sanken sle 501fdj": 1686,
        "oppo a3s": 1965,
        "smartfren andromax b": 2184,
        "sweety pants gold xxl 36": 864,
        "samsung galaxy a8 star": 2020,
        "sensi regular pants s 40": 865,
        "philips 24pha4110s": 866,
        "sweety comfort gold nb 52": 2021,
        "samsung galaxy a3 2017": 1675,
        "samsung 50js7200": 2059,
        "panasonic th 43ex600g": 867,
        "mamypoko soft sensation tape m24": 868,
        "toshiba 24l2800": 2022,
        "asus x550vx": 2023,
        "samsung galaxy s6 edge": 1660,
        "asus zenpad 3s 10": 869,
        "pampers premium care pants xxl 28": 2024,
        "apple macbook pro mpxv2": 2025,
        "xiaomi mi mix 6": 870,
        "changhong e6000i": 1473,
        "xiaomi mi mix 2": 871,
        "xiaomi mi mix 3": 872,
        "mamamia pants s20": 2026,
        "fujifilm x a3": 766,
        "dell xps 13": 2038,
        "acer nitro 5": 2229,
        "canon ixus 175": 2228,
        "hp spectre x360 13 ae076tu": 2028,
        "xiaomi note 5": 874,
        "oppo r11": 875,
        "coocaa 55e700a": 876,
        "oppo r17": 877,
        "oppo r15": 878,
        "strawberry warrior t1": 879,
        "akari le 40d881d": 880,
        "aqua le32aqt6500": 2231,
        "samsung galaxy a9 pro 2016": 881,
        "asus ux550vd": 2245,
        "apple ipad pro 10.5": 882,
        "mito 105": 2032,
        "asus zenpad 10 z301mfl": 884,
        "strawberry s47": 2034,
        "mamamia baby soft magic tape m40": 1694,
        "mamypoko soft sensation tape nb28": 886,
        "mamypoko soft sensation tape m36": 1775,
        "canon eos 200d": 887,
        "samsung galaxy a9 2016": 888,
        "samsung ua65mu6500k": 889,
        "canon powershot g3 x": 1910,
        "lg 50uk6300": 2035,
        "honor 6x": 2036,
        "dell latitude 3490": 2037,
        "nikon d7200": 1327,
        "panasonic th 49e305g": 1852,
        "lenovo thinkpad 13": 890,
        "samsung galaxy a9 2016 3": 891,
        "dell xps 15": 2039,
        "lg 43lk5400": 1546,
        "toshiba 47l2400vj": 892,
        "sweety bronze pants l 30+4": 893,
        "toshiba 32l1600": 2139,
        "sanken sle 323hdb": 894,
        "drypers drypantz mega pack xl 42": 896,
        "sweety pants gold xl 26": 2041,
        "honor 9 lite": 2042,
        "asus zenfone 4 selfie zd553kl": 897,
        "apple ipad mini 4 lte": 898,
        "msi gl63 8rc": 2043,
        "goon smile baby night pants l30": 931,
        "xiaomi mi 5c": 2045,
        "dell inspiron 3459": 2046,
        "msi pl60 7rd": 1637,
        "apple ipad air wifi": 2235,
        "panasonic lumix dmc tz80": 941,
        "dell inspiron 3452": 2048,
        "coocaa 32s3a12g": 899,
        "asus zenfone 4 max pro zc554kl": 900,
        "vivo v5s": 1289,
        "samsung galaxy c9 pro": 2050,
        "coocaa 58g2": 901,
        "asus a411uf": 902,
        "apple macbook pro mpxx2": 2052,
        "xiaomi redmi 5 3": 903,
        "fujifilm x t3": 904,
        "fujifilm x t2": 905,
        "samsung ua43nu7100": 106,
        "akari le 55d88s": 906,
        "sharp lc 65le275x": 907,
        "polytron pld43ts865": 2057,
        "sony kdl 40r350c": 1984,
        "xiaomi mi note": 908,
        "asus a407uf": 1669,
        "olympus om d e m5 mark ii": 208,
        "brandcode b4s": 909,
        "apple ipad mini 3 lte": 1664,
        "hp envy 13 ad181tx": 148,
        "sony dsc hx90v": 911,
        "samsung gear s2 classic": 1665,
        "apple macbook pro mr932": 1019,
        "sharp a2 lite": 912,
        "oppo neo 5 12": 913,
        "sharp lc 32sa4100i": 914,
        "aqua le32aqt1000": 915,
        "mamypoko x tra dry tape m40": 2060,
        "philips 40pfa4160": 916,
        "samsung ua58nu7103": 2062,
        "apple macbook pro mr942": 917,
        "fitti daypants l 24": 2063,
        "huawei mate 9": 918,
        "huawei mate 8": 919,
        "asus x441ua": 2064,
        "asus zenfone zoom zx551ml 4": 920,
        "mamypoko x tra dry pants xxl 24": 921,
        "apple macbook pro mpxq2": 922,
        "huawei honor 7a": 1788,
        "sony kd 49x7500f": 923,
        "sony kd 49x7500e": 924,
        "lenovo thinkpad x270": 1294,
        "asus vivobook pro n580vd": 926,
        "dell inspiron 3157": 2240,
        "sharp lc 60ua440x": 1579,
        "evercoss jump t3 r40d": 1266,
        "apple macbook mnym2": 928,
        "sony cybershot dsc wx50": 1857,
        "sony a5100": 2069,
        "acer aspire e1 472g": 929,
        "polysonic ps 1892": 930,
        "asus k401lb": 2070,
        "acer aspire es1 533": 1673,
        "polytron pld24d901": 2071,
        "hp 14 bs740tu": 2072,
        "polytron 40tv853": 2073,
        "mamypoko extra soft pants xl 46": 932,
        "philips 55put6002": 2075,
        "toshiba 24s1500": 1133,
        "sony xperia xz premium": 1138,
        "asus padfone mini": 1869,
        "acer aspire v3 371": 2078,
        "xiaomi mi mix 2 6": 1758,
        "samsung galaxy j1 2016": 1153,
        "niko nkled1702": 2080,
        "coocaa 50e2000t": 2081,
        "strawberry st6": 933,
        "sensi dry nb52": 934,
        "lenovo ideapad 110": 935,
        "acer aspire r11": 1668,
        "lg 49lk5100": 2083,
        "mamypoko extra dry tape l 62": 936,
        "asus gl752vl": 937,
        "pokana pants super xl 22": 1856,
        "olympus pen e pl9": 2085,
        "hp spectre x360 13 ac051tu": 938,
        "merries pants good skin xl 16": 939,
        "asus x540bp": 527,
        "hp probook 450 g2": 2176,
        "olympus pen e pl7": 2086,
        "asus transformer t101ha": 2087,
        "sweety bronze pants xxl 18+2": 1547,
        "asus zenpad 8 z380knl": 2088,
        "dell inspiron 14 3458": 2047,
        "asus zenfone 4 max": 2090,
        "dell latitude e5450": 942,
        "strawberry s338": 2091,
        "hp pavilion 14 af118au": 1908,
        "mobiistar lai zoro 3": 369,
        "mamypoko extra dry tape xl 50": 943,
        "akari le 43p88": 2093,
        "samsung galaxy j7 pro": 944,
        "hp 14 bs707tu": 1387,
        "polytron pld32v7510": 945,
        "alcatel 818d": 946,
        "samsung 55q7fn": 947,
        "lg 22tk420a": 2094,
        "sharp lc 40le265m": 705,
        "zenfone live l1": 1354,
        "motorola moto g5s plus": 2096,
        "toshiba 24l1600vj": 948,
        "dell latitude e7250": 2097,
        "nokia 216": 949,
        "akari le 24v89": 950,
        "mobiistar zumbo power": 2098,
        "toshiba satellite c55t": 2099,
        "lg 55lf550t": 1815,
        "lg 28tk430v": 951,
        "hp pavilion 14 g008au": 1270,
        "xiaomi redmi 5a": 1511,
        "sanken sle 242hdb": 952,
        "huawei honor 5c": 2104,
        "asus zenfone 4 max zc554kl": 953,
        "panasonic th 40ds500g": 954,
        "changhong g5i": 1762,
        "toshiba satellite c55d": 2105,
        "samsung ua32j4003dr": 2089,
        "motorola moto e5 plus": 883,
        "vivo y53c": 1670,
        "goon excellent dry tape nb48": 956,
        "lenovo a7000": 957,
        "xiaomi mi 5s": 2051,
        "huawei honor 9": 958,
        "oppo r9s black edition": 1318,
        "canon powershot sx400 is": 1299,
        "mobiistar lai zumbo s lite 2017": 960,
        "dell latitude e5570": 961,
        "sharp a click": 2108,
        "sony a7s": 962,
        "sony a7r": 963,
        "nikon d5500": 2110,
        "evercoss jump t2 r40g": 964,
        "polytron pld32s1503": 1300,
        "merries pants good skin l 30": 966,
        "xiaomi redmi note": 967,
        "itel p51": 2112,
        "samsung galaxy s7 edge": 2113,
        "goo.n smile baby pants m20": 2114,
        "changhong 20e2000": 969,
        "dell latitude 7380": 2225,
        "goo.n slim pants xl44": 970,
        "huawei y9 2018 4": 1672,
        "xiaomi mi 5s 4": 1361,
        "samsung 49j5250": 2115,
        "hp 14 bs719tu": 2116,
        "drypers drypantz convenient pack xxl 12": 973,
        "xiaomi redmi 2": 974,
        "xiaomi redmi 3": 975,
        "xiaomi redmi 1": 976,
        "xiaomi redmi 6": 977,
        "samsung galaxy j5": 2120,
        "xiaomi redmi 5": 978,
        "merries tape s 24": 979,
        "nikon coolpix a300": 980,
        "toshiba 24l2800vj": 981,
        "dell inspiron 5567": 982,
        "nikon coolpix s33": 983,
        "nikon d3300": 984,
        "canon eos 3000d": 1627,
        "asus x550iu": 1414,
        "dell latitude e5470": 895,
        "asus rog gl752vw": 985,
        "mito 4231": 2054,
        "huawei y3ii 1": 2125,
        "nepia genki tape m 64": 2126,
        "htc u11 eyes": 2127,
        "polysonic a858i": 986,
        "meizu m6": 2129,
        "panasonic th 32e306g": 987,
        "sony dsc rx100 vi": 2055,
        "msi ge62 6qd apache pro": 2130,
        "advan g1 pro": 988,
        "oppo f3": 989,
        "asus zenfone max m1": 1866,
        "oppo f1": 990,
        "baby happy tape l20": 2056,
        "oppo f7": 991,
        "toshiba 32l3750vj": 992,
        "oppo f5": 993,
        "lg 55sj800t": 2132,
        "lenovo thinkpad x1 yoga": 994,
        "oppo f9": 995,
        "changhong 32e2000": 731,
        "toshiba satellite radius p55w": 2133,
        "apple ipad 2017 wifi": 996,
        "asus vivobook flip tp301uj": 997,
        "asus x450ld": 2134,
        "aqua 32aqt": 2135,
        "lenovo thinkpad t450": 2136,
        "toshiba 43l3750": 2058,
        "merries pants good skin m 34": 998,
        "samsung galaxy tab a 10.1": 999,
        "mamypoko extra dry pants s 38": 2137,
        "asus zenbook ux360ca": 1000,
        "dell inspiron 7567": 2213,
        "sharp lc 60ua6800x": 1001,
        "akari le 29v89": 1002,
        "lenovo thinkpad e470": 2138,
        "xiaomi redmi 5 plus": 1003,
        "hp omen 17 an068tx": 1306,
        "asus zenfone 3 laser": 1245,
        "asus zenfone 5q": 2140,
        "evercoss m50a": 1291,
        "aqua le24aqt6550t": 1005,
        "panasonic th 49d305g": 1006,
        "alcatel 2051d": 1007,
        "asus zenbook ux330": 2142,
        "pokana pants surprise design l 20": 1008,
        "philips 43pft6100s": 1009,
        "lg 20mt48af": 2143,
        "brandcode b3 neo": 910,
        "canon eos m": 1010,
        "asus x441uv": 2066,
        "evercoss winner x3": 1011,
        "sony kd 55x8500f": 1872,
        "asus rog g752vs": 1012,
        "canon ixus 255 hs": 2147,
        "huawei nova 3i 6": 2148,
        "akari le 25v89": 1013,
        "samsung 49m5100": 162,
        "samsung 40j5250": 2163,
        "apple ipad air": 2149,
        "oppo r9 plus": 2150,
        "sony xperia xa2 ultra": 1725,
        "samsung galaxy tab 4 7.0": 1015,
        "nokia 6 2018": 1016,
        "samsung galaxy a3": 1874,
        "sony cybershot dsc hx350": 2152,
        "xiaomi redmi y2": 1017,
        "lg 43uk6300": 1018,
        "canon powershot g9 x": 1979,
        "hp spectre x360 13 ac050tu": 1625,
        "asus zenfone max m2": 1867,
        "mito 188": 1020,
        "apple ipad pro 2017 12.9": 2155,
        "samsung galaxy a6": 1875,
        "canon eos 1500d": 1021,
        "sharp lc 50le275x": 1647,
        "hp 14 bs005tu": 2157,
        "samsung galaxy a7": 1876,
        "sweety comfort gold nb 30": 1022,
        "asus x454yi": 1023,
        "apple watch herm series 2": 540,
        "htc u ultra": 2242,
        "asus zenfone 4 max plus": 1025,
        "oppo r15 pro 6": 1026,
        "asus x454ya": 1027,
        "huawei nova": 1028,
        "sweety pants gold xxl 22": 1029,
        "evercoss winner t selfie r40h": 1679,
        "asus vivobook flip tp203nah": 1030,
        "philips 32pha3052s": 1684,
        "hp elitebook folio 9470": 2153,
        "asus zenfone go zc500tg": 1032,
        "xiaomi mi 4i": 1691,
        "asus zenfone 5 lite 5q zc600kl 4": 1033,
        "asus zenfone 5 lite 5q zc600kl 3": 1034,
        "acer aspire e5 476": 1035,
        "lg 50uk6540": 1036,
        "aqua le32aqt6900": 1037,
        "asus zenfone 4 max pro": 1038,
        "acer aspire e5 473": 1039,
        "lg 24tk425a": 1040,
        "samsung 49m6300": 1879,
        "canon powershot g1x": 1683,
        "acer aspire e5 573": 2166,
        "toshiba 40l2400": 2167,
        "panasonic th 49f305g": 2168,
        "asus zenfone 4 selfie lite zb520kl": 729,
        "panasonic lumix dmc gh4": 2169,
        "canon ixus 190": 2170,
        "xiaomi mi a2 6x 4": 2171,
        "panasonic th l32x30g": 1577,
        "lg q7": 2262,
        "asus x550ik": 2117,
        "asus zenfone max pro m2": 2173,
        "panasonic th 32c305g": 1042,
        "huawei nova 2 plus 4": 2174,
        "hp probook 450 g5": 2175,
        "sweety silver pants l 54": 1043,
        "hp pavilion x360": 1044,
        "nikon d750": 1045,
        "hp 14 bs015tu": 2179,
        "lg 43lj500t": 1046,
        "sony cybershot dsc w810": 1047,
        "smartfren andromax l": 2181,
        "asus zenfone pegasus": 1269,
        "apple watch edition series 2": 1048,
        "apple watch edition series 3": 1049,
        "sony dsc h300": 1050,
        "asus rog gl553vd": 1051,
        "asus rog gl553ve": 1052,
        "samsung ua40m5050": 1053,
        "asus x441ub": 2065,
        "lenovo p2": 885,
        "asus rog gl502vs": 1054,
        "asus x454wa": 1055,
        "asus zenfone max plus m1": 1820,
        "asus rog gl502vm": 1056,
        "asus zenfone 5 ze620kl 4": 1057,
        "acer aspire 3 a315": 740,
        "asus zenfone 5 ze620kl 6": 1058,
        "brandcode b29": 2264,
        "canon eos m3": 1059,
        "lg 43lj500": 1060,
        "canon eos m5": 1061,
        "canon eos m6": 1599,
        "genki moko pants l17": 2040,
        "asus zenfone go zb551kl": 1063,
        "mamypoko extra dry tape s 80": 1064,
        "samsung ua32fh4003r": 1886,
        "sanken sle 401fdj": 1065,
        "happy nappy smart pantz s40": 1631,
        "huawei mate 10": 2196,
        "mamypoko x tra dry pants m 50": 2197,
        "panasonic th 32f302g": 2198,
        "hp 14 ac123tx": 1066,
        "sony kd 43x7000e": 1067,
        "acer aspire e1 410": 1068,
        "sanken sle 40": 2200,
        "nokia 3.1 plus": 2201,
        "pokana pants super m 32": 2202,
        "acer aspire e5 553g": 2203,
        "panasonic th 43f305g": 1069,
        "asus vivobook flip tp410ua": 1070,
        "sweety bronze comfort nb s24": 1071,
        "motorola moto e3 power": 2219,
        "xiaomi mi max 4": 1072,
        "xiaomi mi max 2": 1073,
        "xiaomi mi max 3": 1074,
        "panasonic th 22d305g": 1075,
        "meizu m5c": 2100,
        "apple macbook air mmgg2": 1076,
        "happy nappy smart pantz l30": 2209,
        "sony ericsson aspen m1i": 1077,
        "huawei honor 7s": 1661,
        "samsung galaxy s8": 2211,
        "evercoss jump t4 a74j": 1938,
        "samsung ua65nu7100": 1695,
        "hp elitebook x360": 1078,
        "goon smile baby night pants l20": 2214,
        "apple ipad 2 wi fi 3g": 1079,
        "asus tuf fx504ge": 2215,
        "asus tuf fx504gd": 2216,
        "motorola moto e5": 1080,
        "motorola moto e4": 1081,
        "olympus om d e m10 mark iii": 1082,
        "xiaomi mi 4 lte 3": 1083,
        "hp pavilion 15 bc045tx": 1764,
        "sharp lc 32sa4200i": 1084,
        "changhong l39g3a": 1085,
        "huawei mediapad t2": 2272,
        "canon eos 600d": 1086,
        "mamypoko soft sensation tape nb 40": 2068,
        "dell latitude 7389": 1995,
        "samsung galaxy j2 pro 2016": 1893,
        "huawei p20": 1087,
        "changhong g3": 2223,
        "panasonic th 43ex400": 1088,
        "msi gl62m 7rdx": 1089,
        "honor 9": 12,
        "msi workstation we63": 2208,
        "akari le 25b88": 2226,
        "acer switch 5": 1505,
        "oppo neo 7": 1090,
        "asus zenbook pro 15": 1091,
        "oppo neo 5": 1092,
        "dell latitude e3350": 1093,
        "canon powershot sx730 hs": 2230,
        "htc one x10": 1094,
        "huawei y3 2018": 1095,
        "genki moko pants l7": 2233,
        "asus x541na": 2234,
        "sony kdl 40w650d": 1096,
        "pampers premium care pants s 32": 1097,
        "xiaomi redmi 6a 2": 1098,
        "xiaomi redmi 6a 3": 1099,
        "hp 14 ac004tx": 2237,
        "coocaa 32e2a22g": 1100,
        "evercoss m50 max": 1101,
        "evercoss m50": 2238,
        "mamypoko extra soft pants xxl 20": 2239,
        "nokia 8110": 1721,
        "meizu m5s": 2191,
        "samsung gear s3 frontier": 1102,
        "sharp lc 40le295i": 1688,
        "samsung ua43mu6100": 1104,
        "genki moko pants s22": 1105,
        "asus zenfone zoom": 1106,
        "drypers drypantz mini jumbo pack xl 24": 1107,
        "samsung galaxy folder": 1108,
        "samsung 40mu6100": 2053,
        "nokia 3310 2017": 1109,
        "mito a120": 781,
        "pampers premium care pants m 68": 1110,
        "lenovo k6 2": 2244,
        "sweety bronze pants m 20+2": 1111,
        "sensi dry l34": 1112,
        "samsung b350e": 2246,
        "akari le 50d88": 1499,
        "asus e202sa": 1113,
        "samsung galaxy j7 plus": 2249,
        "toshiba 32p1400": 1225,
        "dell inspiron 14 7447": 1114,
        "panasonic th 55fx400g": 2251,
        "xiaomi redmi 6 3": 2252,
        "acer chromebook 11": 1115,
        "lg v35 thinq": 1116,
        "samsung galaxy j3 pro": 2253,
        "samsung 43nu7090": 1117,
        "dell inspiron 7559": 1118,
        "pokana pants surprise design xxl 18": 2255,
        "mito 322": 1355,
        "asus pro p2430ua": 1119,
        "asus zenfone 5z": 1120,
        "polytron pld40ts153": 1121,
        "sony kd 43x7500f": 1122,
        "samsung qa55q7famkpxd": 2144,
        "evercoss winner y star": 2256,
        "hp 14 ac001tx": 2257,
        "sharp lc 24le175i": 2258,
        "nikon coolpix l820": 1123,
        "lenovo ideapad 100s": 2259,
        "apple macbook pro mjlq2": 1124,
        "goo.n slim pants m62": 707,
        "huawei mediapad m3": 1126,
        "apple watch edition series 3 gps+lte": 2263,
        "fitti tape rainbow m 48": 1127,
        "samsung galaxy tab s3 9.7": 1128,
        "samsung 40m5050": 2074,
        "sharp lc 32sa4500i": 1129,
        "htc u12": 1130,
        "toshiba 24l1600": 1896,
        "xiaomi mi 5s plus": 2267,
        "htc u11": 1131,
        "ichiko s3258": 2268,
        "toshiba 49l3750": 1132,
        "samsung 49m5000": 2269,
        "nepia genki tape xl 44": 2270,
        "polytron pld22d900": 2019,
        "polytron pld32d905": 1171,
        "huawei mediapad t3": 2273,
        "mito 1911": 1135,
        "coocaa 50s3a12g": 1136,
        "merries tape l 32": 2274,
        "samsung gear fit2 pro": 2275,
        "huawei y7 2": 1571,
        "lenovo thinkpad x260": 1137,
        "panasonic lumix dmc tz90": 1897,
        "panasonic th 32d302g": 1513,
        "samsung ua49j5200": 1139,
        "polytron pld24t810": 2277,
        "polytron pld24t811": 2278,
        "panasonic th 22e302g": 396,
        "apple ipad mini 2 wifi": 1949,
        "pampers premium care pants xl 36": 1141,
        "olympus om d e m10 mark ii": 2067
}

def get_jaccard_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

brandDic = {"google": 0, "htc": 1, "apple": 2, "wiko": 3, "polytron": 4, "huawei": 21, "gionee": 5, "leagoo": 6, "brandcode": 7, "luna": 8, "sharp": 10, "acer": 9, "blackview": 11, "prince": 12, "lg": 13, "spc": 14, "coolpad": 15, "smartfren": 16, "infinix": 17, "blaupunkt": 18, "lava": 19, "aldo": 20, "icherry": 32, "advan": 22, "leeco": 23, "nexcom": 24, "zyrex": 25, "axioo": 26, "elephone": 27, "himax": 28, "hp": 29, "nokia": 30, "nuu mobile": 31, "xiaomi": 33, "pixcom": 34, "mito": 35, "huang mi": 36, "maxtron": 37, "sony": 38, "indosat": 39, "philips": 40, "lenovo": 41, "alcatel": 42, "samsung": 43, "zyo": 44, "doogee": 45, "vivo": 46, "evercoss": 47, "strawberry": 48, "ifone": 49, "fujitsu": 50, "blackberry": 51, "asus": 52, "oneplus": 53, "honor": 54, "oppo": 55}
for index, row in data.iterrows():
    similarity = []
    counter = 0
    brand = data.loc[index,"Brand"]
    if (not math.isnan(brand)):
        brandName = list(brandDic.keys())[list(brandDic.values()).index(brand)]
        for key in modelDic.keys():
            start = key.split()[0]
            if start == brandName:
                title = data.loc[index,"title"].split()
                sim = []
                for i in range(len(title)):
                    titlesubstring = ' '.join(title[i:])
                    sim.append(get_jaccard_sim(titlesubstring,key))
                similarity.append(max(sim))
            else:
                similarity.append(-1)
        indexNum = similarity.index(max(similarity))
        temp = list(modelDic.values())
        modelNum = temp[indexNum]
        print(modelNum)
        data.loc[index,"Phone Model"] = modelNum
    else:
        break

save_new_dataset(data, "mobile_data_stage_3.csv")


################################################################################
#
# Stage 4: Fill in color
#
################################################################################
def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
    image = image.reshape(image.shape[0]*image.shape[1], 3)
    return image

def get_colors(image):
    clf = KMeans(n_clusters = 1)
    labels = clf.fit_predict(image)
    counts = Counter(labels)
    #
    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i]/255 for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]*255) for i in counts.keys()]
    rgb_colors = [ordered_colors[i]*255 for i in counts.keys()]
    return rgb_colors

def get_color_name(rgb_array):
    # if within certain range, return a number
    red = rgb_array[0]
    green = rgb_array[1]
    blue = rgb_array[2]
    # yellow
    if  230 <= red <= 255 and 230 <= green <= 255 and 0 <= blue <= 30 :
        return 1
    # pink
    if  240 <= red <= 255 and 0 <= green <= 160 and 140 <= blue <= 220 and blue - green > 70:
        return 2
    # light blue
    if  0 <= red <= 135 and 150 <= green <= 220 and 230 <= blue <= 255 and green - red > 50:
        return 3
    # blue
    if  0 <= red <= 40 and 0 <= green <= 40 and 200 <= blue <= 255:
        return 4
    # deep blue
    if  0 <= red <= 15 and 0 <= green <= 15 and 140 <= blue <= 170:
        return 5
    # purple
    if  120 <= red <= 255 and 0 <= green <= 50 and 120 <= blue <= 255 and abs(red - blue) <= 20 and red + blue - 2 * green > 180:
        return 6
    # rose
    if 170 <= red <= 185 and 60 <= green <= 75 and 100 <= blue <= 115:
        return 7
    # black
    if  0 <= red <= 20 and 0 <= green <= 20 and 0 <= blue <= 20:
        return 10
    # orange
    if  230 <= red <= 255 and 50 <= green <= 170 and 0 <= blue <= 10:
        return 11
    # white
    if  240 <= red <= 255 and 240 <= green <= 255 and 240 <= blue <= 255:
        return 12
    # red
    if  230 <= red <= 255 and 0 <= green <= 30 and 0 <= blue <= 30:
        return 13
    # brown
    if  135 <= red <= 160 and 60 <= green <= 75 and 10 <= blue <= 25:
        return 14
    # navy blue
    if  0 <= red <= 15 and 0 <= green <= 15 and 110 <= blue <= 140:
        return 15
    if  180 <= red <= 195 and 140 <= green <= 150 and 140 <= blue <= 150:
        return 17
    # dark grey
    if  80 <= red <= 120 and 80 <= green <= 120 and 80 <= blue <= 120 and abs(red - green) < 10 and abs(red - blue) < 10 and abs(blue - green) < 10:
        return 18
    # silver
    if  180 <= red <= 210 and 180 <= green <= 210 and 180 <= blue <= 210 and abs(red - green) < 10 and abs(red - blue) < 10 and abs(blue - green) < 10:
        return 19
    # grey
    if  120 <= red <= 150 and 120 <= green <= 150 and 120 <= blue <= 150 and abs(red - green) < 10 and abs(red - blue) < 10 and abs(blue - green) < 10:
        return 20
    # army green
    if  0 <= red <= 10 and 90 <= green <= 120 and 0 <= blue <= 10:
        return 21
    # light grey
    if  150 <= red <= 180 and 150 <= green <= 180 and 150 <= blue <= 180 and abs(red - green) < 10 and abs(red - blue) < 10 and abs(blue - green) < 10:
        return 22
    # apricot
    if  200 <= red <= 215 and 100 <= green <= 110 and 25 <= blue <= 35:
        return 23
    # green
    if  0 <= red <= 30 and 200 <= green <= 255 and 0 <= blue <= 30:
        return 25
    return 10

for index, row in data.iterrows():
    image = data.loc[index,"image_path"]
    color = data.loc[index,"Color Family"]
    if(math.isnan(color)):
        data.loc[index,"Color Family"] = get_color_name(get_colors(get_image(image)))

save_new_dataset(data, "mobile_data_stage_4.csv")


################################################################################
#
# Data Cleaning, Seperating and Training
#
################################################################################
data = pd.read_csv("mobile_data_stage_4.csv")

#This function seprates the dataset into the column specified + title column
def seperate_col(col_name, upper_limit=10000):
    col = ['title', col_name]
    new_data = data[col]
    new_data = new_data[pd.notnull(new_data[col_name]) & (new_data[col_name] <= upper_limit)]
    new_data.columns = ['title', col_name]
    return new_data

#Thus function shows the counts of each label in a count plot
def show_counts(dataset, col_name):
    fig = plt.figure(figsize=(8,6))
    dataset.groupby(col_name).title.count().plot.bar(ylim=0)
    plt.show()
    print(dataset.shape)

#This function shows the most correlated words for each class of the label
def get_correlated_words(dataset, label_name, label_dict):
    #Initialising the vectorizer
    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=0.2, norm='l2', encoding='latin-1',
                        ngram_range=(1, 2), stop_words='english')
    #
    features = tfidf.fit_transform(dataset.title).toarray()
    labels = dataset[label_name]
    #
    N = 2
    #This can be used to see the most common words for each label
    for title, label in sorted(label_dict.items()):
      features_chi2 = chi2(features, labels == label)
      indices = np.argsort(features_chi2[0])
      feature_names = np.array(tfidf.get_feature_names())[indices]
      unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
      bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
      print("# '{}':".format(title))
      print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
      print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))

#This function trains the model on Naive Bayes, Linear SVC, RBF SVC, Logistic Regression and Random Forest
def train_model(dataset, label_name, label_dict):
    X_train, X_test, y_train, y_test = train_test_split(dataset['title'], dataset[label_name], random_state = 0)
    #
    #Naive Bayes
    NB_Predictor = Pipeline([('nb_vect', CountVectorizer()),
                      ('nb_tfidf', TfidfTransformer()),
                      ('nb_clf', MultinomialNB()),
                        ])
    NB_Predictor = NB_Predictor.fit(X_train, y_train)
    NB_Values = NB_Predictor.predict(X_test)
    NB_Score = accuracy_score(NB_Values, y_test)
    #
    #Linear SVC
    Lin_Predictor = Pipeline([('lin_vect', CountVectorizer()),
                      ('lin_tfidf', TfidfTransformer()),
                      ('lin_clf', SVC(random_state=0, tol=1e-5, kernel='linear', probability=True)),
                        ])
    Lin_Predictor = Lin_Predictor.fit(X_train, y_train)
    Lin_Values = Lin_Predictor.predict(X_test)
    Lin_Score = accuracy_score(Lin_Values, y_test)
    #
    #RBF SVC
    Rbf_Predictor = Pipeline([('Rbf_vect', CountVectorizer()),
                      ('Rbf_tfidf', TfidfTransformer()),
                      ('Rbf_clf', SVC(gamma='auto', kernel='rbf', probability=True)),
                        ])
    Rbf_Predictor = Rbf_Predictor.fit(X_train, y_train)
    Rbf_Values = Rbf_Predictor.predict(X_test)
    Rbf_Score = accuracy_score(Rbf_Values, y_test)
    #
    #Random Forest Classifier
    RFC_Predictor = Pipeline([('rfc_vect', CountVectorizer()),
                      ('rfc_tfidf', TfidfTransformer()),
                      ('rfc_clf', RandomForestClassifier(n_estimators=100, max_depth=3, random_state=0)),
                        ])
    RFC_Predictor = RFC_Predictor.fit(X_train, y_train)
    RFC_Values = RFC_Predictor.predict(X_test)
    RFC_Score = accuracy_score(RFC_Values, y_test)
    #
    #Logistic Regression
    LR_Predictor = Pipeline([('lr_vect', CountVectorizer()),
                      ('lr_tfidf', TfidfTransformer()),
                      ('lr_clf', LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial')),
                        ])
    LR_Predictor.fit(X_train, y_train)
    LR_Values = LR_Predictor.predict(X_test)
    LR_Score = accuracy_score(LR_Values, y_test)
    #
    print("Naive Bayes:", NB_Score)
    print("Linear SVC:", Lin_Score)
    print("Random Forest Classifier:", RFC_Score)
    print("Logistic Regression:", LR_Score)
    print("RBF SVC Regression:", Rbf_Score)
    #
    #Comparing the models and saving the one with the best accuracy
    to_use = max(NB_Score, Lin_Score, RFC_Score, LR_Score, Rbf_Score)
    #
    file_name = "models/" + label_name + "_model"
    #
    with open(file_name, "wb") as f:
        if(to_use == NB_Score):
            pickle.dump(NB_Predictor, f)
            print("Using Naive Bayes")
        elif(to_use == Lin_Score):
            pickle.dump(Lin_Predictor, f)
            print("Using Linear SVC")
        elif(to_use==RFC_Score):
            pickle.dump(RFC_Predictor, f)
            print("Using Random Forest Classifier")
        elif(to_use==Rbf_Score):
            pickle.dump(Rbf_Predictor, f)
            print("Using RBF SVC")
        else:
            pickle.dump(LR_Predictor, f)
            print("Using Logistic Regression")

#This checks the accuracy of the model on a test subset
def check_accuracy(model, dataset, label_name):
    X_train, X_test, y_train, y_test = train_test_split(dataset['title'], dataset[label_name], random_state = 1)
    model.fit(X_train, y_train)
    model_Values = model.predict(X_test)
    model_Score = accuracy_score(model_Values, y_test)
    return model_Score

#This gets the top n predictions for the given value(descending order)
def get_n_predictions(model, n, value):
    #
    inputValue = model.named_steps['lin_vect'].transform([value])
    #
    probs = model.named_steps['lin_clf'].predict_proba(inputValue)
    best_n = np.argsort(probs, axis=1)[:, -n:]
    best_n = np.flip(best_n)
    return best_n

### Labels
OS_label= {"symbian": 2,
        "windows": 3,
        "samsung os": 4,
        "blackberry os": 5,
        "nokia os": 0,
        "android": 6,
        "ios": 1
    }
Feature_label = {"expandable memory": 3,
        "touchscreen": 0,
        "fingerprint sensor": 4,
        "dustproof": 6,
        "waterproof": 1,
        "wifi": 2,
        "gps": 5
    }
Network_label = {
        "4g": 0,
        "2g": 1,
        "3g": 2,
        "3.5g": 3
    }
RAM_label = {
        "4gb": 5,
        "2gb": 6,
        "1.5gb": 0,
        "16gb": 9,
        "512mb": 1,
        "8gb": 3,
        "3gb": 7,
        "10gb": 2,
        "1gb": 8,
        "6gb": 4
    }
Brand_label = {
        "google": 0,
        "htc": 1,
        "apple": 2,
        "wiko": 3,
        "polytron": 4,
        "huawei": 21,
        "gionee": 5,
        "leagoo": 6,
        "brandcode": 7,
        "luna": 8,
        "sharp": 10,
        "acer": 9,
        "blackview": 11,
        "prince": 12,
        "lg": 13,
        "spc": 14,
        "coolpad": 15,
        "smartfren": 16,
        "infinix": 17,
        "blaupunkt": 18,
        "lava": 19,
        "aldo": 20,
        "icherry": 32,
        "advan": 22,
        "leeco": 23,
        "nexcom": 24,
        "zyrex": 25,
        "axioo": 26,
        "elephone": 27,
        "himax": 28,
        "hp": 29,
        "nokia": 30,
        "nuu mobile": 31,
        "xiaomi": 33,
        "pixcom": 34,
        "mito": 35,
        "huang mi": 36,
        "maxtron": 37,
        "sony": 38,
        "indosat": 39,
        "philips": 40,
        "lenovo": 41,
        "alcatel": 42,
        "samsung": 43,
        "zyo": 44,
        "doogee": 45,
        "vivo": 46,
        "evercoss": 47,
        "strawberry": 48,
        "ifone": 49,
        "fujitsu": 50,
        "blackberry": 51,
        "asus": 52,
        "oneplus": 53,
        "honor": 54,
        "oppo": 55
    }
Warranty_label = {
        "7 months": 0,
        "4 months": 1,
        "6 months": 10,
        "3 months": 3,
        "10 years": 4,
        "2 month": 5,
        "11 months": 6,
        "10 months": 7,
        "5 months": 8,
        "3 years": 9,
        "2 years": 2,
        "1 month": 11,
        "18 months": 12,
        "1 year": 13
    }
Storage_label = {
        "256gb": 16,
        "1.5gb": 0,
        "128gb": 1,
        "512mb": 2,
        "64gb": 3,
        "512gb": 4,
        "8gb": 5,
        "4mb": 10,
        "6gb": 7,
        "4gb": 9,
        "2gb": 6,
        "128mb": 11,
        "32gb": 12,
        "256mb": 13,
        "10gb": 14,
        "3gb": 15,
        "1gb": 8,
        "16gb": 17
    }
Color = {
        "blue": 4,
        "gold": 0,
        "brown": 14,
        "navy blue": 15,
        "yellow": 1,
        "neutral": 16,
        "rose gold": 17,
        "light blue": 3,
        "dark grey": 18,
        "silver": 19,
        "pink": 2,
        "gray": 20,
        "army green": 21,
        "deep blue": 5,
        "purple": 6,
        "rose": 7,
        "light grey": 22,
        "deep black": 8,
        "off white": 9,
        "multicolor": 24,
        "black": 10,
        "apricot": 23,
        "orange": 11,
        "green": 25,
        "white": 12,
        "red": 13
    }
Camera_label = {
        "42mp": 0,
        "dua slot": 1,
        "5 mp": 2,
        "3 mp": 3,
        "1 mp": 4,
        "8 mp": 5,
        "single camera": 6,
        "24 mp": 7,
        "16mp": 8,
        "13mp": 9,
        "6 mp": 10,
        "10mp": 11,
        "2 mp": 12,
        "20 mp": 13,
        "4 mp": 14
    }
Size_label = {
        "4.6 to 5 inches": 0,
        "4.1 to 4.5 inches": 3,
        "less than 3.5 inches": 4,
        "3.6 to 4 inches": 1,
        "more than 5.6 inches": 2,
        "5.1 to 5.5 inches": 5
    }


###### Seprating Operating System
os = seperate_col("Operating System", 7)
show_counts(os, "Operating System")
os.head()
train_model(os, "Operating System", OS_label)

###### Seprating Features
feature = seperate_col("Features", 7)
show_counts(feature, "Features")
feature.head()
train_model(feature, "Features", Feature_label)

###### Seprating Network Connections
network = seperate_col("Network Connections", 7)
show_counts(network, "Network Connections")
network.head()
train_model(network, "Network Connections", Network_label)

###### Seprating Memory RAM
ram = seperate_col("Memory RAM", 7)
show_counts(ram, "Memory RAM")
ram.head()
train_model(ram, "Memory RAM", RAM_label)

###### Seprating Brand
brand = seperate_col("Brand", 60)
show_counts(brand, "Brand")
brand.head()
train_model(brand, "Brand", Brand_label)

###### Seprating Warranty Period
warranty = seperate_col("Warranty Period", 14)
show_counts(warranty, "Warranty Period")
warranty.head()
train_model(warranty, "Warranty Period", Warranty_label)

###### Seprating Storage Capacity
storage = seperate_col("Storage Capacity", 18)
show_counts(storage, "Storage Capacity")
storage.head()
train_model(storage, "Storage Capacity", Storage_label)

###### Seprating Color Family
color = seperate_col("Color Family", 26)
show_counts(color, "Color Family")
color.head()
train_model(color, "Color Family", Color_label)

###### Seprating Phone Model
model = seperate_col("Phone Model", 2300)
show_counts(model, "Phone Model")
model.head()
train_model(model, "Phone Model", modelDic)

###### Seprating Camera
camera = seperate_col("Camera", 15)
show_counts(camera, "Camera")
camera.head()
train_model(camera, "Camera", Camera_label)

###### Seprating Phone Screen Size
size = seperate_col("Phone Screen Size", 6)
show_counts(size, "Phone Screen Size")
size.head()
train_model(size, "Phone Screen Size", Size_label)



################################################################################
#
# Evaluation
#
################################################################################

with open("models/Operating System_model", "rb") as f:
    Operating_System_model = pickle.load(f)
os_accuracy = check_accuracy(Operating_System_model, os, "Operating System")
print(os_accuracy)

with open("models/Features_model", "rb") as f:
    Features_model = pickle.load(f)
feature_accuracy = check_accuracy(Features_model, feature, "Features")
print(feature_accuracy)

with open("models/Network Connections_model", "rb") as f:
    Network_Connections_model = pickle.load(f)
network_accuracy = check_accuracy(Network_Connections_model, network, "Network Connections")
print(network_accuracy)

with open("models/Memory RAM_model", "rb") as f:
    Memory_RAM_model = pickle.load(f)
ram_accuracy = check_accuracy(Memory_RAM_model, ram, "Memory RAM")
print(ram_accuracy)

with open("models/Brand_model", "rb") as f:
    Brand_model = pickle.load(f)
brand_accuracy = check_accuracy(Brand_model, brand, "Brand")
print(brand_accuracy)

with open("models/Warranty Period_model", "rb") as f:
    Warranty_Period_model = pickle.load(f)
warranty_accuracy = check_accuracy(Warranty_Period_model, warranty, "Warranty Period")
print(warranty_accuracy)

with open("models/Storage Capacity_model", "rb") as f:
    Storage_Capacity_model = pickle.load(f)
storage_accuracy = check_accuracy(Storage_Capacity_model, storage, "Storage Capacity")
print(storage_accuracy)

with open("models/Color Family_model", "rb") as f:
    Color_Family_model = pickle.load(f)
color_accuracy = check_accuracy(Color_Family_model, color, "Color Family")
print(color_accuracy)

with open("models/Phone Model_model", "rb") as f:
    Phone_Model_model = pickle.load(f)
model_accuracy = check_accuracy(Phone_Model_model, model, "Phone Model")
print(model_accuracy)

with open("models/Camera_model", "rb") as f:
    Camera_model = pickle.load(f)
camera_accuracy = check_accuracy(Camera_model, camera, "Camera")
print(camera_accuracy)

with open("models/Phone Screen Size_model", "rb") as f:
    Phone_Screen_Size_model = pickle.load(f)
size_accuracy = check_accuracy(Phone_Screen_Size_model, size, "Phone Screen Size")
print(size_accuracy)


################################################################################
#
# Make Prediction
#
################################################################################

config = ('-l eng --oem 1 --psm 3')
valData = pd.read_csv("mobile_data_info_val_competition.csv")
outData = pd.DataFrame(columns=['id', 'tagging'])

i=0
total = len(valData)

for index, row in valData.iterrows():
    #
    os_prediction = get_n_predictions(Operating_System_model, 2, row["title"])
    outData = outData.append({'id': str(row["itemid"])+"_Operating System", 'tagging': os_prediction[0]}, ignore_index=True)
    #
    feature_prediction = get_n_predictions(Features_model, 2, row["title"])
    outData = outData.append({'id': str(row["itemid"])+"_Features", 'tagging': feature_prediction[0]}, ignore_index=True)
    #
    network_prediction = get_n_predictions(Network_Connections_model, 2, row["title"])
    outData = outData.append({'id': str(row["itemid"])+"_Network Connection", 'tagging': network_prediction[0]}, ignore_index=True)
    #
    ram_prediction = get_n_predictions(Memory_RAM_model, 2, row["title"])
    outData = outData.append({'id': str(row["itemid"])+"_Memory RAM", 'tagging': ram_prediction[0]}, ignore_index=True)
    #
    brand_prediction = get_n_predictions(Brand_model, 2, row["title"])
    outData = outData.append({'id': str(row["itemid"])+"_Brand", 'tagging': brand_prediction[0]}, ignore_index=True)
    #
    color_predictoin = get_n_predictions(Color_Family_model,2,row["title"])
    outData = outData.append({'id':str(row["itemid"])+"_Color Family", 'tagging':color_predictoin[0]},ignore_index=True)
    #
    network_prediction = get_n_predictions(Warranty_Period_model, 2, row["title"])
    outData = outData.append({'id': str(row["itemid"])+"_Warranty Period", 'tagging': warranty_prediction[0]}, ignore_index=True)
    #
    storage_prediction = get_n_predictions(Storage_Capacity_model, 2, row["title"])
    outData = outData.append({'id': str(row["itemid"])+"_Storage Capacity", 'tagging': storage_prediction[0]}, ignore_index=True)
    #
    model_prediction = get_n_predictions(Phone_Model_model, 2, row["title"])
    outData = outData.append({'id': str(row["itemid"])+"_Phone Model", 'tagging': model_prediction[0]}, ignore_index=True)
    #
    camera_prediction = get_n_predictions(Camera_model, 2, row["title"])
    outData = outData.append({'id': str(row["itemid"])+"_Camera", 'tagging': camera_prediction[0]}, ignore_index=True)
    #
    size_prediction = get_n_predictions(Phone_Screen_Size_model, 2, row["title"])
    outData = outData.append({'id': str(row["itemid"])+"_Phone Screen Size", 'tagging': size_prediction[0]}, ignore_index=True)
    #
    print(index/total)

outData.to_csv("mobile.csv")
