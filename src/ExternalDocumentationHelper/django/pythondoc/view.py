import django.http
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))
import ExternalDocumentationHelper.django.pythondoc.mapping as mapping


def index(request: django.http.HttpRequest):
	version = request.COOKIES.get('v')


def tensorflow(request: django.http.HttpRequest):
	qualifiedIdentifier = request.GET.get('q', '').strip()
	method = request.GET.get('m', '').strip()
	version = request.COOKIES.get('v', '').strip()

	# if version is determined by cookie, do not make permanent redirect
	isPermanentRedirect = version == ''
	version = request.GET.get('v', version).strip()

	qualifiedIdentifier = mapping.map(qualifiedIdentifier, method)

	url = qualifiedIdentifier.replace('.', '/')

	if version != '':
		url = f'https://www.tensorflow.org/versions/r{version}/api_docs/python/' + url
	else:
		url = 'https://www.tensorflow.org/api_docs/python/' + url

	if isPermanentRedirect:
		return django.http.HttpResponsePermanentRedirect(url)
	else:
		return django.http.HttpResponseRedirect(url)
