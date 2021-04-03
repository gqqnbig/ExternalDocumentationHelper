import django.http
import re


def index(request: django.http.HttpRequest):
	version = request.COOKIES.get('v')


def fixNamespace(identifier):
	identifier = re.sub(r'\.ops\.dataset_ops\.DatasetV\d\.', '.Dataset.', identifier)
	identifier = re.sub(r'\.framework\.ops\.', '.', identifier)
	return identifier


ruledConversions = {
	r'tensorflow_core\.python\.read_file': 'tf.io.read_file',
	r'tensorflow_core\.python\.keras\.engine\.network\.Network\.([a-z]\w*)': r'tf.keras.Model#\1',
	r'tensorflow_core\.python\.keras\.engine\.network\.Network': r'tf.keras.Model',
	r'tensorflow_core\.python\.keras\.saving\.save\.([a-z]\w*)': r'tf.keras.models.\1',
	r'tensorflow\.python\.ops\.random_ops\.random_([a-z]\w*)': r'tf.random.\1',
	r'tensorflow\.python\.ops\.confusion_matrix\.confusion_matrix': r'tf.math.confusion_matrix',
}


def tensorflow(request: django.http.HttpRequest):
	qualifiedIdentifier = request.GET.get('q', '').strip()
	method = request.GET.get('m', '').strip()
	version = request.COOKIES.get('v', '').strip()

	# if version is determined by cookie, do not make permanent redirect
	isPermanentRedirect = version == ''
	version = request.GET.get('v', version).strip()

	isProcessed = False
	for pattern, replace in ruledConversions.items():
		q, n = re.subn(pattern, replace, qualifiedIdentifier)
		if n > 0:
			isProcessed = True
			qualifiedIdentifier = q
			break

	if not isProcessed:
		qualifiedIdentifier = re.sub(r'^tensorflow_core\.(python\.)?', 'tf.', qualifiedIdentifier)

		qualifiedIdentifier = fixNamespace(qualifiedIdentifier)

		if qualifiedIdentifier.endswith('.' + method):
			qualifiedIdentifier = qualifiedIdentifier[:len(qualifiedIdentifier) - len('.' + method)]
			if qualifiedIdentifier == 'tf':
				# it's a static method under tf.
				qualifiedIdentifier = qualifiedIdentifier + '.' + method
			else:
				qualifiedIdentifier = qualifiedIdentifier + '#' + method

	url = qualifiedIdentifier.replace('.', '/')

	if version != '':
		url = f'https://www.tensorflow.org/versions/r{version}/api_docs/python/' + url
	else:
		url = 'https://www.tensorflow.org/api_docs/python/' + url

	if isPermanentRedirect:
		return django.http.HttpResponsePermanentRedirect(url)
	else:
		return django.http.HttpResponseRedirect(url)
