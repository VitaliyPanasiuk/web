from django.http.response import Http404
from .models import AuthUser
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.http import HttpResponse
from .models import Продукт, ShopCalls, ShopCategory
from django.db import models
import requests
from requests.exceptions import MissingSchema
from datetime import datetime
from django.contrib import messages
import math

продукты = Продукт.objects.all()

x = 0
y = 4


def homePage(request, lang):
    language = request.POST.get("language", "")
    if request.POST:
        if language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect("/" + current_user.user_language)
            else:
                return redirect("/" + str(language))
        else:
            HttpResponse("404")
    else:
        if request.user.id != None:
            current_user = AuthUser.objects.get(id=request.user.id)
            context = {
                "lang": lang, 
            }
            try:
                return render(
                    request, current_user.user_language + "/shop/index.html", context
                )
            except TypeError:
                return render(request, str(lang) + "/shop/index.html", context)
        else:
            context = {
                "lang": lang,
            }
            return render(request, str(lang) + "/shop/index.html", context)

'''def redirectProductsPage(request, lang):
    return redirect("/" + str(lang) + "/products/p1")'''


def productsPage(request, lang):
    start = 0
    end = 20
    if request.POST:
        search = request.POST.get("search", "")
        searchTextRaw = request.POST.get("searchtext", "")
        searchText = searchTextRaw.replace(" ", "-")
        applyfilters = request.POST.get("applyfilters", "")
        nofilters = request.POST.get("nofilters", "")
        language = request.POST.get("language", "")
        try:
            page = int(request.POST.get("page", ""))
        except ValueError:
            page = 1
        withpriceStatus = request.POST.get("withpriceStatus", "")
        availableStatus = request.POST.get("availableStatus", "")
        nextPage = request.POST.get("nextPage", "")
        prevPage = request.POST.get("prevPage", "")
        
        if search:
            return redirect("/" + str(lang) + "/products/search/?q=" + searchText)
        elif nextPage:
            page += 1
            print(page)
            for i in range(page-1):
                start += 20
                end += 20
            if availableStatus == "yes" and withpriceStatus == "yes":
                filteredProducts = Продукт.objects.exclude(наличие="-").exclude(цена=None)[start:end] 
                maxPage = math.ceil(len(Продукт.objects.exclude(наличие="-").exclude(цена=None))/20)
            elif availableStatus == "spec" and withpriceStatus == "spec":
                filteredProducts = продукты[start:end]
                maxPage = math.ceil(len(продукты)/20)
            elif availableStatus == "yes" and withpriceStatus == "no":
                filteredProducts = Продукт.objects.exclude(наличие="-").filter(цена=None)[start:end]
                maxPage = math.ceil(len(Продукт.objects.exclude(наличие="-").filter(цена=None))/20)
            elif availableStatus == "no" and withpriceStatus == "yes":
                filteredProducts = Продукт.objects.exclude(цена=None).filter(наличие="-")[start:end]
                maxPage = math.ceil(len(Продукт.objects.exclude(цена=None).filter(наличие="-"))/20)
            elif availableStatus == "no" and withpriceStatus == "no":
                filteredProducts = Продукт.objects.filter(цена=None).filter(наличие="-")[start:end]
                maxPage = math.ceil(len(Продукт.objects.filter(цена=None).filter(наличие="-"))/20)
            elif availableStatus == "yes" and withpriceStatus == "spec":
                filteredProducts = Продукт.objects.exclude(наличие="-")[start:end]
                maxPage = math.ceil(len(Продукт.objects.exclude(наличие="-"))/20)
            elif availableStatus == "no" and withpriceStatus == "spec":
                filteredProducts = Продукт.objects.filter(наличие="-")[start:end]
                maxPage = math.ceil(len(Продукт.objects.filter(наличие="-"))/20)
            elif availableStatus == "spec" and withpriceStatus == "yes":
                filteredProducts = Продукт.objects.exclude(цена=None)[start:end]
                maxPage = math.ceil(len(Продукт.objects.exclude(цена=None))/20)
            elif availableStatus == "spec" and withpriceStatus == "no":
                filteredProducts = Продукт.objects.filter(цена=None)[start:end]
                maxPage = math.ceil(len(Продукт.objects.filter(цена=None))/20)
            context = {
                "продукты": filteredProducts,
                "available": availableStatus,
                "withprice": withpriceStatus,
                "lang": lang,
                "page": page,
                "category": ShopCategory.objects.all(),
                "maxPage": maxPage,
            }
            template = str(lang) + "/products/index.html"
            return render(request, template, context)
        elif prevPage:
            page -= 1
            start = 0
            end = 20
            for i in range(page-1):
                start += 20
                end += 20
            if availableStatus == "yes" and withpriceStatus == "yes":
                filteredProducts = Продукт.objects.exclude(наличие="-").exclude(цена=None)[start:end] 
                maxPage = math.ceil(len(Продукт.objects.exclude(наличие="-").exclude(цена=None))/20)
            elif availableStatus == "spec" and withpriceStatus == "spec":
                filteredProducts = продукты[start:end]
                maxPage = math.ceil(len(продукты)/20)
            elif availableStatus == "yes" and withpriceStatus == "no":
                filteredProducts = Продукт.objects.exclude(наличие="-").filter(цена=None)[start:end]
                maxPage = math.ceil(len(Продукт.objects.exclude(наличие="-").filter(цена=None))/20)
            elif availableStatus == "no" and withpriceStatus == "yes":
                filteredProducts = Продукт.objects.exclude(цена=None).filter(наличие="-")[start:end]
                maxPage = math.ceil(len(Продукт.objects.exclude(цена=None).filter(наличие="-"))/20)
            elif availableStatus == "no" and withpriceStatus == "no":
                filteredProducts = Продукт.objects.filter(цена=None).filter(наличие="-")[start:end]
                maxPage = math.ceil(len(Продукт.objects.filter(цена=None).filter(наличие="-"))/20)
            elif availableStatus == "yes" and withpriceStatus == "spec":
                filteredProducts = Продукт.objects.exclude(наличие="-")[start:end]
                maxPage = math.ceil(len(Продукт.objects.exclude(наличие="-"))/20)
            elif availableStatus == "no" and withpriceStatus == "spec":
                filteredProducts = Продукт.objects.filter(наличие="-")[start:end]
                maxPage = math.ceil(len(Продукт.objects.filter(наличие="-"))/20)
            elif availableStatus == "spec" and withpriceStatus == "yes":
                filteredProducts = Продукт.objects.exclude(цена=None)[start:end]
                maxPage = math.ceil(len(Продукт.objects.exclude(цена=None))/20)
            elif availableStatus == "spec" and withpriceStatus == "no":
                filteredProducts = Продукт.objects.filter(цена=None)[start:end]
                maxPage = math.ceil(len(Продукт.objects.filter(цена=None))/20)
            context = {
                "продукты": filteredProducts,
                "available": availableStatus,
                "withprice": withpriceStatus,
                "lang": lang,
                "page": page,
                "category": ShopCategory.objects.all(),
                "maxPage": maxPage,
            }
            template = str(lang) + "/products/index.html"
            return render(request, template, context)
        elif applyfilters:
            pricefilter = request.POST.get("pricefilter", "")
            availablefilter = request.POST.get("availablefilter", "")
            if pricefilter == "Цена есть" and availablefilter == "Есть":
                filteredProducts = Продукт.objects.exclude(цена=None).exclude(наличие="-")[start:end]  # | Продукт.objects.exclude(наличие='-') | Продукт.objects.exclude(цена='None')
                maxPage = math.ceil(len(Продукт.objects.exclude(наличие="-").exclude(цена=None))/20)
                context = {
                    "продукты": filteredProducts,
                    "withprice": "yes",
                    "available": "yes",
                    "lang": lang,
                    "page": page,
                    "category": ShopCategory.objects.all(),
                    "maxPage": maxPage,
                }
                template = str(lang) + "/products/index.html"
                return render(request, template, context)
            elif pricefilter == "Цена есть" and availablefilter == "Нету":
                filteredProducts = Продукт.objects.exclude(цена=None).filter(наличие="-")[start:end]
                maxPage = math.ceil(len(Продукт.objects.exclude(цена=None).filter(наличие="-"))/20)
                context = {
                    "продукты": filteredProducts,
                    "withprice": "yes",
                    "available": "no",
                    "lang": lang,
                    "page": page,
                    "category": ShopCategory.objects.all(),
                    "maxPage": maxPage,
                }
                template = str(lang) + "/products/index.html"
                return render(request, template, context)
            elif pricefilter == "Цены нет" and availablefilter == "Нету":
                filteredProducts = Продукт.objects.filter(цена=None).filter(наличие="-")[start:end]
                maxPage = math.ceil(len(Продукт.objects.filter(цена=None).filter(наличие="-"))/20)
                context = {
                    "продукты": filteredProducts,
                    "withprice": "no",
                    "available": "no",
                    "lang": lang,
                    "page": page,
                    "category": ShopCategory.objects.all(),
                    "maxPage": maxPage,
                }
                template = str(lang) + "/products/index.html"
                return render(request, template, context)
            elif pricefilter == "Цены нет" and availablefilter == "Есть":
                filteredProducts = Продукт.objects.exclude(наличие="-").filter(цена=None)[start:end]
                maxPage = math.ceil(len(Продукт.objects.filter(цена=None).filter(наличие="-"))/20)
                context = {
                    "продукты": filteredProducts,
                    "withprice": "no",
                    "available": "yes",
                    "lang": lang,
                    "page": page,
                    "category": ShopCategory.objects.all(),
                    "maxPage": maxPage,
                }
                template = str(lang) + "/products/index.html"
                return render(request, template, context)
            elif pricefilter == "Цены нет" and availablefilter == "":
                filteredProducts = Продукт.objects.filter(цена=None)[start:end]
                maxPage = math.ceil(len(Продукт.objects.filter(цена=None)[start:end])/20)
                context = {
                    "продукты": filteredProducts,
                    "withprice": "no",
                    "available": "spec",
                    "lang": lang,
                    "page": page,
                    "category": ShopCategory.objects.all(),
                    "maxPage": maxPage,
                }
                template = str(lang) + "/products/index.html"
                return render(request, template, context)
            elif pricefilter == "" and availablefilter == "Нету":
                filteredProducts = Продукт.objects.filter(наличие="-")[start:end]
                maxPage = math.ceil(len(Продукт.objects.filter(наличие="-")[start:end])/20)
                context = {
                    "продукты": filteredProducts,
                    "withprice": "spec",
                    "available": "no",
                    "lang": lang,
                    "page": page,
                    "category": ShopCategory.objects.all(),
                    "maxPage": maxPage,
                }
                template = str(lang) + "/products/index.html"
                return render(request, template, context)
            elif pricefilter == "Цена есть" and availablefilter == "":
                filteredProducts = Продукт.objects.exclude(цена=None)[start:end]
                maxPage = math.ceil(len(filteredProducts)/20)
                context = {
                    "продукты": filteredProducts,
                    "withprice": "yes",
                    "available": "spec",
                    "lang": lang,
                    "page": page,
                    "category": ShopCategory.objects.all(),
                    "maxPage": maxPage,
                }
                template = str(lang) + "/products/index.html"
                return render(request, template, context)
            elif pricefilter == "" and availablefilter == "Есть":
                filteredProducts = Продукт.objects.exclude(наличие="-")[start:end]
                maxPage = math.ceil(len(filteredProducts)/20)
                context = {
                    "продукты": filteredProducts,
                    "withprice": "spec",
                    "available": "yes",
                    "lang": lang,
                    "page": page,
                    "category": ShopCategory.objects.all(),
                    "maxPage": maxPage,
                }
                template = str(lang) + "/products/index.html"
                return render(request, template, context)
            elif pricefilter == "" and availablefilter == "Нету":
                filteredProducts = Продукт.objects.filter(наличие="-")[start:end]
                maxPage = math.ceil(len(filteredProducts)/20)
                context = {
                    "продукты": filteredProducts,
                    "withprice": "spec",
                    "available": "no",
                    "lang": lang,
                    "page": page,
                    "category": ShopCategory.objects.all(),
                    "maxPage": maxPage,
                }
                template = str(lang) + "/products/index.html"
                return render(request, template, context)
        elif nofilters:
            withpriceStatus = "spec"
            availableStatus = "spec"
            maxPage = math.ceil(len(продукты)/20)
            context = {
                "продукты": продукты[start:end],
                "withprice": "spec",
                "available": "spec",
                "lang": lang,
                "page": 1,
                "category": ShopCategory.objects.all(),
                "maxPage": maxPage,
            }
            template = str(lang) + "/products/index.html"
            return render(request, template, context)
        elif language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect("/" + current_user.user_language + "/products/")
            else:
                return redirect("/" + str(language) + "/products/")

    filteredProducts = Продукт.objects.exclude(наличие="-").exclude(цена=None)[start:end]
    maxPage = math.ceil(len(Продукт.objects.exclude(наличие="-").exclude(цена=None))/20)
    context = {
        "продукты": filteredProducts,
        "available": "yes",
        "withprice": "yes",
        "lang": lang,
        "page": 1,
        "category": ShopCategory.objects.all(),
        "maxPage": maxPage,
    }
    template = str(lang) + "/products/index.html"
    return render(request, template, context)


