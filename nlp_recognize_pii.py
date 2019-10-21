import spacy
from spacy.matcher import Matcher

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

regex_ssn_hyphen = [{"TEXT": {"REGEX": "^(?!219-09-9999|078-05-1120)(?!666|000|9\d{2})\d{3}-(?!00)\d{2}-(?!0{4})\d{4}$"}}]
regex_ssn = [{"TEXT": {"REGEX": "^(?!219099999|078051120)(?!666|000|9\d{2})\d{3}(?!00)\d{2}(?!0{4})\d{4}$"}}]
regex_personal_id = [{"TEXT": {"REGEX": "^(?!999999999(\d{2}|\d)*)((([1-9]\d{8})([01]\d)*)|([rR]*\d{8}))$"}}]
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
matcher.add("SSN_Hyphen", None, regex_ssn_hyphen)
matcher.add("SSN", None, regex_ssn)
matcher.add("Personal_Id", None, regex_personal_id)


def find_pii(text):
    doc = nlp(text)
    matches = matcher(doc)
    print(text)
    if len(matches) == 0:
        print("No PII found")
    else:
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print("Found " + string_id + ": " + span.text)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        find_pii(sys.argv[1])
    else:
        print("Error: Please enter as 'py nlp_recognize_pii.py <text>'")
