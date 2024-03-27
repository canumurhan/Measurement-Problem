#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchasemetriğine odaklanılmalıdır.




#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBiddinguygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç

#####################################################
# Proje Görevleri
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.

#Görev 1: Veriyi Hazırlama ve Analiz Etme

#Adım 1: ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz.
#Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp,shapiro,levene,ttest_ind,mannwhitneyu,pearsonr,spearmanr,kendalltau,f_oneway,kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option("display.max_rows", None)
pd.set_option('display.width',500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: "%.1f" %x)



control_group=pd.read_excel("Week 4 Measurement Problems/ab_testing.xlsx", sheet_name="Control Group")
test_group=pd.read_excel("Week 4 Measurement Problems/ab_testing.xlsx", sheet_name="Test Group")

#Adım 2: Kontrol ve test grubu verilerini analiz ediniz.

control_group.describe().T
test_group.describe().T

#Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

control_group=control_group.astype(int)
test_group=test_group.astype(int)

control_group["group"]="control_group"
test_group["group"]="test_group"

df=pd.concat([control_group,test_group],axis=0,ignore_index=True)

#Görev 2: A/B Testinin Hipotezinin Tanımlanması

#Adım 1: Hipotezi tanımlayınız.
#H0 : M1 = M2 Average Bidding ile Maximum Bidding için (kazanç)ortalamaları arasında istatiksel olarak anlamlı bir farklılık yoktur.
#H1 : M1!= M2 Average Bidding ile Maximum Bidding için (kazanç)ortalamaları arasında istatiksel olarak anlamlı bir farklılık vardır.

#Adım 2: Kontrol ve test grubu için purchase (kazanç) ortalamalarını analiz ediniz.

df.groupby("group").agg({"Purchase":"mean"})

#Görev 3: Hipotez Testinin Gerçekleştirilmesi
#Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.

#Normallik varsayımını inceleyelim;
#HO:Normal dağılım varsayımı sağlanır.
#H1:Normal dağılım varsayımı sağlanmamaktadır.
test_stat,p_value=shapiro(df.loc[df["group"]=="control_group","Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, p_value))
test_stat,p_value=shapiro(df.loc[df["group"]=="test_group","Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, p_value))

#Varyans Homojenliği;
#H0:Varyanslar homojendir.
#H1:Varyanslar homojen değildir.
test_stat,p_value=levene(df.loc[df["group"]=="control_group","Purchase"],df.loc[df["group"]=="test_group","Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, p_value))

#iki koşulumuzda sağlamıştır.

#Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz.
#Varsayımlar sağlandığı için T Testi uygulayacağız.

#H0 : M1 = M2 Average Bidding ile Maximum Bidding için (kazanç)ortalamaları arasında istatiksel olarak anlamlı bir farklılık yoktur.
#H1 : M1!= M2 Average Bidding ile Maximum Bidding için (kazanç)ortalamaları arasında istatiksel olarak anlamlı bir farklılık vardır.

test_stat,p_value=ttest_ind(df.loc[df["group"]=="control_group","Purchase"],df.loc[df["group"]=="test_group","Purchase"],equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, p_value))

#Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak
# kontrol ve test grubu satın alma ortalamaları arasında
#istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

#Görev 4: Sonuçların Analizi
#Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.
#T testini uyguladık çünkü tüm varsayımlar sağlanıyordu. Bu sebeple parametrik yöntem olan
#T testini uyguladık.

#Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.
#Sunulan iki teklif yöntemi arasında anlamlı bir farklılık olmadığı istatiksel olarak %95
# güven düzeyinde ispatlanmıştır.dolayı bu iki yöntem arasında müşteriye yönelik
# yeni çalışmalar başlatılabilir veya bu iki yöntemden biri revize edilerek tekrar bir
#çalışma yapılabilir.