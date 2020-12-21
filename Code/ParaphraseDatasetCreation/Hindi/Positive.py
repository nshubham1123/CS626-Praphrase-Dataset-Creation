import stanfordnlp
stanfordnlp.download('hi')

import pyiwn
pyiwn.download()


class Positive_Paraphrases:
  """ This class generated positive paraphrases using 2 methods:
    1. get_paraphrase_by_synonym_change
    2. get_paraphrase_by_change_conj
  """
  def __init__(self):
    """Constructor method.
    """
    self.nlp = stanfordnlp.Pipeline(lang='hi',processors="tokenize,pos,depparse")
    self.iwn = pyiwn.IndoWordNet(lang=pyiwn.Language.HINDI)
  
  def find_pos_tag(self,tag):
    """  it return POS tag on which synset is searched , we are only replacing Noun , Verb and Adjective

    :param tag: POS tag
    :type tag: string

    :return: pyiwn object of POS tag
    :rtype: string
    """

    if tag.startswith('NN'):
      return pyiwn.PosTag.NOUN
    if tag.startswith('V'):
      return pyiwn.PosTag.VERB
    if tag.startswith('JJ'):
      return pyiwn.PosTag.ADJECTIVE
    return None


  def get_synonyms(self,word,tag):
    """  return list of all synonyms for given word according to given POS tag

    :param word: word for which synonyms to be returned
    :type word: string
    :param tag: POS tag for given word
    :type tag: string

    :return: list of synonyms of given word
    :rtype: list
    """

    synonyms=[]
    # vocabulary of hindi words
    vocab = self.iwn.all_words()
    # searching for synset of particular word is based on its POS tag
    pos_tag= self.find_pos_tag(tag)
    if pos_tag != None and word in vocab:
      #print('yes' , word)
      for syn in self.iwn.synsets(word,pos=pos_tag):
        for l in syn.lemmas(): 
          #print(l.name())
          synonyms.append(l.name())
    return synonyms

  
  def get_synonym(self,synonyms ,word):
    """input is word and list of its synonyms , return synonym which is different from current word
    since list of synonyms also contain same word.

    :param synonyms: list of synonyms for given word
    :type synonyms: list

    :param word: word for which synonyms to be returned
    :type word: string

    :return: synonym of given word
    :rtype: string
    """

    for synonym in synonyms:
      if word != synonym:
        #print(synonym)
        return synonym
    return word


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

  def get_paraphrase_by_synonym(self,text):
    """ function which returns paraphrase of given sentence , by synonyms substitution
    it replaces each word with its Synonyms , Proper Nouns are not replaced

    :param text: sentence to be paraphrased
    :type text: string 

    :return: paraphrased sentence by synonym substitution
    :rtype: string
    """

    tagged_sent = self.get_tagged_sent(text)
    #print(tagged_sent)
    paraphrase=''

    for i,(word,tag) in enumerate(tagged_sent):
      synonyms = self.get_synonyms(word,tag)
      # check whether list of synonyms is empty and current word is not proper noun
      if synonyms!=None and (len(synonyms)>0) and tag!='NNP':
        paraphrase+=self.get_synonym(synonyms,word)
      else:
        paraphrase+=word
      paraphrase+=' '

    return paraphrase

  def get_dep_tree(self,text):
    """ function to do dependency parsing of sentence

    :param text: sentence to be parsed
    :type text: string of words

    :return: list of tuples of form (parent word , dependency relation , current word)
    :rtype: list of tuples
    """

    doc = self.nlp(text)
    return doc.sentences[0].dependencies

  def get_paraphrase_by_change_conj(self,text):

    """ function which returns negative paraphrase of given sentence , by changing order of conjunctions
        dependency tuple format: (word_parent<index,text> , dep_relation , word_child<index,text> )
        conj_indx will store indexes of all words modifed as conj (i.e. I like a , b and c) ,so contain index of a , b ,c


    :param text: sentence to be paraphrased
    :type text: string 

    :return: paraphrased sentence by changing order of conjunctions
    :rtype: string
    """

    dep_tree = self.get_dep_tree(text)
    paraphrase=[]
  
    conj_indx=set()

    for i,tup in enumerate(dep_tree):
    
      if(tup[1]=='conj'):
        conj_indx.add(i)
        # storing index of parent also.
        conj_indx.add(int(tup[0].index)-1)
      paraphrase.append(tup[2].text)

    conj_index = sorted(conj_indx)
    # if no conj relationship found then return
    if(len(conj_index)<=1):
      return None
    # shifitng positions of all conj words anticlock-wise by 1 , so first/start word goes at last
    start_word=paraphrase[conj_index[0]]
    for i in range(1,len(conj_index)):
      paraphrase[conj_index[i-1]]=paraphrase[conj_index[i]]
    paraphrase[conj_index[-1]]=start_word

    return ' '.join(paraphrase)