def categoryPage(request, lang, id):
    if request.POST:
        search = request.POST.get("search", "")
        searchTextRaw = request.POST.get("searchtext", "")
        searchText = searchTextRaw.replace(" ", "-")
        applyfilters = request.POST.get("applyfilters", "")
        nofilters = request.POST.get("nofilters", "")
        language = request.POST.get("language", "")
        if search:
            return redirect(
                "/"
                + str(lang)
                + "/products/category/"
                + str(id)
                + "/search/?q="
                + searchText
            )
        elif applyfilters:
            pricefilter = request.POST.get("pricefilter", "")
            availablefilter = request.POST.get("availablefilter", "")
            if pricefilter == "Цена есть" and availablefilter == "Есть":
                filteredProducts = (
                    Продукт.objects.exclude(цена=None)
                    .exclude(наличие="-")
                    .filter(категория=id)
                )  # | Продукт.objects.exclude(наличие='-') | Продукт.objects.exclude(цена='None')
                context = {
                    "продукты": filteredProducts,
                    "withprice": "yes",
                    "available": "yes",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/index.html"
                return render(request, template, context)
            elif pricefilter == "Цена есть" and availablefilter == "Нету":
                filteredProducts = (
                    Продукт.objects.exclude(цена=None)
                    .filter(наличие="-")
                    .filter(категория=id)
                )
                context = {
                    "продукты": filteredProducts,
                    "withprice": "yes",
                    "available": "no",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/index.html"
                return render(request, template, context)
            elif pricefilter == "Цены нет" and availablefilter == "Нету":
                filteredProducts = (
                    Продукт.objects.filter(цена=None)
                    .filter(наличие="-")
                    .filter(категория=id)
                )
                context = {
                    "продукты": filteredProducts,
                    "withprice": "no",
                    "available": "no",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/index.html"
                return render(request, template, context)
            elif pricefilter == "Цены нет" and availablefilter == "Есть":
                filteredProducts = (
                    Продукт.objects.exclude(наличие="-")
                    .filter(цена=None)
                    .filter(категория=id)
                )
                context = {
                    "продукты": filteredProducts,
                    "withprice": "no",
                    "available": "yes",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/index.html"
                return render(request, template, context)
            elif pricefilter == "Цены нет" and availablefilter == "":
                filteredProducts = Продукт.objects.filter(цена=None).filter(
                    категория=id
                )
                context = {
                    "продукты": filteredProducts,
                    "withprice": "no",
                    "available": "spec",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/index.html"
                return render(request, template, context)
            elif pricefilter == "" and availablefilter == "Нету":
                filteredProducts = Продукт.objects.filter(наличие="-").filter(
                    категория=id
                )
                context = {
                    "продукты": filteredProducts,
                    "withprice": "spec",
                    "available": "no",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/index.html"
                return render(request, template, context)
            elif pricefilter == "Цена есть" and availablefilter == "":
                filteredProducts = Продукт.objects.exclude(цена=None).filter(
                    категория=id
                )
                context = {
                    "продукты": filteredProducts,
                    "withprice": "yes",
                    "available": "spec",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/index.html"
                return render(request, template, context)
            elif pricefilter == "" and availablefilter == "Есть":
                filteredProducts = Продукт.objects.exclude(наличие="-").filter(
                    категория=id
                )
                context = {
                    "продукты": filteredProducts,
                    "withprice": "spec",
                    "available": "yes",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/index.html"
                return render(request, template, context)
            elif pricefilter == "" and availablefilter == "Нету":
                filteredProducts = Продукт.objects.filter(наличие="-").filter(
                    категория=id
                )
                context = {
                    "продукты": filteredProducts,
                    "withprice": "spec",
                    "available": "no",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/index.html"
                return render(request, template, context)
            elif pricefilter == "" and availablefilter == "":
                filteredProducts = Продукт.objects.filter(категория=id)
                context = {
                    "продукты": filteredProducts,
                    "withprice": "spec",
                    "available": "spec",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/index.html"
                return render(request, template, context)
        elif nofilters:
            filteredProducts = Продукт.objects.filter(категория=id)[:20]
            context = {
                "продукты": filteredProducts,
                "withprice": "spec",
                "available": "spec",
                "lang": lang,
                "category": ShopCategory.objects.all(),
            }
            template = str(lang) + "/products/category/index.html"
            return render(request, template, context)
        elif language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect(
                    "/"
                    + current_user.user_language
                    + "/products/category/"
                    + str(id)
                    + "/"
                )
            else:
                return redirect(
                    "/" + str(language) + "/products/category/" + str(id) + "/"
                )

    else:
        template = str(lang) + "/products/category/index.html"
        # category = ShopCategory.objects.get(id=id)
        filteredProducts = Продукт.objects.filter(категория=id)[:20]
        context = {
            "продукты": filteredProducts,
            "lang": lang,
            "withprice": "spec",
            "available": "spec",
            "category": ShopCategory.objects.all(),
        }
        # return HttpResponse(filteredProducts)
        return render(request, template, context)


def searchPage(request, lang):
    q = request.GET.get("q").replace("-", " ").lower()
    if lang == "ru":
        a = Продукт.objects.filter(название_позиции__icontains=q)
    elif lang == "en":
        a = Продукт.objects.filter(name__icontains=q)
    elif lang == "uk":
        a = Продукт.objects.filter(название_позиции_укр__icontains=q)
    if q == "":
        return redirect("/" + str(lang) + "/products/")
    if request.POST:
        page = 1
        counter = 20
        search = request.POST.get("search", "")
        searchTextRaw = request.POST.get("searchtext", "")
        searchText = searchTextRaw.replace(" ", "-")
        applyfilters = request.POST.get("applyfilters", "")
        nofilters = request.POST.get("nofilters", "")
        language = request.POST.get("language", "")
        if search:
            return redirect("/" + str(lang) + "/products/search/?q=" + searchText)
        elif applyfilters:
            pricefilter = request.POST.get("pricefilter", "")
            availablefilter = request.POST.get("availablefilter", "")
            if pricefilter == "Цена есть" and availablefilter == "Есть":
                filteredProducts = (
                    Продукт.objects.exclude(цена=None)
                    .exclude(наличие="-")
                    .filter(название_позиции__icontains=q.lower())
                )  # | Продукт.objects.exclude(наличие='-') | Продукт.objects.exclude(цена='None')
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "withprice": "yes",
                    "available": "yes",
                    "lang": lang,
                }
                template = str(lang) + "/products/search/index.html"
                return render(request, template, context)
            elif pricefilter == "Цена есть" and availablefilter == "Нету":
                filteredProducts = (
                    Продукт.objects.exclude(цена=None)
                    .filter(наличие="-")
                    .filter(название_позиции__icontains=q.lower())
                )
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "withprice": "yes",
                    "available": "no",
                    "lang": lang,
                }
                template = str(lang) + "/products/search/index.html"
                return render(request, template, context)
            elif pricefilter == "Цены нет" and availablefilter == "Нету":
                filteredProducts = (
                    Продукт.objects.filter(цена=None)
                    .filter(наличие="-")
                    .filter(название_позиции__icontains=q.lower())
                )
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "withprice": "no",
                    "available": "no",
                    "lang": lang,
                }
                template = str(lang) + "/products/search/index.html"
                return render(request, template, context)
            elif pricefilter == "Цены нет" and availablefilter == "Нету":
                filteredProducts = (
                    Продукт.objects.filter(цена=None)
                    .filter(наличие="-")
                    .filter(название_позиции__icontains=q.lower())
                )
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "withprice": "no",
                    "available": "no",
                    "lang": lang,
                }
                template = str(lang) + "/products/search/index.html"
                return render(request, template, context)
            elif pricefilter == "Цены нет" and availablefilter == "Есть":
                filteredProducts = Продукт.objects.filter(цена=None).filter(
                    название_позиции__icontains=q.lower()
                )
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "withprice": "no",
                    "available": "yes",
                    "lang": lang,
                }
                template = str(lang) + "/products/search/index.html"
                return render(request, template, context)
            elif pricefilter == "Цена есть" and availablefilter == "":
                filteredProducts = Продукт.objects.exclude(цена=None).filter(
                    название_позиции__icontains=q.lower()
                )
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "lang": lang,
                    "withprice": "yes",
                    "available": "spec",
                }
                template = str(lang) + "/products/search/index.html"
                return render(request, template, context)
            elif pricefilter == "" and availablefilter == "Нету":
                filteredProducts = Продукт.objects.filter(наличие="-").filter(
                    название_позиции__icontains=q.lower()
                )
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "withprice": "spec",
                    "available": "no",
                    "lang": lang,
                }
                template = str(lang) + "/products/search/index.html"
                return render(request, template, context)
            elif pricefilter == "" and availablefilter == "Есть":
                filteredProducts = Продукт.objects.exclude(наличие="-").filter(
                    название_позиции__icontains=q.lower()
                )
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "withprice": "spec",
                    "available": "yes",
                    "lang": lang,
                }
                template = str(lang) + "/products/search/index.html"
                return render(request, template, context)
            elif pricefilter == "" and availablefilter == "":
                filteredProducts = Продукт.objects.filter(
                    название_позиции__icontains=q.lower()
                )
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "withprice": "spec",
                    "available": "spec",
                    "lang": lang,
                }
                template = str(lang) + "/products/search/index.html"
                return render(request, template, context)
            elif pricefilter == "Цены нет" and availablefilter == "":
                filteredProducts = Продукт.objects.filter(цена=None).filter(
                    название_позиции__icontains=q.lower()
                )
                context = {
                    "продукты": filteredProducts,
                    "withprice": "no",
                    "available": "spec",
                    "lang": lang,
                }
                template = str(lang) + "/products/index.html"
                return render(request, template, context)
            elif availablefilter == "Нету" and pricefilter == "":
                filteredProducts = Продукт.objects.filter(наличие="-").filter(
                    название_позиции__icontains=q.lower()
                )
                context = {
                    "продукты": filteredProducts,
                    "withprice": "spec",
                    "available": "no",
                    "lang": lang,
                }
                template = str(lang) + "/products/index.html"
                return render(request, template, context)

        elif nofilters:
            context = {
                "продукты": a,
                "page": int(page),
                "withprice": "spec",
                "available": "spec",
                "lang": lang,
            }
            template = str(lang) + "/products/search/index.html"
            return render(request, template, context)
        elif language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect(
                    "/" + current_user.user_language + "/products/search/?q=" + q
                )
            else:
                return redirect("/" + str(language) + "/products/search/?q=" + q)

    else:
        template = str(lang) + "/products/search/index.html"
        if len(a) == len(Продукт.objects.all()):
            if lang == "ru":
                context = {
                    #'продукты': a[0:len(a):],
                    "error_message": "Пустой запрос",
                    "lang": lang,
                    #'page': int(page),
                }
                return render(request, template, context)
            elif lang == "en":
                context = {
                    #'продукты': a[0:len(a):],
                    "error_message": "Empty search field",
                    "lang": lang,
                    #'page': int(page),
                }
                return render(request, template, context)
            elif lang == "uk":
                context = {
                    #'продукты': a[0:len(a):],
                    "error_message": "Порожнє поле пошуку",
                    "lang": lang,
                    #'page': int(page),
                }
            return render(request, template, context)
        elif len(a) == 0:
            if lang == "ru":
                context = {
                    #'продукты': a[0:len(a):],
                    "error_message": "По Вашему запросу ничего не найдено",
                    "lang": lang,
                    #'page': int(page),
                }
                return render(request, template, context)
            elif lang == "en":
                context = {
                    #'продукты': a[0:len(a):],
                    "error_message": "No results were found for your search",
                    "lang": lang,
                    #'page': int(page),
                }
                return render(request, template, context)
            elif lang == "uk":
                context = {
                    #'продукты': a[0:len(a):],
                    "error_message": "За Вашим запитом нічого не знайдено",
                    "lang": lang,
                    #'page': int(page),
                }
                return render(request, template, context)
        else:
            context = {
                "продукты": a[0 : len(a) :],
                "withprice": "spec",
                "available": "spec",
                "lang": lang,
                "category": ShopCategory.objects.all(),
                #'page': int(page),
            }
            return render(request, template, context)


def categorySearchPage(request, lang, id):
    q = request.GET.get("q").replace("-", " ").lower()
    if lang == "ru":
        a = Продукт.objects.filter(название_позиции__icontains=q).filter(категория=id)
    elif lang == "en":
        a = Продукт.objects.filter(name__icontains=q).filter(категория=id)
    elif lang == "uk":
        a = Продукт.objects.filter(название_позиции_укр__icontains=q).filter(
            категория=id
        )
    if q == "":
        return redirect("/" + str(lang) + "/products/category/" + str(id) + "/")
    if request.POST:
        page = 1
        counter = 20
        search = request.POST.get("search", "")
        searchTextRaw = request.POST.get("searchtext", "")
        searchText = searchTextRaw.replace(" ", "-")
        applyfilters = request.POST.get("applyfilters", "")
        nofilters = request.POST.get("nofilters", "")
        language = request.POST.get("language", "")
        if search:
            return redirect(
                "/"
                + str(lang)
                + "/products/category/"
                + str(id)
                + "/search/?q="
                + searchText
            )
        elif applyfilters:
            pricefilter = request.POST.get("pricefilter", "")
            availablefilter = request.POST.get("availablefilter", "")
            if pricefilter == "Цена есть" and availablefilter == "Есть":
                filteredProducts = (
                    Продукт.objects.exclude(цена=None)
                    .exclude(наличие="-")
                    .filter(название_позиции__icontains=q.lower())
                    .filter(категория=id)
                )  # | Продукт.objects.exclude(наличие='-') | Продукт.objects.exclude(цена='None')
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "withprice": "yes",
                    "available": "yes",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/search/index.html"
                return render(request, template, context)
            elif pricefilter == "Цена есть" and availablefilter == "Нету":
                filteredProducts = (
                    Продукт.objects.exclude(цена=None)
                    .filter(наличие="-")
                    .filter(название_позиции__icontains=q.lower())
                ).filter(категория=id)
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "withprice": "yes",
                    "available": "no",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/search/index.html"
                return render(request, template, context)
            elif pricefilter == "Цены нет" and availablefilter == "Нету":
                filteredProducts = (
                    Продукт.objects.filter(цена=None)
                    .filter(наличие="-")
                    .filter(название_позиции__icontains=q.lower())
                ).filter(категория=id)
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "withprice": "no",
                    "available": "no",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/search/index.html"
                return render(request, template, context)
            elif pricefilter == "Цены нет" and availablefilter == "Нету":
                filteredProducts = (
                    Продукт.objects.filter(цена=None)
                    .filter(наличие="-")
                    .filter(название_позиции__icontains=q.lower())
                ).filter(категория=id)
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "withprice": "no",
                    "available": "no",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/search/index.html"
                return render(request, template, context)
            elif pricefilter == "Цены нет" and availablefilter == "Есть":
                filteredProducts = (
                    Продукт.objects.filter(цена=None)
                    .filter(название_позиции__icontains=q.lower())
                    .filter(категория=id)
                )
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "withprice": "no",
                    "available": "yes",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/search/index.html"
                return render(request, template, context)
            elif pricefilter == "Цена есть" and availablefilter == "":
                filteredProducts = (
                    Продукт.objects.exclude(цена=None)
                    .filter(название_позиции__icontains=q.lower())
                    .filter(категория=id)
                )
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "lang": lang,
                    "withprice": "yes",
                    "available": "spec",
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/search/index.html"
                return render(request, template, context)
            elif pricefilter == "" and availablefilter == "Нету":
                filteredProducts = (
                    Продукт.objects.filter(наличие="-")
                    .filter(название_позиции__icontains=q.lower())
                    .filter(категория=id)
                )
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "withprice": "spec",
                    "available": "no",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/search/index.html"
                return render(request, template, context)
            elif pricefilter == "" and availablefilter == "Есть":
                filteredProducts = (
                    Продукт.objects.exclude(наличие="-")
                    .filter(название_позиции__icontains=q.lower())
                    .filter(категория=id)
                )
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "withprice": "spec",
                    "available": "yes",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/search/index.html"
                return render(request, template, context)
            elif pricefilter == "" and availablefilter == "":
                filteredProducts = Продукт.objects.filter(
                    название_позиции__icontains=q.lower()
                ).filter(категория=id)
                context = {
                    "продукты": filteredProducts,
                    "page": int(page),
                    "withprice": "spec",
                    "available": "spec",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/search/index.html"
                return render(request, template, context)
            elif pricefilter == "Цены нет" and availablefilter == "":
                filteredProducts = (
                    Продукт.objects.filter(цена=None)
                    .filter(название_позиции__icontains=q.lower())
                    .filter(категория=id)
                )
                context = {
                    "продукты": filteredProducts,
                    "withprice": "no",
                    "available": "spec",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/search/index.html"
                return render(request, template, context)
            elif availablefilter == "Нету" and pricefilter == "":
                filteredProducts = (
                    Продукт.objects.filter(наличие="-")
                    .filter(название_позиции__icontains=q.lower())
                    .filter(категория=id)
                )
                context = {
                    "продукты": filteredProducts,
                    "withprice": "spec",
                    "available": "no",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                }
                template = str(lang) + "/products/category/search/index.html"
                return render(request, template, context)

        elif nofilters:
            context = {
                "продукты": a,
                "page": int(page),
                "withprice": "spec",
                "available": "spec",
                "lang": lang,
                "category": ShopCategory.objects.all(),
            }
            template = str(lang) + "/products/category/search/index.html"
            return render(request, template, context)
        elif language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect(
                    "/"
                    + current_user.user_language
                    + "/products/category/"
                    + str(id)
                    + "/search/?q="
                    + q
                )
            else:
                return redirect(
                    "/"
                    + str(language)
                    + "/products/category/"
                    + str(id)
                    + "/search/?q="
                    + q
                )

    else:
        template = str(lang) + "/products/category/search/index.html"
        if len(a) == len(Продукт.objects.all()):
            if lang == "ru":
                context = {
                    #'продукты': a[0:len(a):],
                    "error_message": "Пустой запрос",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                    #'page': int(page),
                }
                return render(request, template, context)
            elif lang == "en":
                context = {
                    #'продукты': a[0:len(a):],
                    "error_message": "Empty search field",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                    #'page': int(page),
                }
                return render(request, template, context)
            elif lang == "uk":
                context = {
                    #'продукты': a[0:len(a):],
                    "error_message": "Порожнє поле пошуку",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                    #'page': int(page),
                }
            return render(request, template, context)
        elif len(a) == 0:
            if lang == "ru":
                context = {
                    #'продукты': a[0:len(a):],
                    "error_message": "По Вашему запросу ничего не найдено",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                    #'page': int(page),
                }
                return render(request, template, context)
            elif lang == "en":
                context = {
                    #'продукты': a[0:len(a):],
                    "error_message": "No results were found for your search",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                    #'page': int(page),
                }
                return render(request, template, context)
            elif lang == "uk":
                context = {
                    #'продукты': a[0:len(a):],
                    "error_message": "За Вашим запитом нічого не знайдено",
                    "lang": lang,
                    "category": ShopCategory.objects.all(),
                    #'page': int(page),
                }
                return render(request, template, context)
        else:

            context = {
                "продукты": a[0 : len(a) :],
                "withprice": "spec",
                "available": "spec",
                "lang": lang,
                "category": ShopCategory.objects.all(),
                #'page': int(page),
                "error": str(len(a)),
            }
            return render(request, template, context)


def error404(request, exception):
    return render(request, "ru/404.html")


def achievementsPage(request, lang):
    language = request.POST.get("language", "")
    if request.POST:
        if language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect("/" + current_user.user_language + "/achievements/")
            else:
                return redirect("/" + str(language) + "/achievements/")
        else:
            HttpResponse("404")
    else:
        context = {
            "lang": lang,
        }
        return render(request, str(lang) + "/achievements/index.html", context=context)


def aboutUsPage(request, lang):
    language = request.POST.get("language", "")
    if request.POST:
        if language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect("/" + current_user.user_language + "/about/")
            else:
                return redirect("/" + str(language) + "/about/")
        else:
            HttpResponse("404")
    else:
        context = {
            "lang": lang,
        }
        return render(request, str(lang) + "/about/index.html", context=context)


def collaborationPage(request, lang):
    language = request.POST.get("language", "")
    if request.POST:
        if language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect("/" + current_user.user_language + "/collaboration/")
            else:
                return redirect("/" + str(language) + "/collaboration/")
        else:
            HttpResponse("404")
    else:
        context = {
            "lang": lang,
        }
        return render(request, str(lang) + "/collaboration/index.html", context=context)


def guaranteesPage(request, lang):
    language = request.POST.get("language", "")
    if request.POST:
        if language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect("/" + current_user.user_language + "/guarantees/")
            else:
                return redirect("/" + str(language) + "/guarantees/")
        else:
            HttpResponse("404")
    else:
        context = {
            "lang": lang,
        }
        return render(request, str(lang) + "/guarantees/index.html", context=context)


def aboutProductPage(request, id, lang):
    class ShopCarty(models.Model):
        user_id = models.CharField(max_length=45)
        item = models.CharField(max_length=90, blank=True, null=True)
        cart_id = models.AutoField(primary_key=True)
        amount = models.IntegerField(blank=True, null=True, default=1)
        name = models.CharField(max_length=300, blank=True, null=True)
        price = models.CharField(max_length=30, blank=True, null=True)
        currency = models.CharField(max_length=30, blank=True, null=True)
        ru_order_item = models.CharField(max_length=500, null=True, blank=True)
        uk_order_item = models.CharField(max_length=500, null=True, blank=True)
        en_order_item = models.CharField(max_length=500, null=True, blank=True)

        class Meta:
            managed = False
            db_table = "shop_cart"

    carts = ShopCarty.objects.all()

    class ShopFavourite(models.Model):
        favourite_id = models.AutoField(primary_key=True)
        user_id = models.CharField(max_length=45)
        favourite_item = models.CharField(max_length=45, blank=True, null=True)
        name = models.CharField(max_length=300, blank=True, null=True)
        price = models.CharField(max_length=45, blank=True, null=True)
        currency = models.CharField(max_length=45, blank=True, null=True)
        ru_name = models.CharField(max_length=1000, blank=True, null=True)
        uk_name = models.CharField(max_length=1000, blank=True, null=True)
        image = models.CharField(max_length=200, null=True, blank=True)

        class Meta:
            managed = False
            db_table = "shop_favourite"

    """for i in продукты:
        if int(i.id) > 236:
            russian_desc = i.описание
            from googletrans import Translator
            translator = Translator(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
            english_desc = translator.translate(russian_desc, dest='en').text
            import time
            time.sleep(2)
            eng_name = translator.translate(i.название_позиции, dest='en').text
            time.sleep(2)
            print(english_desc + ' $ ' + eng_name)
            item = Продукт.objects.get(id=i.id)
            item.description = english_desc
            item.name = eng_name
            item.save()
            print(i.id)"""

    #favourites = ShopFavourite.objects.all()
    if request.POST:
        cart_add = request.POST.get("add_to_cart", "")
        favourite_add = request.POST.get("add_to_favourite", "")
        first_name = request.POST.get("callme_first_name", "")
        last_name = request.POST.get("callme_last_name", "")
        phone_number = request.POST.get("callme_phone_number")
        callme = request.POST.get("callme_inp_button", "")
        language = request.POST.get("language", "")
        if cart_add:
            item_id = request.POST.get("add_id", "")
            item_name_ru = request.POST.get("add_name_ru", "")
            item_name_uk = request.POST.get("add_name_uk", "")
            item_name_en = request.POST.get("add_name_en", "")
            item_price = request.POST.get("add_price", "")
            item_currency = request.POST.get("add_currency", "")
            howMuchToAdd = request.POST.get("how_much_to_add", "")
            if lang == "ru":
                product = Продукт.objects.get(id=item_id)
                if int(howMuchToAdd) >= int(round(product.минимальный_заказ_опт, 0)):
                    prce = product.оптовая_цена
                else:
                    prce = max(float(i) for i in item_price.replace(",", ".").split())
                try:
                    if int(howMuchToAdd) < product.минимальный_объем_заказа:
                        error_message = (
                            "Вы не можете заказать меньше "
                            + str(product.минимальный_объем_заказа)
                            + " единиц этого товара"
                        )
                        messages.error(request, error_message)
                        return redirect("/" + str(lang) + "/product/" + str(id))
                except TypeError:
                    error_message = (
                            "Вы не можете заказать меньше "
                            + str(product.минимальный_объем_заказа)
                            + " единиц этого товара"
                        )
                    messages.error(request, error_message)
                    return redirect("/" + str(lang) + "/product/" + str(id))  
                if product.скидка > 0:
                    prce = str(float(prce) * ((100 - int(product.скидка))/100))
                ToSave = ShopCarty(
                    user_id=request.user.id,
                    item=item_id,
                    name=item_name_ru,
                    price=prce,
                    currency=item_currency,
                    ru_order_item=item_name_ru,
                    en_order_item=item_name_en,
                    uk_order_item=item_name_uk,
                )
            elif lang == "en":
                product = Продукт.objects.get(id=item_id)
                if int(howMuchToAdd) >= int(round(product.минимальный_заказ_опт, 0)):
                    prce = product.оптовая_цена
                else:
                    prce = max(float(i) for i in item_price.replace(",", ".").split())
                try:
                    if int(howMuchToAdd) < product.минимальный_объем_заказа:
                        error_message = (
                            "You cannot order less than "
                            + str(product.минимальный_объем_заказа)
                            + " units"
                        )
                        messages.error(request, error_message)
                        return redirect("/" + str(lang) + "/product/" + str(id))
                except TypeError:
                    error_message = (
                            "You cannot order less than "
                            + str(product.минимальный_объем_заказа)
                            + " units"
                        )
                    messages.error(request, error_message)
                    return redirect("/" + str(lang) + "/product/" + str(id))
                if product.скидка > 0:
                    prce = prce * ((100 - product.скидка)/100)
                ToSave = ShopCarty(
                    user_id=request.user.id,
                    item=item_id,
                    name=item_name_ru,
                    price=prce,
                    currency=item_currency,
                    ru_order_item=item_name_ru,
                    en_order_item=item_name_en,
                    uk_order_item=item_name_uk,
                )
            elif lang == "uk":
                product = Продукт.objects.get(id=item_id)
                if int(howMuchToAdd) >= int(round(product.минимальный_заказ_опт, 0)):
                    prce = product.оптовая_цена
                else:
                    prce = max(float(i) for i in item_price.replace(",", ".").split())
                try:
                    if int(howMuchToAdd) < product.минимальный_объем_заказа:
                        error_message = (
                            "Ви не можете замовити менш як "
                            + str(product.минимальный_объем_заказа)
                            + " одиниць цього товару"
                        )
                        messages.error(request, error_message)
                        return redirect("/" + str(lang) + "/accounts/" + str(request.user.id) + '/cart')
                except TypeError:
                    if product.минимальный_объем_заказа == None:
                        error_message = (
                            "Ви не можете замовити цей товар "
                        )
                        messages.error(request, error_message)
                        return redirect("/" + str(lang) + "/accounts/" + str(request.user.id) + '/cart')
                    else:
                        error_message = (
                            "Ви не можете замовити менш як "
                            + str(product.минимальный_объем_заказа)
                            + " одиниць цього товару"
                        )
                        messages.error(request, error_message)
                        return redirect("/" + str(lang) + "/accounts/" + str(request.user.id) + '/cart')
                if product.скидка > 0:
                    prce = prce * ((100 - product.скидка)/100)
                ToSave = ShopCarty(
                user_id=request.user.id,
                item=item_id,
                name=item_name_ru,
                price=prce,
                currency=item_currency,
                ru_order_item=item_name_ru,
                en_order_item=item_name_en,
                uk_order_item=item_name_uk,
                )
            ToSave.save()
            cart_item = ShopCarty.objects.all()
            for i in cart_item:
                if i.amount:
                    ToSave.amount = i.amount + int(howMuchToAdd) - 1
                else:
                    ToSave.amount = i.amount + int(howMuchToAdd)
            for i in carts:
                if i.amount != ToSave.amount and i.item == ToSave.item:
                    ShopCarty.objects.filter(item=ToSave.item).delete()
                elif i.amount == ToSave.amount and i.item == ToSave.item:
                    ShopCarty.objects.filter(item=ToSave.item).delete()
            ToSave.save()
            return redirect(
                "/" + str(lang) + "/accounts/" + str(request.user.id) + "/cart"
            )
        elif language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect(
                    "/" + current_user.user_language + "/product/" + str(id)
                )
            else:
                return redirect("/" + str(language) + "/product/" + str(id))
        elif favourite_add:
            favourite_item_id = request.POST.get("favourite_add_id", "")
            favourite_item_name_ru = request.POST.get("favourite_add_name_ru", "")
            favourite_item_name_en = request.POST.get("favourite_add_name_en", "")
            favourite_item_name_uk = request.POST.get("favourite_add_name_uk", "")
            favourite_item_price = request.POST.get("favourite_add_price", "")
            favourite_item_currency = request.POST.get("favourite_add_currency", "")
            favourite_item_image = request.POST.get("favourite_add_image", "")
            if favourite_item_price == "None":
                favourite_item_price = 0
                favouriteToSave = ShopFavourite(
                    user_id=request.user.id,
                    favourite_item=favourite_item_id,
                    name=favourite_item_name_en,
                    price=favourite_item_price,
                    ru_name=favourite_item_name_ru,
                    uk_name=favourite_item_name_uk,
                    currency=favourite_item_currency,
                    image = favourite_item_image
                )
            else:
                favouriteToSave = ShopFavourite(
                    user_id=request.user.id,
                    favourite_item=favourite_item_id,
                    name=favourite_item_name_en,
                    ru_name=favourite_item_name_ru,
                    uk_name=favourite_item_name_uk,
                    price=max(
                        float(i) for i in favourite_item_price.replace(",", ".").split()
                    ),
                    currency=favourite_item_currency,
                    image = favourite_item_image
                )
            favouriteToSave.save()
            favourite_item = ShopFavourite.objects.all()
            for i in favourite_item:
                if i.favourite_item == favourite_item_id:
                    ShopFavourite.objects.filter(
                        favourite_item=favourite_item_id
                    ).delete()
            favouriteToSave.save()
            return redirect(
                "/" + str(lang) + "/accounts/" + str(request.user.id) + "/favourites"
            )
        elif callme:
            item_name = request.POST.get("add_name", "")
            item_price = request.POST.get("add_price", "")
            item_currency = request.POST.get("add_currency", "")
            call = ShopCalls(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                timedate=datetime.now(),
                viewed_product=item_name,
                price=item_price + " " + item_currency,
            )
            call.save()
            return redirect("/" + str(lang) + "/products")
    else:
        if request.user.is_authenticated == False:
            auth_status = "failed"
            product = Продукт.objects.get(id=int(id))
            context = {
                "продукт": product,
                "user_id": request.user.id,
                "auth_status": auth_status,
                "lang": lang,
            }
        else:
            user = AuthUser.objects.get(id=request.user.id)
            auth_status = "success"
            product = Продукт.objects.get(id=int(id))
            images = product.images.all()
            context = {
                "продукт": product,
                "user_id": request.user.id,
                "user": user,
                "auth_status": auth_status,
                "images": images,
                "lang": lang,
            }
        template = str(lang) + "/productInfo/more.html"
        context.update(csrf(request))
        return render(request, template, context)


def goWithLanguage(request):
    if request.user.id != None:
        current_user = AuthUser.objects.get(id=request.user.id)
        return redirect("/" + current_user.user_language)
    else:
        return redirect("/uk")
