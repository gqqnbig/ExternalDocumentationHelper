import os
import pytest
import sys

# import local packages
testFolder = os.path.dirname(os.path.abspath(__file__))
# print(f'testFolder={testFolder}')
sys.path.append(os.path.join(testFolder, '../../'))
# print(sys.path)
import ExternalDocumentationHelper.django.pythondoc.mapping as mapping

testData = [
	('tensorflow.python.ops.math_ops.argmax_v2', 'argmax_v2', 'tf.math.argmax'),
	('tensorflow.python.ops.nn_ops.softmax_v2', 'softmax_v2', 'tf.nn.softmax'),
	('tensorflow.python.ops.ragged.ragged_string_ops.unicode_split', 'unicode_split', 'tf.strings.unicode_split'),
	('tensorflow.python.data.ops.dataset_ops.DatasetV1.take', 'take', 'tf.data.Dataset#take'),
	('tensorflow.python.keras.preprocessing.text_dataset.text_dataset_from_directory', 'text_dataset_from_directory', 'tf.keras.preprocessing.text_dataset_from_directory'),
	('tensorflow.python.keras.Model.save', 'save', 'tf.keras.Model#save'),
	('tensorflow.python.ops.string_ops.regex_replace', 'regex_replace', 'tf.strings.regex_replace'),
	('tensorflow.python.feature_column.feature_column_v2.categorical_column_with_vocabulary_list','categorical_column_with_vocabulary_list', 'tf.feature_column.categorical_column_with_vocabulary_list')
]


@pytest.mark.parametrize('identifier, methodName, expected', testData)
def test_Mapping(identifier, methodName, expected):
	assert mapping.map(identifier, methodName) == expected
