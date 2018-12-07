# coding=utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator
# Create your views here.

def index(request):

    # 分别查询最新4条的和最热的4条数据
    typelist = TypeInfo.objects.filter(isDelete=False)
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]

    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]

    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]

    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]

    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]

    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]

    context = {
        'title':'首页',
        'type0': type0,'type01': type01,
        'type1': type1, 'type11': type11,
        'type2': type2, 'type21': type21,
        'type3': type3, 'type31': type31,
        'type4': type4, 'type41': type41,
        'type5': type5, 'type51': type51,
    }
    print(type0)
    return render(request,'df_goods/index.html',context)


def list(request,tid,pindex,sort): # tid 商品类型 pindex 商品页码 sort分类方式
    #print(tid,pindex,sort)
    typeinfo = TypeInfo.objects.get(pk=tid)
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort == '1':
        goods_list = typeinfo.goodsinfo_set.order_by('-id')
    if sort == '2':
        goods_list = typeinfo.goodsinfo_set.order_by('-gprice')
    if sort == '3':
        goods_list = typeinfo.goodsinfo_set.order_by('-gclick')

    # 每页10个对商品结果集进行分页
    pageinator = Paginator(goods_list,5)
    # 返回指定页的对象集和
    page = pageinator.page(int(pindex))

    # 构建上下文
    context = {
        'title':typeinfo.ttitle,
        'news':news,
        'page':page,
        'typeinfo':typeinfo,
        'sort':sort
    }
    #print(news)
    return render(request,'df_goods/list.html',context)


def detail(request,id):

    goods = GoodsInfo.objects.get(pk=int(id))
    typeinfo = goods.gtype
    news = GoodsInfo.objects.filter(isDelete=False,gtype_id=typeinfo.id).order_by('-id')[0:2]
    context = {
        'title':typeinfo.ttitle,
        'id':id,
        'goods':goods,
        'typeinfo':typeinfo,
        'news':news
    }
    return render(request,'df_goods/detail.html',context)

