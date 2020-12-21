import stanfordnlp
stanfordnlp.download('hi')

class Negative_Paraphrases:
  """This class generates negative paraphrase for input sentence using 2 methods:
    1. proper_noun_swap()
    2. negation_by_compound()
  """

  def __init__(self):
    """Constructor method.
    """
    self.nlp = stanfordnlp.Pipeline(lang='hi',processors="tokenize,pos,depparse")

  def get_tagged_sent(self,text):
    """ function to do POS tagging of sentence by tokenizing it into words
        return list of words with corresponding POS tag

    :param text: string of words to be tagged
    :type text: string

    :return: list of tuples of form (word,tag)
    :rtype: list of tuples
    """
    tagged_sent=[]
    doc = self.nlp(text)
    for sent in doc.sentences:
      for word in sent.words:
        tagged_sent.append([word.text , word.pos])
    return tagged_sent

  def get_dep_tree(self,text):
    """ function to do dependency parsing of sentence

    :param text: sentence to be parsed
    :type text: string of words

    :return: list of tuples of form (parent word , dependency relation , current word)
    :rtype: list of tuples
    """

    doc = self.nlp(text)
    return doc.sentences[0].dependencies

  def proper_noun_swap(self,text):
    """ function which returns negative paraphrase of given sentence , by swapping Proper Nouns (NNP)

    :param text: sentence to be paraphrased
    :type text: string 

    :return: negative paraphrased sentence
    :rtype: string
    """

    tagged_sent = self.get_tagged_sent(text)
    first_NNP_found = 0
    first_NNP_index = None
    swapping = 0
    for i,(word,tag) in enumerate(tagged_sent):
      if tag=='NNP':
        if first_NNP_found == 0:
          first_NNP_found = 1
          first_NNP_index = i
        else:
          first_NNP = tagged_sent[first_NNP_index][0]
          tagged_sent[first_NNP_index][0] = word
          tagged_sent[i][0] = first_NNP
          swapping=1
          break
    if swapping==0:
      return None
    return ' '.join([word[0] for word in tagged_sent])


  def negation_by_compound(self,text):
    """ function which returns negative paraphrase of given sentence , by swapping Proper Nouns (NNP)

    :param text: sentence to be paraphrased
    :type text: string 

    :return: negative paraphrased sentence
    :rtype: string
    """
    dep_tree = self.get_dep_tree(text)
    negation=[]
    neg_done=0
    for i,tup in enumerate(dep_tree):
      negation.append(tup[2].text)
      if tup[2].upos=='NOUN' and tup[1]=='compound' and neg_done==0 and dep_tree[i+1][2].upos=='VERB':
        negation.append('नही')
        neg_done=1
    if neg_done==0:
      return None
    return ' '.join(negation)


