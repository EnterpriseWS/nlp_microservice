import spacy


def search_pii_by_entity(doc):
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            print("++ Found Name: " + ent.text)
        elif ent.label_ == 'DATE':
            print("++ Found Date: " + ent.text)