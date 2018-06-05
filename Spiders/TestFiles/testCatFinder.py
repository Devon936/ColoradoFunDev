from google.cloud import language_v1beta2
from google.cloud.language_v1beta2 import enums
from google.cloud.language_v1beta2 import types

language_client = language_v1beta2.LanguageServiceClient()

document = types.Document(
    content='''
    Rafael Montero Shines in Mets Victory Over the Reds. Montero, who was demoted at midseason, took
     a one-hitter into the ninth inning as the Mets continued to dominate Cincinnati with a win at 
     Great American Ball Park.''',
    type=enums.Document.Type.PLAIN_TEXT
)

result = language_client.classify_text(document)

for category in result.categories:
    print('category name: ', category.name)
    print('category confidence: ', category.confidence, '\n')