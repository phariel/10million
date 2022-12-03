from requests_html import HTMLSession
import random
import json
import os


class Lottery:

    def __init__(self) -> None:
        self.url = ""

    def getWebContent(self):
        session = HTMLSession()
        return session.get(self.url)

    def getParseResults(self):
        pass

    def getPredictedResults(self):
        pass


class BinaryColor(Lottery):

    def __init__(self) -> None:
        self.url = "https://datachart.500.com/ssq/history/newinc/history_same.php?num=100&sort=0"
        self.res = None

    def getParsedResults(self):
        content = self.getWebContent()
        blueNumbers = content.html.find('td.t_cfont2')
        blueBalls = []
        blueBallsItem = []
        blueBallsCount = blueNumbers.__len__()
        for i in range(0, blueBallsCount):
            blueBallsItem.append(blueNumbers[i].text)
            if (i + 1) % 6 == 0:
                blueBalls.append(blueBallsItem)
                blueBallsItem = []

        redNumbers = content.html.find('td.t_cfont4')
        redBalls = []
        for number in redNumbers:
            redBalls.append(number.text)
        return {'blueBalls': blueBalls, 'redBalls': redBalls}

    def getPredictedResults(self):
        if self.res == None:
            self.res = self.getParsedResults()
        parsedResult = self.res
        blueBallsResult = []

        while blueBallsResult.__len__() < 1:
            blueBalls = self.getRandomBlueBalls()
            isValid = True
            for i in parsedResult['blueBalls']:
                if set(blueBalls).intersection(i).__len__() > 2:
                    print("Not Valid")
                    print(i)
                    print("================")
                    isValid = False
                    break
            if isValid:
                blueBallsResult = blueBalls

        redBallResult = []
        while redBallResult.__len__() < 1:
            redBall = self.getRandomRedBalls()
            if set(redBall).intersection(
                    parsedResult['redBalls']).__len__() <= 10:
                redBallResult = redBall
        return {'red': blueBallsResult, 'blue': redBallResult}

    def getRandomBlueBalls(self):
        return sorted(random.sample(range(1, 34), 6))

    def getRandomRedBalls(self):
        return random.sample(range(1, 17), 1)


# def exec():
#     bc = BinaryColor()
#     print(bc.getPredictedResults())
#     print("=============================")

# def main(count=10):
#     print("========final result=========")
#     for i in range(0, count):
#         exec()


def getSmsCode():
    bc = BinaryColor()
    codeObj = bc.getPredictedResults()
    returnCode = '#'
    allList = codeObj['red'] + codeObj['blue']
    for ball in allList:
        returnCode += str.zfill(str(ball), 2)
    return returnCode


def getSmsText():
    res = 'a3362'
    for i in range(0, 5):
        res += getSmsCode()
    return res


def main():
    finalRes = {'ball1': getSmsText(), 'ball2': getSmsText()}
    file = open(os.path.join(os.path.dirname(__file__), 'ball.txt'), 'w')
    finalResText = json.dumps(finalRes)
    print(finalResText)
    file.write(finalResText)
    file.close()


main()