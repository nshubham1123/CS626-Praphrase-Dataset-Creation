"""
This file houses methods for creating negative paraphrase samples for 
Malayalam. Unlike Hindi, good parsers, Pos-taggers etc are not available
for Malayalam yet. So, some methods used for Hindi cannot be used here. 
Even though IndoWordnet provides synonym functionality, we cannot use 
tags to select the correct ones and so, that is also avoided since it 
created a lot of errors.
"""


import copy

class NegativeParaphrases:
  """This class houses the methods for creating sentence pairs that are not 
  paraphrases. Since we could not find usable open-source packages to find 
  synonyms or get parses for Malayalam, we decided to implement various
  rule-based approaches. Negative pairs can trivially be created by returning
  some unrelated sentence or a non-grammatical sentence. But we intend to 
  create grammatical sentences that share same context as the query sentence.
  """

  def __init__(self):
    """Constructor method.
    """
    pass

  def _tokenize(self, sent):
    """split sentence into words. Remove fullstop.
    
    :param sent: sentence to be tokenized
    :type sent: list of strings

    :return: list of words
    :rtype: list of strings
    """
    return sent.strip(". ").split(" ")

  def _generate_paraphrases(self, nsyn_set, sent, word, idx):
    """generates paraphrases by substituting word at given index with other
    words from given set. Only one word is substituted at a time.

    :param nsyn_set: set of non-synonyms
    :type nsyn_set: set of strings

    :param sent: tokenized sentence
    :type sent: list of strings

    :param word: word to be replaced
    :type word: string

    :param idx: index of word to be replaced in sentence
    :type idx: int

    :return: list of paraphrases
    :rtype: list of strings
    """
    paraphrases = []
    for w in nsyn_set:
      if w == word:
        continue
      
      paraphrases.append(sent[:idx] + [w] + sent[idx + 1:])
    return paraphrases

  def negate_if_last_word_is_is(self, sent):
    """If the last word of the sentence is 'ആണ്‌' (is), then the sentence can be
    negated by changing the last word to 'അല്ല' (isn't).

    :param sent: sentence to get negative paraphrase samples for.
    :type sent: string

    :return: list of negative paraphrase samples.
    :rtype: list of strings
    """
    sentence = self._tokenize(sent)

    if sentence[-1] == "ആണ്‌".strip("\u200c"):
      return [" ".join(sentence[:-1] + ["അല്ല".strip()])]
    return []

  def subst_with_non_synonyms(self, sent):
    """Create negative paraphrase samples by replacing a word with another word 
    from the set of non-synonyms.

    :param sent: sentence to get negative paraphrase samples for.
    :type sent: string

    :return: list of negative paraphrase samples.
    :rtype: list of strings
    """
    rule_set = [                 
                # pronound differences
                set(["നിങ്ങളെ", "എന്നെ", "അവനെ", "അവളെ", "അവരെ", "എല്ലാവരെയും", "ഞങ്ങളെ"]), # you, me, him, her, them, ...
                set(["ഞാൻ", "അവൻ", "അവൾ", "അവർ", "അയാൾ", "ഞങ്ങൾ", "നമ്മൾ"]), # I, he, she, they, he, we, we

                # time differences
                set(["മറ്റന്നാൾ", "നാളെ", "രാവിലെ", "രാത്രി", "അടുത്ത ആഴ്ച", "അടുത്ത മാസം", "അടുത്ത വര്ഷം"]), # day after tomorrow, tomorrow, morning, night, next week, next month, next year
                set(["ഇന്നലെ", "മിനിയാന്ന്", "കഴിഞ്ഞ ആഴ്ച", "കഴിഞ്ഞ മാസം", "കഴിഞ്ഞ വര്ഷം"]), # yesterday, day before yesterday, last week, last month, last year
    ]

    paraphrases = []
    sentence = self._tokenize(sent)

    for idx, word in enumerate(sentence):
      for s in rule_set:
        if word in s:
          paraphrases += self._generate_paraphrases(s, sentence, word, idx)
    
    return [" ".join(paraphrase) for paraphrase in paraphrases]

  def generate(self, sent):
    """Attempt to generate negative samples using all the implemented methods
    and return the aggregated list. 

    :param sent: sentence to get negative paraphrase samples for.
    :type sent: string

    :return: list of negative paraphrase samples.
    :rtype: list of strings
    """
    paraphrases = []

    paraphrases += self.subst_with_non_synonyms(sent)
    paraphrases += self.negate_if_last_word_is_is(sent)

    return list(set(paraphrases))