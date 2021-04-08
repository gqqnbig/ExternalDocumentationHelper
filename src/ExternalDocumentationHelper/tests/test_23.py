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
	('tensorflow.python.data.ops.dataset_ops.DatasetV1.take', 'take', 'tf.data.Dataset#take'),
	('tensorflow.python.keras.preprocessing.text_dataset.text_dataset_from_directory', 'text_dataset_from_directory', 'tf.keras.preprocessing.text_dataset_from_directory'),
	('tensorflow.python.keras.Model.save', 'save', 'tf.keras.Model#save'),
	('tensorflow.python.ops.string_ops.regex_replace', 'regex_replace', 'tf.strings.regex_replace'),
]


@pytest.mark.parametrize('identifier, methodName, expected', testData)
def test_Mapping(identifier, methodName, expected):
	assert mapping.map(identifier, methodName) == expected
