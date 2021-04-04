import os
import pytest
import sys

# import local packages
testFolder = os.path.dirname(os.path.abspath(__file__))
# print(f'testFolder={testFolder}')
sys.path.append(os.path.join(testFolder, '../../'))
# print(sys.path)
import ExternalDocumentationHelper.django.pythondoc.mapping as mapping


def test_Mapping():
	assert mapping.map('tensorflow.python.keras.preprocessing.text_dataset.text_dataset_from_directory', 'text_dataset_from_directory') == 'tf.keras.preprocessing.text_dataset_from_directory'
