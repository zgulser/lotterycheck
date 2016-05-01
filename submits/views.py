from django.forms import formset_factory
from django.shortcuts import render, redirect
from submits import forms, utils
from submits.models import Lottery, LotteryPlayer
from django.http import HttpResponse
import time
import submits.javascript

# Create a timer thread

import threading
class SubThread(threading.Thread):

    def __init__(self, pThreadId, pThreadName, lottery):
        threading.Thread.__init__(self)
        self.threadName = pThreadName
        self.count = 0
        self.lottery = lottery

    def run(self):
        remaining = utils.LotteryUtils.getRemainingTimeInSecs(self.lottery)
        while remaining > 0:
            print (">> Log.Verbose: Remaning time i thread: %s" %(utils.LotteryUtils.getRemainingTimeFormatted(self.lottery)))
            time.sleep(1)
            # TODO: update view(s)
        utils.LotteryUtils.updateLotteryModelAsExpired(self.lottery.token)
        utils.LotteryUtils.calculateWinner(self.lottery.token)

# Create your views here.

#
# play lottery form view function
# M prefix to identify it as Mdel data
#
started = False
def playlottery(request):
    try:
        # grab the lottery object, create one if necessary
        lotteryM = utils.LotteryUtils.createLotteryObj()
        print (">> Log.verbose lottery deadline date @: %s" %(utils.LotteryUtils.getLotteryDeadlineDate(lotteryM.created_at, lotteryM.duration)))

        if started == False:
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
            #queryset = LotteryPlayer.objects.all()
            #winnerrow = utils.LotteryUtils.getWinnerRow(lotteryM.token)
            #return render("winner_form.html", {"queryset": queryset, 'winner': winnerrow})
            pass
        else:
            formattedRemaningTime = utils.LotteryUtils.getRemainingTimeFormatted(lotteryM)
            return render(request, 'play_lottery_form.html', {'formset': formset, 'lottery':formattedRemaningTime})
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
        print(">> Log.verbose player name is: %s" %(playerR.firstname))
        return render(request, 'play_status_success_form.html', {'player': playerR, 'lottery': lotteryR})
        #queryset = LotteryPlayer.objects.all()
        #winnerrow = utils.LotteryUtils.getWinnerRow(lotteryR.token)
        #return render("winner_form.html", {"queryset": queryset, 'winner': winnerrow})
    except:
        print (">> Log.Error: Exception @confirmation")

def playerexists(request):
    try:
        playerR = request.session.get('player', None)
        lotteryR = request.session.get('lottery', None)
        return render(request, 'player_exists_form.html', {'player': playerR, 'lottery':lotteryR})
        pass
    except:
        print (">> Log.Error: Exception @playerexists")

#
# result form view function
#
def winner(request):
    return HttpResponse("Hello, world. You're at the lottery result.")

def backToPlayerForm():
    return redirect('playlottery/')