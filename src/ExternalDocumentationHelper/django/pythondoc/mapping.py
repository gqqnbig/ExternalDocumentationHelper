import re


def fixNamespace(identifier: str):
	assert identifier[-1] != '.'

	if identifier == 'tf':
		return 'tf.'

	identifier = re.sub(r'\.text_dataset$', '', identifier)
	identifier = re.sub(r'\.ops\.dataset_ops\.DatasetV\d$', '.Dataset', identifier)
	identifier = re.sub(r'\.ops\.(ragged\.ragged_)?string_ops', '.strings', identifier)
	identifier = re.sub(r'\.feature_column\.feature_column_v\d$', '.feature_column', identifier)

	p = identifier.rfind('.')
	if p > -1 and p + 1 < len(identifier) and identifier[p + 1].isupper():
		identifier += '#'
	else:
		identifier += '.'

	# identifier = re.sub(r'\.ops\.dataset_ops\.DatasetV\d\.', '.Dataset.', identifier)
	# identifier = re.sub(r'\.framework\.ops\.', '.', identifier)
	# identifier = re.sub(r'\.ops\.array_ops\.([a-z]\w*?)(_v\d)$', r'.\1', identifier)

	return identifier


ruledConversions = {
	r'tensorflow_core\.python\.read_file': 'tf.io.read_file',
	r'tensorflow_core\.python\.keras\.engine\.network\.Network\.([a-z]\w*)': r'tf.keras.Model#\1',
	r'tensorflow_core\.python\.keras\.engine\.network\.Network': r'tf.keras.Model',
	r'tensorflow_core\.python\.keras\.saving\.save\.([a-z]\w*)': r'tf.keras.models.\1',
	r'tensorflow\.python\.ops\.random_ops\.random_([a-z]\w*)': r'tf.random.\1',
	r'tensorflow\.python\.ops\.confusion_matrix\.confusion_matrix': r'tf.math.confusion_matrix',
	r'tensorflow\.python\.ops\.([a-z]\w*)_ops\.([a-z]\w*)_v\d': r'tf.\1.\2',
}


def map(qualifiedIdentifier, method):
	isProcessed = False
	for pattern, replace in ruledConversions.items():
		q, n = re.subn(pattern, replace, qualifiedIdentifier)
		if n > 0:
			isProcessed = True
			qualifiedIdentifier = q
			break
	if not isProcessed:
		qualifiedIdentifier = re.sub(r'^tensorflow(_core)?\.(python\.)?', 'tf.', qualifiedIdentifier)

		if qualifiedIdentifier.endswith('.' + method):
			namespace = qualifiedIdentifier[:len(qualifiedIdentifier) - len('.' + method)]
			namespace = fixNamespace(namespace)
			qualifiedIdentifier = namespace + method
			
	return qualifiedIdentifier
