import spacy
from spacy.matcher import Matcher
import re
import ent_pii_reco

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

regex_ssn_hyphen = r"(?!219-09-9999|078-05-1120)(?!666|000|9\d{2})\d{3}-(?!00)\d{2}-(?!0{4})\d{4}"
# TODO: Investigate why hyphen doesn't work for begin "^" and end "$"
# regex_ssn_hyphen = r"^(?!219-09-9999|078-05-1120)(?!666|000|9\d{2})\d{3}-(?!00)\d{2}-(?!0{4})\d{4}$"
regex_ssn = r"^(?!219099999|078051120)(?!666|000|9\d{2})\d{3}(?!00)\d{2}(?!0{4})\d{4}$"
regex_personal_id = r"^(?!999999999(\d{2}|\d)*)((([1-9]\d{8})([01]\d)*)|([rR]*\d{8}))$"
pattern_ssn_hyphen = [{"TEXT": {"REGEX": regex_ssn_hyphen}}]
pattern_ssn = [{"TEXT": {"REGEX": regex_ssn}}]
pattern_personal_id = [{"TEXT": {"REGEX": regex_personal_id}}]
ssn_hyphen_mid = r"SSN_Hyphen"
ssn_mid = r"SSN"
personal_id_mid = r"Personal_Id"

# ----------- Start NLP here -----------
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
matcher.add(ssn_hyphen_mid, None, pattern_ssn_hyphen)
matcher.add(ssn_mid, None, pattern_ssn)
matcher.add(personal_id_mid, None, pattern_personal_id)


def find_pii(text):
    is_ssn_hyphen_mid = False
    is_ssn_mid = False
    is_personal_id_mid = False
    doc = nlp(text)
    matches = matcher(doc)
    print("Token search for '" + text + "'...")
    if len(matches) == 0:
        print("No PII found in tokens")
    else:
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]
            if string_id == ssn_hyphen_mid:
                is_ssn_hyphen_mid = True
            elif string_id == ssn_mid:
                is_ssn_mid = True
            elif string_id == personal_id_mid:
                is_personal_id_mid = True
            span = doc[start:end]
            print("++ Found " + string_id + ": " + span.text)

    if not (is_ssn_hyphen_mid and is_ssn_mid and is_personal_id_mid):
        # No luck for one of tokens search, try full text
        print("Start full text search...")
        if not is_ssn_hyphen_mid:
            search_pii_in_text(ssn_hyphen_mid, doc)
        if not is_ssn_mid:
            search_pii_in_text(ssn_mid, doc)
        if not is_personal_id_mid:
            search_pii_in_text(personal_id_mid, doc)

    print("Start entity search...")
    ent_pii_reco.search_pii_by_entity(doc)


def search_pii_in_text(string_id, doc):
    expression = ""
    if string_id == ssn_hyphen_mid:
        expression = regex_ssn_hyphen
    elif string_id == ssn_mid:
        expression = regex_ssn
    elif string_id == personal_id_mid:
        expression = regex_personal_id
    # print("Search By Text = " + doc.text)
    # print("Search By Regex = " + expression)
    for match in re.finditer(expression, doc.text):
        start, end = match.span()
        span = doc.char_span(start, end)
        if span is not None:
            print("++ Found " + string_id + ": " + span.text)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        find_pii(sys.argv[1])
    else:
        print("Error: Please enter as 'py nlp_pii_reco.py <text>'")
