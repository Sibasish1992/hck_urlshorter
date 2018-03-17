



from django.shortcuts import render
import json,os
# Create your views here.
from django.http import HttpResponse,Http404
from django.views.generic import View

from django.conf import settings
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import UrlStorage

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect


class JSONResponseMixin(object):
    def render_to_json_response(self, context, response_class=HttpResponse):
        return self.get_json_response(self.convert_context_to_json(context), response_class)
    def get_json_response(self, content, response_class, **httpresponse_kwargs):
        return response_class(content, content_type='application/json', **httpresponse_kwargs)
    def convert_context_to_json(self, context):
        return json.dumps(context)

class HomeView(JSONResponseMixin,View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("You're looking at me .")

class ShortURLView(JSONResponseMixin,View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("ShortURLView")

    def post(self, request, *args, **kwargs):

        data={"status": "FAILED","status_codes": ["BAD_DATA"]}
        body = request.body

        if body:
            json_data = json.loads(request.body.decode('utf-8'))
            if 'long_url' in json_data:
                long_url = json_data['long_url']
                val = URLValidator(schemes=['https','http'])
                try:
                    val(long_url)
                    url = UrlStorage.objects.create(
                        big_url = long_url
                    )
                    id = url.id
                    hash = encode_url(id)
                    short_url = settings.SHRT_URL_ENDPOINT+hash
                    data = {"short_url": short_url,"status": "OK","status_codes": []}
                    return self.render_to_json_response(data)

                except ValidationError as e:
                    data = {"status": "FAILED", "status_codes": ["INVALID_URLS"]}
                    return self.render_to_json_response(data)

            else:
                return self.render_to_json_response(data)
        else:
            return self.render_to_json_response(data)


class LongURLView(JSONResponseMixin,View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("LongURLView")

    def post(self, request, *args, **kwargs):
        data = {"status": "FAILED", "status_codes": ["BAD_DATA"]}
        body = request.body
        if body:
            json_data = json.loads(request.body.decode('utf-8'))
            if 'short_url' in json_data:
                short_url =  json_data['short_url']
                if settings.SHRT_URL_ENDPOINT in short_url:
                    hash_part  = short_url.replace(settings.SHRT_URL_ENDPOINT,"")

                    hash_list = hash_part.split("/")
                    if len(hash_list)<=2:
                        hash=""
                        if len(hash_list) == 2:
                            if hash_list[1] != "":
                                return self.render_to_json_response(data)
                            hash = hash_list[0]
                        else:
                            hash = hash_list[0]
                        id = decode_url(hash)
                        try:
                            url = UrlStorage.objects.get(pk=id)
                            long_url = url.big_url
                            data = {"long_url": long_url, "status": "OK", "status_codes": []}
                            return self.render_to_json_response(data)
                        except ObjectDoesNotExist:
                            data = {"status": "FAILED", "status_codes": ["SHORT_URLS_NOT_FOUND"]}
                            return self.render_to_json_response(data)

                    else:
                        return self.render_to_json_response(data)
                else:
                    return self.render_to_json_response(data)
            else:
                return self.render_to_json_response(data)

        else:
            return self.render_to_json_response(data)


class CleanUrlView(JSONResponseMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            UrlStorage.objects.all().delete()
            return HttpResponse("DB Cleaned")
        except :
            return HttpResponse("Error")

    def post(self, request, *args, **kwargs):
        try:
            UrlStorage.objects.all().delete()
            return self.render_to_json_response({"message":"Db Cleared"})
        except :
            return self.render_to_json_response({"message":"Error While Deleting All URLS!!!!!"})



class ShortURLSView(JSONResponseMixin,View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("ShortURLSView")

    def post(self, request, *args, **kwargs):
        data = {"status": "FAILED", "status_codes": ["BAD_DATA"]}
        body = request.body
        if body:
            json_data = json.loads(request.body.decode('utf-8'))
            if 'long_urls' in json_data:
                long_urls = json_data['long_urls']
                if len(long_urls) != 0:
                    val = URLValidator(schemes=['https', 'http'])
                    invalid_list= []
                    valid_dic = {}
                    is_valid = True
                    for long_url in long_urls:
                        try:
                            val(long_url)
                            url = UrlStorage.objects.create(
                                big_url=long_url
                            )
                            id = url.id
                            hash = encode_url(id)
                            short_url = settings.SHRT_URL_ENDPOINT + hash

                            if long_url in valid_dic:
                                already_url = valid_dic[long_url]
                                valid_dic[long_url] = short_url + " Or " +already_url
                            else:
                                valid_dic[long_url] = short_url
                        except ValidationError as e:
                            is_valid = False
                            invalid_list.append(long_url)
                    if is_valid:
                        data = {"short_urls": valid_dic,'invalid_urls':invalid_list ,"status": "OK", "status_codes": []}
                    else:
                        data = {"invalid_urls":invalid_list,"status": "FAILED", "status_codes": ["INVALID_URLS"]}

                    return self.render_to_json_response(data)
                else:
                    return self.render_to_json_response(data)
            else:
                return self.render_to_json_response(data)
        else:
            return self.render_to_json_response(data)


class HitCountView(JSONResponseMixin,View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("HitCountView")

    def post(self, request, *args, **kwargs):
        data = {"status": "FAILED", "status_codes": ["BAD_DATA"]}
        body = request.body
        if body:
            json_data = json.loads(request.body.decode('utf-8'))
            if 'short_url' in json_data:
                short_url =  json_data['short_url']
                if settings.SHRT_URL_ENDPOINT in short_url:
                    hash_part  = short_url.replace(settings.SHRT_URL_ENDPOINT,"")

                    hash_list = hash_part.split("/")
                    if len(hash_list)<=2:
                        hash=""
                        if len(hash_list) == 2:
                            if hash_list[1] != "":
                                return self.render_to_json_response(data)
                            hash = hash_list[0]
                        else:
                            hash = hash_list[0]
                        id = decode_url(hash)
                        try:
                            url = UrlStorage.objects.get(pk=id)
                            count = url.count
                            data = {"count": count, "status": "OK", "status_codes": []}
                            return self.render_to_json_response(data)
                        except ObjectDoesNotExist:
                            data = {"status": "FAILED", "status_codes": ["SHORT_URLS_NOT_FOUND"]}
                            return self.render_to_json_response(data)

                    else:
                        return self.render_to_json_response(data)
                else:
                    return self.render_to_json_response(data)
            else:
                return self.render_to_json_response(data)

        else:
            return self.render_to_json_response(data)




class LongURLSView(JSONResponseMixin,View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("LongURLSView")

    def post(self, request, *args, **kwargs):
        data = {"status": "FAILED", "status_codes": ["BAD_DATA"]}
        body = request.body
        if body:
            json_data = json.loads(request.body.decode('utf-8'))
            if 'short_urls' in json_data:
                short_urls =  json_data['short_urls']
                if len(short_urls) != 0 :
                    invalid_list = []
                    valid_dic = {}

                    is_valid = True
                    for short_url in short_urls:
                        if settings.SHRT_URL_ENDPOINT in short_url:
                            hash_part  = short_url.replace(settings.SHRT_URL_ENDPOINT,"")
                            hash_list = hash_part.split("/")
                            if len(hash_list)<=2:
                                hash=""
                                if len(hash_list) == 2:
                                    if hash_list[1] != "":
                                        is_valid = False
                                        invalid_list.append(short_url)
                                        continue
                                    hash = hash_list[0]
                                else:
                                    hash = hash_list[0]
                                id = decode_url(hash)
                                try:
                                    url = UrlStorage.objects.get(pk=id)
                                    long_url = url.big_url
                                    valid_dic[short_url] = long_url
                                except ObjectDoesNotExist:
                                    is_valid = False
                                    invalid_list.append(short_url)
                            else:
                                is_valid = False
                                invalid_list.append(short_url)
                        else:
                            is_valid = False
                            invalid_list.append(short_url)

                    if is_valid:
                        data = {"long_urls": valid_dic, 'invalid_urls': invalid_list, "status": "OK",
                                "status_codes": []}
                    else:
                        data = {"invalid_urls": invalid_list, "status": "FAILED",
                                "status_codes": ["SHORT_URLS_NOT_FOUND"]}
                    return self.render_to_json_response(data)
                else:
                    return self.render_to_json_response(data)
            else:
                return self.render_to_json_response(data)

        else:
            return self.render_to_json_response(data)



class RedirectToView(JSONResponseMixin,View):
    def get(self, request, *args, **kwargs):
        hash = self.kwargs['short_url_hash']
        id = decode_url(hash)
        try:
            url = UrlStorage.objects.get(pk=id)
            long_url = url.big_url
            url.count = url.count + 1
            url.save()
            return redirect(long_url)
        except ObjectDoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):
        hash = self.kwargs['short_url_hash']
        id = decode_url(hash)
        try:
            url = UrlStorage.objects.get(pk=id)
            long_url = url.big_url
            url.count = url.count+1
            url.save()
            return redirect(long_url)
        except ObjectDoesNotExist:
            raise Http404







'''Hashing Algo'''

DEFAULT_ALPHABET = settings.DEFAULT_ALPHABET
DEFAULT_BLOCK_SIZE = settings.DEFAULT_BLOCK_SIZE
MIN_LENGTH = settings.MIN_LENGTH


class UrlEncoder(object):
    def __init__(self, alphabet=DEFAULT_ALPHABET, block_size=DEFAULT_BLOCK_SIZE):
        self.alphabet = alphabet
        self.block_size = block_size
        self.mask = (1 << block_size) - 1
        self.mapping = list(range(block_size))
        self.mapping.reverse()

    def encode_url(self, n, min_length=MIN_LENGTH):
        return self.enbase(self.encode(n), min_length)

    def decode_url(self, n):
        return self.decode(self.debase(n))

    def encode(self, n):
        return (n & ~self.mask) | self._encode(n & self.mask)

    def _encode(self, n):
        result = 0
        for i, b in enumerate(self.mapping):
            if n & (1 << i):
                result |= (1 << b)
        return result

    def decode(self, n):
        return (n & ~self.mask) | self._decode(n & self.mask)

    def _decode(self, n):
        result = 0
        for i, b in enumerate(self.mapping):
            if n & (1 << b):
                result |= (1 << i)
        return result

    def enbase(self, x, min_length=MIN_LENGTH):
        print(type(x))
        result = self._enbase(x)
        padding = self.alphabet[0] * (min_length - len(result))
        return '%s%s' % (padding, result)

    def _enbase(self, x):
        n = len(self.alphabet)
        if x < n:
            print(type(x))
            return self.alphabet[x]
        return self._enbase(int(x / n)) + self.alphabet[int(x % n)]

    def debase(self, x):
        n = len(self.alphabet)
        result = 0
        for i, c in enumerate(reversed(x)):
            result += self.alphabet.index(c) * (n ** i)
        return result


DEFAULT_ENCODER = UrlEncoder()


def encode(n):
    return DEFAULT_ENCODER.encode(n)


def decode(n):
    return DEFAULT_ENCODER.decode(n)


def enbase(n, min_length=MIN_LENGTH):
    return DEFAULT_ENCODER.enbase(n, min_length)


def debase(n):
    return DEFAULT_ENCODER.debase(n)


def encode_url(n, min_length=MIN_LENGTH):
    return DEFAULT_ENCODER.encode_url(n, min_length)


def decode_url(n):
    return DEFAULT_ENCODER.decode_url(n)



