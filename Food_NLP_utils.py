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
        tempList = self.wordListWithTags
        if targetTag is not None:
            tempList = [word for word, tag in tempList if tag == targetTag]
        else:
            tempList = [word for word, tag in tempList]
        if targetLen is not None:
            tempList = [word for word in tempList if len(word) >= targetLen]
        return tempList

keywords = ['食', '飲']

def check_Wiki_API(word) -> bool:
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
    print(f"database_add_topic - {word}")

def all_in_one(articleID, plainText) -> None:
    """One shot programe to run when a new article scraped"""
    wordList = Word_Segment_Tag(plainText).get_filtered_wordList(targetTag='NOUN', targetLen=2)
    # remove duplicated words
    wordList = list(set(wordList))
    for word in wordList:
        database_add_topic(word, articleID)

# test code
if __name__ == "__main__":
    plainText = "望住梅窩夜景，食住海鮮配啤酒簡直係享受。必試椒鹽九肚魚，口感滑捋捋，炸漿又夠鬆脆，點埋個喼汁真係食多多都無問題；避風塘炒蜆新鮮惹味。特別一提個乾炒牛河都好出色，乾身又夠鑊氣，最緊要係唔算油，牛肉份量又多，可以話係一碟出色嘅炒牛河！;、;行完山唔想食得太heavy，去呢間人氣麵包店食個包嘆杯咖啡都唔錯㗎。裝修好有外國風格，主打手工麵包，人氣自家製酸種麵包，酸種天然酵母發酵出嚟嘅麵包更有嚼勁，入面嘅合桃、杏脯同提子更添口感。提子玉桂麵包都值得一試，包身好軟熟，玉桂味突出而且唔會太甜，另外重有唔少蛋糕類質素都唔錯"
    all_in_one(1, plainText)