import spacy
from spacy.pipeline import merge_entities
from spacy import displacy
import spacy
import re
import spacy
from spacy.matcher import Matcher

# ============== SSN without hyphen ============
# re.match(r'^(?!000|.+0{4})(?:\d{9}|\d{3}-\d{2}-\d{4})$'
# Simplest form: ^(?!(000|666|9))\d{3}-(?!00)\d{2}-(?!0000)\d{4}$
# With hyphen: ^(?!219-09-9999|078-05-1120)(?!666|000|9\d{2})\d{3}-(?!00)\d{2}-(?!0{4})\d{4}$
# W/o hyphen: ^(?!219099999|078051120)(?!666|000|9\d{2})\d{3}(?!00)\d{2}(?!0{4})\d{4}$
# ============== member ID =====================
# Include FEP: ^(?!999999999(\d{2}|\d)*)((([1-9]\d{8})([01]\d)*)|([rR]*\d{8}))$
# ============== Phone number matching ==============
# Regex: ((\(\d{3}\)?)|(\d{3}))([\s-./]?)(\d{3})([\s-./]?)(\d{4})
# Below is training-based
# --------------------------
# nlp = spacy.load("en_core_web_sm")
# matcher = Matcher(nlp.vocab)
# pattern = [{"ORTH": "("}, {"SHAPE": "ddd"}, {"ORTH": ")"}, {"SHAPE": "ddd"},
#            {"ORTH": "-", "OP": "?"}, {"SHAPE": "ddd"}]
# matcher.add("PHONE_NUMBER", None, pattern)
# doc = nlp("Call me at (123) 456 789 or (123) 456 789!")
# print([t.text for t in doc])
# matches = matcher(doc)
# for match_id, start, end in matches:
#     span = doc[start:end]
#     print(span.text)
# --------------------------

# ============== Regex matching ==============
nlp = spacy.load("en_core_web_sm")
doc = nlp("The United States of America (USA) are commonly known as the United States (U.S. or US) or America.")

expression = r"[Uu](nited|\.?) ?[Ss](tates|\.?)"
for match in re.finditer(expression, doc.text):
    start, end = match.span()
    span = doc.char_span(start, end)
    # This is a Span object or None if match doesn't map to valid token sequence
    if span is not None:
        print("Found match:", span.text)

# pattern = [{"TEXT": {"REGEX": "^[Uu](\.?|nited)$"}},
#            {"TEXT": {"REGEX": "^[Ss](\.?|tates)$"}},
#            {"LOWER": "president"}]

# ============== Multi-rule example =============
nlp = spacy.load("en_core_web_sm")


def extract_person_orgs(doc):
    person_entities = [ent for ent in doc.ents if ent.label_ == "PERSON"]
    for ent in person_entities:
        head = ent.root.head
        if head.lemma_ == "work":
            preps = [token for token in head.children if token.dep_ == "prep"]
            for prep in preps:
                orgs = [token for token in prep.children if token.ent_type_ == "ORG"]
                print({'person': ent, 'orgs': orgs, 'past': head.tag_ == "VBD"})
    return doc


# To make the entities easier to work with, we'll merge them into single tokens
nlp.add_pipe(merge_entities)
nlp.add_pipe(extract_person_orgs)

doc = nlp("Alex Smith worked at Acme Corp Inc.")
# If you're not in a Jupyter / IPython environment, use displacy.serve
displacy.render(doc, options={'fine_grained': True})

if __name__ == '__main__':
    i = 1
    # Do nothing yet
