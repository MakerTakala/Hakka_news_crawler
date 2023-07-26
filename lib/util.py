import re
import string
import zhon

def cleartext(text):
    text = re.sub(r"\s+", "", text)
    text = re.sub("\(.*?\)","", text)
    text = re.sub("[" + string.punctuation + "]", "", text)
    text = re.sub("[" + zhon.hanzi.punctuation + "]", "", text)
    return text


def is_space(text):
    if text == "" or len(text) < 3: 
        return True
    if text.count("計") > 2 or text.count("于") > 2:
        return True
    for c in text:
        if text.count(c) > 3:
            return True
    return False


def text_is_differ(s1, s2):
    n1 = len(s1)
    n2 = len(s2)

    dp = [[None] * (n2 + 1) for i in range(n1 + 1)]

    for i in range(n1 + 1):
        for j in range(n2 + 1):
            if i == 0 or j == 0 :
                dp[i][j] = 0
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    return dp[n1][n2] < n1 - 5