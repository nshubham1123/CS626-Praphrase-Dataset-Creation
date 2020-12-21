"""
This file houses methods for creating positive paraphrase samples for 
Malayalam. Unlike Hindi, good parsers, Pos-taggers etc are not available
for Malayalam yet. So, some methods used for Hindi cannot be used here. 
Even though IndoWordnet provides synonym functionality, we cannot use 
tags to select the correct ones and so, that is also avoided since it 
created a lot of errors.
"""


import copy


class PositiveParaphrases:
  """This class houses the methods for creating paraphrases for a given
  sentence. Since we could not find usable open-source packages to find 
  synonyms or get parses for Malayalam, we decided to implement various
  rule-based approaches.
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
    return sent.strip(". ").split()

  def morphology_and_agglutination_based_paraphrasing(self, sent):
    """Malayalam is an agglutinative language. This means that words can get 
    clubbed together. But in Malayalam, it is also perfectly valid to write 
    these as separate words. For example: "that [I] saw" can be written as:
    " കണ്ടു എന്ന് ", " കണ്ടെന്നു " / " കണ്ടെന്ന് " or  " കണ്ടുവെന്ന് "
    Hence, such cases can be used as a rule-based approach to paraphrasing. 
    These rules (സന്ധി നിയമങ്ങൾ / Sandhi rules) exist in the language and can 
    be coded up. Here we use just one of these rules. Others can also be 
    included similarly.
    
    :param sent: sentence to be paraphrased
    :type sent: list of strings

    :return: list of paraphrases
    :rtype: list of strings
    """

    sentence = self._tokenize(sent)
    new_sentence = []
    success = False
    ignore = False
    n = len(sentence)

    for idx, word in enumerate(sentence):
      if word == "എന്നു" or word == "എന്ന്":
        if not ignore:
          ignore = False
          new_sentence.append(word)
        continue

      if idx < n - 1 and (sentence[idx + 1] == "എന്നു" or sentence[idx + 1] == "എന്ന്"):
        if word[-1] == "ു" or word[-1] == "്":
          y = word[:-1] + "െ"
          y += "ന്ന്"

          new_sentence.append(y)
          success = True
          ignore = True
        else:
          new_sentence.append(word)
      else:
        new_sentence.append(word)
    
    if success:
      return [" ".join(new_sentence)]
    else:
      return []
          

  def translate_pairs_to_paraphrases(self, sent1, sent2, l1, l2):
    """Take a pair of sentences in 2 languages l1 and l2. Then convert both 
    sentences into the target language using some pre-existing API. If they are 
    not identical, then they could be paraphrases.
    
    :param sent1: first sentence in pair
    :type sent: string

    :param sent2: second sentence in pair
    :type sent: string

    :param l1: language of first sentence in pair
    :type l1: string

    :param l2: language of second sentence in pair
    :type l2: string

    :return: list of paraphrases
    :rtype: list of strings
    """
    paraphrases = []
    try: 
      from textblob import TextBlob
      if l1 != "ml" and l1!= u"ml":
        x = TextBlob(sent1)
        trans1 = x.translate(to=u"ml").strip(". ")
      
      if l2 != "ml" and l2 != u"ml":
        x = TextBlob(sent2)
        trans2 = x.translate(to=u"ml").strip(". ")
      if trans1 != trans2:
        paraphrases = [str(trans1), str(trans2)]
      else:
        print("Both sentences translated into identical sentences. Unusable.\n")
    except:
      pass
    return paraphrases

  def back_translation(self, sent):
    """Automatic Back Translation can be used to create paraphrases. The 
    paraphrases may not always be correct because translators can make errors. 
    But like the other methods outlined, this can be used to create an auxiliary
    paraphrase dataset.
    
    :param sent: sentence to be paraphrased
    :type sent: list of strings

    :return: list of paraphrases
    :rtype: list of strings
    """
    paraphrases = []
    try: 
      from textblob import TextBlob
      
      x = TextBlob(sent)
      
      if "ml" != x.detect_language():
        print("Enter a Malayalam sentence.")
        return []
      
      temp = x.translate(to=u"en")
      y = temp.translate(to=u"ml")
      print((x, y))

      if x != y:
        paraphrases.append(str(y))
    except:
      pass
    return paraphrases

#   def synonym_substitution(self, sent):
#     """The pyiwn (https://github.com/riteshpanjwani/pyiwn) package can be used
#     to get synonyms for Malayalam words. The returned synonyms are accompanied 
#     with the post-tag of the source word for which that synonym works. But to 
#     make use of this feature, we need to know the pos-tag of the source word in
#     sentence (Malayalam). We could attempt to use TextBlob and some rules to 
#     hopefully achieve this for many sentences since there is no package 
#     available with a good coverage.
    
#     :param sent: sentence to be paraphrased
#     :type sent: list of strings

#     :return: list of paraphrases
#     :rtype: list of strings
#     """
#     pass
  
  def generate(self, sent):
    """Attempt to generate positive samples using all the implemented methods
    for single sentenceand return the aggregated list. 

    :param sent: sentence to get paraphrase samples for.
    :type sent: string

    :return: list of paraphrase samples.
    :rtype: list of strings
    """
    paraphrases = []

    # paraphrases += self.synonym_substitution(sent)
    paraphrases += morphology_and_agglutination_based_paraphrasing(sent)
    paraphrases += self.back_translation(sent)

    return list(set(paraphrases))  

  def generate_for_pair(self, sent1, sent2, l1, l2):
    """Attempt to generate positive samples using all the implemented methods 
    for pairs of sentences and return aggregated list.
    
    :param sent1: first sentence in pair
    :type sent: string

    :param sent2: second sentence in pair
    :type sent: string

    :param l1: language of first sentence in pair
    :type l1: string

    :param l2: language of second sentence in pair
    :type l2: string

    :return: list of paraphrases
    :rtype: list of strings
    """
    paraphrases = []

    paraphrases += self.translate_pairs_to_paraphrases(sent1, sent2, l1, l2)
