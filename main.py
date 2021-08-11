from requests_html import HTMLSession
import random


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
        parsedResult = self.getParsedResults()
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


def exec():
    bc = BinaryColor()
    print("========final result=========")
    print(bc.getPredictedResults())
    print("=============================")


def main(count=5):
    for i in range(0, count):
        exec()


main()