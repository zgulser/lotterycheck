from django.forms import formset_factory
from django.shortcuts import render, redirect
from submits import forms, utils
from submits.models import Lottery, LotteryPlayer
from django.http import HttpResponse
import time
import submits.javascript

# global/stub variable to check thread start
started = False

# Create a timer thread

import threading
class SubThread(threading.Thread):

    def __init__(self, pThreadId, pThreadName, lottery):
        threading.Thread.__init__(self)
        self.threadName = pThreadName
        self.count = 0
        self.lottery = lottery
        started = True

    def run(self):
        remaining = utils.LotteryUtils.getRemainingTimeInSecs(self.lottery)
        while remaining > 0:
            print (">> Log.Verbose: Remaning secs: %s" %(remaining))
            time.sleep(1)
            remaining = utils.LotteryUtils.getRemainingTimeInSecs(self.lottery)
        print (">> Log.Verbose: Lottery ended!")
        utils.LotteryUtils.updateLotteryModelAsExpired(self.lottery.token)
        utils.LotteryUtils.calculateWinner(self.lottery.token)

# Create your views here.

#
# play lottery form view function
# M prefix to identify it as Mdel data
#
def playlottery(request):
    try:
        # grab the lottery object, create one if necessary
        lotteryM = utils.LotteryUtils.createLotteryObj()

        # check lottery has expired or not
        if not utils.LotteryUtils.isLotteryExpired(lotteryM):
            print (">> Log.Verbose: Updater thread has created!")
            thread1 = SubThread(1, 'Thread-updater', lotteryM)
            thread1.start()

        # do the form stuff here
        playerFormSet = formset_factory(forms.LotteryPlayerForm)
        if request.method == "POST":
            formset = playerFormSet(request.POST, request.FILES)
            if formset.is_valid(): # handles id-based uniqueness validation
                # process form data
                for form in formset:
                    playerM = form.save()
                    utils.LotteryUtils.isLotteryPlayerExists(playerM)
                    request.session['player'] = playerM
                    request.session['lottery'] = lotteryM
                    # we may have used render as well to initiate the confirmation
                    # in the same view.
                    return redirect('confirmation/')
            else:
                for form in formset:
                    return redirect('playerexists/')
        else:
            formset = playerFormSet()

        if utils.LotteryUtils.isLotteryExpired(lotteryM):
            print (">> Log.Verbose: Lottery expired - redirecting to Results page")
            request.session['lottery'] = lotteryM
            return redirect('winner/')
        else:
            lotterydeadline = utils.LotteryUtils.getLotteryDeadlineDate(lotteryM.created_at, lotteryM.duration)
            lotterydeadlineformatted = utils.LotteryUtils.getLotteryDeadlineDateAsFormatted(lotteryM.created_at, lotteryM.duration)
            print (">> Log.verbose lottery deadline date @: %s" %(lotterydeadline))
            return render(request, 'play_lottery_form.html', {'formset': formset,
                                                              'lotterydeadline':lotterydeadline,
                                                              'lotterydeadlineformatted':lotterydeadlineformatted})
    except:
        print (">> Log.Error: Exception @playlottery")

#
# confirmation form view function
# R prefix to identify it as Request data
#
def confirmation(request):
    try:
        playerR = request.session.get('player', None)
        lotteryR = request.session.get('lottery', None)
        return render(request, 'play_status_success_form.html', {'player': playerR, 'lottery': lotteryR})
    except:
        print (">> Log.Error: Exception @confirmation")

def playerexists(request):
    try:
        playerR = request.session.get('player', None)
        lotteryR = request.session.get('lottery', None)
        return render(request, 'player_exists_form.html', {'player': playerR, 'lottery':lotteryR})
    except:
        print (">> Log.Error: Exception @playerexists")

#
# result form view function
#
def winner(request):
    try:
        lotteryR = request.session.get('lottery', None)
        print(">> Log.verbose winning row is: %s" %(lotteryR.winner_row))
        query_results = LotteryPlayer.objects.all()
        #winnerrow = utils.LotteryUtils.getWinnerRow(lotteryR.token)
        return render(request, "winner_form.html", {"query_results": query_results, 'winnerrow': 1})
    except:
        print (">> Log.Error: Exception @winner")
