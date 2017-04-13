# -*- coding:utf-8 -*-
import jieba, os
from gensim import corpora, models
import sys
import requests
import jieba
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')
def sp(page):
    cookie={'Cookie':'_T_WM=a40da23f4b49e18c2fc15bac6db9c42d; ALF=1494382792; SCF=AnG7ojpmmH1bLhkAgrI0fJoUjIDDEUzVEBDHdXc1DPK4Bg6n2L1Re6dwh5gfVu4vSix-CILAjEq6i8qx7u_PTJg.; SUB=_2A2517pzNDeRhGeNI7lYW9yjIyDiIHXVXECSFrDV6PUJbktBeLVHwkW0m-tXI0CO-v0HjOG4DkXRZeaTseQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5NkNEDYVkAGzhAlZv3jU055JpX5o2p5NHD95QfSo-XS0McSheXWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNSKqfShMNSoB0S5tt; SUHB=0y0ZlRe-w7c7P6; SSOLoginState=1491791006'}
    f = open('data.txt', 'w')
    for i in range(1,page):

        url = 'https://weibo.cn/leijun?page=%d'%i
        print url
        html = requests.get(url, cookies=cookie).content
        re = etree.HTML(html)
        data = re.xpath('//*[@class="c"]/div[1]/span/text()')
        for d in data:
             f.write(d+'\n')
    f.close()
def gener2list(gen):
    file=open('stopword.txt')
    f=file.read()
    stop=f.split('\n')
    l=[]
    for g in gen:
        if g not in stop:
            l.append(g)

    return l

def cutcode(file):
    file = open(file)
    f=file.read()
    train=[]
    change=f.split('\n')
    for c in change:
        cutstr=jieba.cut(c,cut_all=True)
        clist=gener2list(cutstr)
        if clist!=[]:
            train.append(clist)
    file.close()
    return train
#sp(657)
train=cutcode('data.txt')

#print train
dic = corpora.Dictionary(train)
corpus = [dic.doc2bow(text) for text in train]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lda = models.LdaModel(corpus_tfidf, id2word = dic, num_topics = 10)
corpus_lda = lda[corpus_tfidf]


for i in range(0, 10):
     print lda.print_topic(i)