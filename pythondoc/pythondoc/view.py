import django.http
import re


def fixNamespace(identifier):
	identifier = re.sub(r'\.ops\.dataset_ops\.DatasetV\d\.', '.Dataset.', identifier)
	identifier = re.sub(r'\.framework\.ops\.', '.', identifier)
	return identifier


def tensorflow(request: django.http.HttpRequest):
	qualifiedIdentifier = request.GET.get('q', '').strip()
	method = request.GET.get('m', '').strip()

	qualifiedIdentifier = re.sub(r'^tensorflow_core\.python\.', 'tf.', qualifiedIdentifier)

	qualifiedIdentifier = fixNamespace(qualifiedIdentifier)

	if qualifiedIdentifier.endswith('.' + method):
		qualifiedIdentifier = qualifiedIdentifier[:len(qualifiedIdentifier) - len('.' + method)]
		if qualifiedIdentifier == 'tf':
			# it's a static method under tf.
			qualifiedIdentifier = qualifiedIdentifier + '.' + method
		else:
			qualifiedIdentifier = qualifiedIdentifier + '#' + method


	url = qualifiedIdentifier.replace('.', '/')

	url = 'https://www.tensorflow.org/api_docs/python/' + url

	# if version is determined by cookie, do not make permanent redirect
	return django.http.HttpResponsePermanentRedirect(url)
