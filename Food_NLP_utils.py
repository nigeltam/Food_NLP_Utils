import pycantonese as pyc
import requests

class Word_Segment_Tag:
    def __init__(self, plainText) -> None:
        # '我噚日買嗰對鞋。'
        self.plainText = plainText
        # ['我', '噚日', '買', '嗰', '對', '鞋', '。']
        self.wordList = pyc.segment(plainText)
        # [('我', 'PRON'), ('噚日', 'ADV'), ('買', 'VERB'), 
        # ('嗰', 'PRON'), ('對', 'NOUN'), ('鞋', 'NOUN'),
        # ('。', 'PUNCT')]
        self.wordListWithTags = pyc.pos_tag(self.wordList)

    def get_filtered_wordList(self, targetTag=None, targetLen=None) -> list:
        """Get a list of words under certain filtering.

        Args:
            targetTag (String, optional): Word tag to keep. Defaults to None.
                    ADJ: adjective
                    ADP: adposition
                    ADV: adverb
                    AUX: auxiliary
                    CCONJ: coordinating conjunction
                    DET: determiner
                    INTJ: interjection
                    NOUN: noun
                    NUM: numeral
                    PART: particle
                    PRON: pronoun
                    PROPN: proper noun
                    PUNCT: punctuation
                    SCONJ: subordinating conjunction
                    SYM: symbol
                    VERB: verb
                    X: other
            targetLen (int, optional): Minimun length of word. Defaults to None.

        Returns:
            list: List of target words.
        """
        tempList = self.wordListWithTags
        if targetTag is not None:
            tempList = [(word, tag) for word, tag in tempList if tag == targetTag]
        if targetLen is not None:
            tempList = [(word, tag) for word, tag in tempList if len(word) >= targetLen]
        return [word for word, _ in tempList]

# keywords related to Food
keywords = ['食', '飲', '菜']
def check_Wiki_API(word) -> bool:
    """Check Wiki to determine whether a word related to Food.

    Args:
        word (String): Word to check.

    Returns:
        bool: Word is related to Food or Not.
    """
    try:
        resultJson = requests.get(url=r"https://zh.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&redirects&titles=" + word).json()
    except:
        return None
    
    for keyword in keywords:
        if keyword in str(resultJson): return True
    return False

def database_add_topic(word, articleID) -> None:
    """
    Case 1:
    Word is Food - Append a record to ArticleTopic table
    """

    """
    Case 2:
    Word is Not Food - Pass
    """

    """
    Case 3:
    Word is Undetermined (Not exist in Topic table)
    Do a Wiki API check
    if check_Wiki_API() == True:
        add record {word, True} to Topic table
        add record {word, article ID} to ArticleTopic/CommentTopic
    elif check_Wiki_API() == False:
        add record {word, False} to Topic table
    else:
        ERROR
    """

    print(f"database_add_topic - {word} = {check_Wiki_API(word)}")

def all_in_one(articleID, plainText) -> None:
    """One-shot function to run for a new article"""
    wordList = Word_Segment_Tag(plainText).get_filtered_wordList(targetTag='NOUN', targetLen=2)
    # remove duplicated words
    wordList = list(set(wordList))
    for word in wordList:
        database_add_topic(word, articleID)

# test code
if __name__ == "__main__":
    plainText = "望住梅窩夜景，食住海鮮配啤酒簡直係享受。必試椒鹽九肚魚，口感滑捋捋，炸漿又夠鬆脆，點埋個喼汁真係食多多都無問題；避風塘炒蜆新鮮惹味。特別一提個乾炒牛河都好出色，乾身又夠鑊氣，最緊要係唔算油，牛肉份量又多，可以話係一碟出色嘅炒牛河！;、;行完山唔想食得太heavy，去呢間人氣麵包店食個包嘆杯咖啡都唔錯㗎。裝修好有外國風格，主打手工麵包，人氣自家製酸種麵包，酸種天然酵母發酵出嚟嘅麵包更有嚼勁，入面嘅合桃、杏脯同提子更添口感。提子玉桂麵包都值得一試，包身好軟熟，玉桂味突出而且唔會太甜，另外重有唔少蛋糕類質素都唔錯"
    all_in_one(1, plainText)
    """
    database_add_topic - 杏脯 = False
    database_add_topic - 椒鹽 = True
    database_add_topic - 提子 = True
    database_add_topic - 酵母 = True
    database_add_topic - 自家 = False
    database_add_topic - 啤酒 = True
    database_add_topic - 喼汁 = True
    database_add_topic - 咖啡 = True
    database_add_topic - 海鮮 = True
    database_add_topic - 玉桂 = True
    database_add_topic - 質素 = False
    database_add_topic - 出色 = False
    database_add_topic - 無問題 = False
    database_add_topic - 口感 = True
    database_add_topic - 麵包 = True
    database_add_topic - 外國 = False
    database_add_topic - 人氣 = False
    database_add_topic - 牛河 = True
    database_add_topic - 夜景 = False
    database_add_topic - 合桃 = True
    database_add_topic - 個包 = False
    database_add_topic - heavy = False
    database_add_topic - 牛肉 = True
    database_add_topic - 乾炒牛河 = True
    database_add_topic - 蛋糕 = True
    database_add_topic - 手工 = False
    database_add_topic - 惹味 = False
    database_add_topic - 份量 = False
    database_add_topic - 風格 = False
    """