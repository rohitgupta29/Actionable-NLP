import config
import os
import json
from expertai.nlapi.cloud.client import ExpertAiClient
client = ExpertAiClient()


os.environ["EAI_USERNAME"] = config.expertai_mail
os.environ["EAI_PASSWORD"] = config.expertai_password


def sentiment(text):
    """returns overall sentiment"""
    output = client.specific_resource_analysis(body = {"document":{"text": text}},
                                               params = {'language': 'en','resource': 'sentiment'})
    return output.sentiment.overall

def named_entity_extraction(text):
    """extract named entities"""
    output = client.specific_resource_analysis(body={"document": {"text": text}},
                                               params={'language': 'en', 'resource': 'entities'})
    return [entity.lemma for entity in output.entities]

def key_phrase_extraction(text):
    """extract key phrases"""
    output = client.specific_resource_analysis(body={"document": {"text": text}},
                                               params={'language': 'en', 'resource': 'relevants'})
    return [lemma.value for lemma in output.main_lemmas]


def resource_concept_score_analysis(text):
    """extract concept and provide the score"""
    document = client.specific_resource_analysis(
        body={"document": {"text": text}},
        params={'language': "en", 'resource': 'relevants'})
    # print(f'{"CONCEPT":{20}} {"SCORE":{5}} \n')
    return [f'{main_concept.lemma:{2}}: {main_concept.score:{1}}' for main_concept in document.main_syncons]


def deep_linguistic_analysis(text):
    """returns POS for words in the text"""
    output = client.specific_resource_analysis(
        body={"document": {"text": text}},
        params={'language': 'en', 'resource': 'disambiguation'
                })
    # print(f'{"TEXT":{20}} {"LEMMA":{40}} {"POS":{6}}')
    # print(f'{"----":{20}} {"-----":{40}} {"---":{6}}')
    # return [f'{text[token.start:token.end]:{20}} {token.lemma:{40}} {token.pos:{6}}' for token in output.tokens]
    return [f'{text[token.start:token.end]} {token.lemma} {token.pos}' for token in output.tokens]


def document_classification(text):
    taxonomy = 'iptc'
    document = client.classification(
        body={"document": {"text": text}},
        params={'taxonomy': taxonomy, 'language': 'en'})
    # print(f'{"CATEGORY":{47}} {"IPTC ID":{10}} {"FREQUENCY":{8}}\n')
    return [f'{category.label:{47}} {category.id_:{10}}{category.frequency:{8}}' for category in document.categories]

# Check if a single function can be made for behavioural traits and document classification.
def behavioural_traits(text):
    taxonomy ='behavioral-traits'
    output = client.classification(
        body={"document": {"text": text}},
        params={'taxonomy': taxonomy, 'language': 'en'})
    print("list of categories")
    list = []
    for category in output.categories:
        list.append({"category.id_":category.id_,"category.hierarchy":category.hierarchy})
    return list
    # return [[category.id_,category.hierarchy]for category in output.categories]


def information_detection(text):
    """ add details """
    detector = 'pii'
    output = client.detection(
        body={"document": {"text": text}},
        params={"detector": detector, 'language': 'en'})
    return "extra_data: " + json.dumps(output.extra_data, indent=4, sort_keys = True)



def relation_extraction(text):
    """shows the relations in the text given"""
    output = client.specific_resource_analysis(
        body={"document": {"text": text}},
        params={'language': "en", 'resource': 'relations'})
    print("Output relations' data:")
    output_relations = []
    for relation in output.relations:
        print(relation.verb.lemma, ":");
        for related in relation.related:
            print("\t", "(", related.relation, ")", related.lemma);
    #add return statement

def full_document_analysis(text):
    """ add details"""
    output = client.full_analysis(
        body={"document": {"text": text}},
        params={'language': "en"})
    try:
        print("knowledge: ", len(output.knowledge))
        print("paragraphs: ", len(output.paragraphs))
        print("sentences: ", len(output.sentences))
        print("phrases: ", len(output.phrases))
        print("tokens: ", len(output.tokens))
        print("mainSentences: ", len(output.main_sentences))
        print("mainPhrases: ", len(output.main_phrases))
        print("mainLemmas: ", len(output.main_lemmas))
        print("mainSyncons: ", len(output.main_syncons))
        print("topics: ", len(output.topics))
        print("entities: ", len(output.entities))
        print("relations: ", len(output.relations))
        print("sentiment.items: ", len(output.sentiment.items))
        return 1
    except Exception as e:
        return 0



# 
# if __name__ == '__main__':
# 
#     t = "This is not a great present"
#     # print(sentiment(t))
#     # print(named_entity_extraction(t))
#     # print(key_phrase_extraction(t))
#     # print(document_classification(t))
#     # print(deep_linguistic_analysis(t))
#     # print(relation_extraction(t))
#     # print(full_document_analysis(t))
#     # print(information_detection(t))
#     # print(resource_concept_score_analysis(t))
#     # print(behavioural_traits(t))
