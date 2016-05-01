from datetime import datetime
import time, random
from django.utils.timezone import localtime, now
from submits.models import Lottery, LotteryPlayer
import pytz

class DateUtils:

    @staticmethod
    def getFormattedCountdownTime(timestamp):
        return "TODO"

class LotteryUtils:

    @staticmethod
    def isLotteryPlayerExistsByID(id):
        exists = LotteryPlayer.objects.filter(identity=id).exists()
        return exists

    @staticmethod
    def createLotteryObj():
        lotteryObj = Lottery.objects.first()
        if lotteryObj == None:
            Lottery.objects.create()
            lotteryObj = Lottery.objects.first()

        return lotteryObj

    @staticmethod
    def isLotteryPlayerExists(lotteryplayer):
        id = lotteryplayer.identity
        exists = LotteryPlayer.objects.filter(identity=id).exists()
        print (">> Log.verbose lottery player with %s exists: %s" %(lotteryplayer.firstname, exists))

    @staticmethod
    def getLotteryCreatedTime(lottery):
        epoch = int(time.mktime(lottery.created_at.timetuple())*1000)
        return epoch


    @staticmethod
    def getLotteryDeadlineDate(created, durationP):
        epoch = int(time.mktime(created.timetuple())*1000)
        duration = durationP*60*1000
        deadline_ts = epoch - duration
        deadline_date = datetime.fromtimestamp(deadline_ts/1000)
        return deadline_date

    @staticmethod
    def getNow():
        current = datetime.now()
        epoch = int(time.mktime(current.timetuple())*1000)
        return epoch

    @staticmethod
    def getRemainingTimeInSecs(lottery):
        d1 = lottery.created_at
        d2 = datetime.now()
        passedsecs = (d2-d1).seconds
        remaning = lottery.duration*60 - passedsecs # cache it instead calculation each time
        return remaning

    @staticmethod
    def getRemainingTimeFormatted(lottery):
        remaining = LotteryUtils.getRemainingTimeInSecs(lottery)
        return time.strftime('%H:%M:%S', time.gmtime(remaining))
        pass

    @staticmethod
    def isLotteryExpired(lottery):
        token = lottery.token
        exists = Lottery.objects.filter(token=token).exists()
        if exists:
            return lottery.expired
        return False

    @staticmethod
    def updateLotteryModelAsExpired(ptoken):
        print (">> Log.Verbose: Updating lottery expiration...")
        Lottery.objects.filter(token=ptoken).update(expired=True) # save might have been used as well on the lot object

    @staticmethod
    def updateLotteryModelWinner(ptoken, row):
        print (">> Log.Verbose: Updating lottery winner column...")
        Lottery.objects.filter(token=ptoken).update(winner_row=row) # save might have been used as well on the lot object

    @staticmethod
    def calculateWinner(ptoken):
        count = Lottery.objects.count()
        winner = random.randint(0, count)
        LotteryUtils.updateLotteryModelWinner(ptoken, winner)

    @staticmethod
    def getWinnerRow(ptoken):
        lottery = Lottery.objects.filter(token=ptoken)
        return lottery.winner_row


