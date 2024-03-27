###################################################
# Veri Seti Hikayesi
###################################################

# Amazon ürün verilerini içeren bu veri seti ürün kategorileri ile çeşitli metadataları içermektedir.
# Elektronik kategorisindeki en fazla yorum alan ürünün kullanıcı puanları ve yorumları vardır.

# Değişkenler:
# reviewerID: Kullanıcı ID’si
# asin: Ürün ID’si
# reviewerName: Kullanıcı Adı
# helpful: Faydalı değerlendirme derecesi
# reviewText: Değerlendirme
# overall: Ürün rating’i
# summary: Değerlendirme özeti
# unixReviewTime: Değerlendirme zamanı
# reviewTime: Değerlendirme zamanı Raw
# day_diff: Değerlendirmeden itibaren geçen gün sayısı
# helpful_yes: Değerlendirmenin faydalı bulunma sayısı
# total_vote: Değerlendirmeye verilen oy sayısı

import pandas as pd
import math
import scipy.stats as st
from pandas import DataFrame
from sklearn.preprocessing import MinMaxScaler
pd.set_option('display.max_columns', None)
pd.set_option("display.max_rows", None)
pd.set_option('display.width',500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: "%.5f" %x)

df: DataFrame= pd.read_csv("Week 4 Measurement Problems/amazon_review.csv")
df_= df.copy
df.head(50)

#GÖREV 1
#Adım1: Ürünün ortalama puanını hesaplayınız.

df["overall"].value_counts()
df["overall"].mean()

#Adım 2: Tarihe göre ağırlıklı puan ortalamasını hesaplayınız.
df.loc[df["day_diff"]<=30,"overall"].mean()
df.loc[(df["day_diff"]>30) & (df["day_diff"]<=90),"overall"].mean()
df.loc[(df["day_diff"]>90) & (df["day_diff"]<=180),"overall"].mean()
df.loc[(df["day_diff"]>180).mean()

#Adım 3: Ağırlıklandırılmış puanlamada her bir zaman diliminin ortalamasını karşılaştırıp yorumlayınız.

df.loc[df["day_diff"]<=30,"overall"].mean() * 28/100 +\
df.loc[(df["day_diff"]>30) & (df["day_diff"]<=90),"overall"].mean() * 26/100 +\
df.loc[(df["day_diff"]>90) & (df["day_diff"]<=180),"overall"].mean() * 24/100 +\
df.loc[(df["day_diff"]>180).mean() * 22/100

#def time_based_weighted_average(dataframe, w1:28,w2:26,w3:24,w4:22):

#return dataframe.loc[df["day_diff"]<=30,"overall"].mean()* w1/100 + \
#dataframe.loc[(dataframe["day_diff"]>30) & (df["day_diff"]<=90),"overall"].mean()* w2/100 +\
#dataframe.loc[(dataframe["day_diff"]>90) & (df["day_diff"]<=180),"overall"].mean()* w3/100 +\
#dataframe.loc[(dataframe["day_diff"]>180).mean()* w4/100

#time_based_weighted_average(df)

#GÖREV 2 : Ürün için ürün detay sayfasında görüntülenecek 20 review’i belirleyiniz.

#Adım 1: helpful_no değişkenini üretiniz.

#total_vote bir yoruma verilen toplam up-down sayısıdır.
#up, helpful demektir.
#Veri setinde helpful_no değişkeni yoktur, var olan değişkenler üzerinden üretilmesi gerekmektedir.
#Toplam oy sayısından (total_vote) yararlı oy sayısı (helpful_yes) çıkarılarak yararlı bulunmayan oy sayılarını (helpful_no) bulunuz.

df["helpful_no"]= df["total_vote"] - df["helpful_yes"]
df.head()


#Adım 2: score_pos_neg_diff, score_average_rating ve wilson_lower_bound skorlarını hesaplayıp veriye ekleyiniz.
#score_pos_neg_diff, score_average_rating ve wilson_lower_bound skorlarını hesaplayabilmek için score_pos_neg_diff, score_average_rating ve wilson_lower_bound fonksiyonlarını tanımlayınız.
#score_pos_neg_diff'a göre skorlar oluşturunuz. Ardından; df içerisinde score_pos_neg_diff ismiyle kaydediniz.
#score_average_rating'a göre skorlar oluşturunuz. Ardından; df içerisinde score_average_rating ismiyle kaydediniz.
#wilson_lower_bound'a göre skorlar oluşturunuz. Ardından; df içerisinde wilson_lower_bound ismiyle kaydediniz.


# score_pos_neg_diff fonksiyonu
def score_pos_neg_diff(up, down):
    return up - down

df["score_pos_neg_diff"] = df.apply(lambda x: score_pos_neg_diff(x["helpful_yes"], x["helpful_no"]), axis=1)
df.head(20)

#df["score_pos_neg_diff"]= MinMaxScaler(feature_range=(1,5)).fit(df[["helpful_no"]]) \
   # .transform(df[["helpful_no"]])

#df["score_average_rating"]= MinMaxScaler(feature_range=(1,5)).fit(df[["overall"]]) \
   # .transform(df[["overall"]])
#df.head()

#df["score_average_rating"]=
#def score_average_rating(df):


   # if df[helpful_yes]+ df["helpful_no"]==0:
        #return 0



    #return (df["helpful_yes"]/df["helpful_yes"]+ df["helpful_no"])
# score_average_rating fonksiyonu
def score_average_rating(up, down):
    if up + down == 0:
        return 0
    else:
        return up / (up + down)

df["score_average_rating"] = df.apply(lambda x: score_average_rating(x["helpful_yes"], x["helpful_no"]), axis=1)


def wilson_lower_bound_score(df,guven_araligi):
    df["wilson_lower_bound"] = n = df["helpful_yes"] + df["helpful_no"]

    if n == 0:
        return 0

    z = st.norm.ppf(1 - (1 - guven_araligi) / 2)
    phat = 1.0 * df["helpful_yes"] / n

    return ((phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n))

guven_araligi = 0.95
pri
#Adım 3: 20 Yorumu belirleyiniz ve sonuçları Yorumlayınız.
#wilson_lower_bound'a göre ilk 20 yorumu belirleyip sıralayanız.
#Sonuçları yorumlayınız.

df["wilson_lower_bound"].sort_values(ascending=False,).head(20)

