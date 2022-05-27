from django.shortcuts import redirect, render
from .models import Bid, BidEntry
from crop.models import Crop
from account.models import UserProfile
import datetime
from django.http import HttpResponse
from django.contrib import messages



def create_bid(request, id):
    print("Hello")
    crop = Crop.objects.get(id=id)
    b_end = request.POST['last_date']
    b_start = datetime.date.today()
    active = True
    b_price = request.POST['base_price']
    
    crop_bid = Bid()
    crop_bid.bid_start_date = b_start
    crop_bid.bid_close_date = b_end = b_end
    crop_bid.base_price = b_price
    crop_bid.is_Active = active
    crop_bid.bid_for_crop = crop
    crop_bid.save()

    return redirect('individual_crop', crop.id)


def place_bid(request):
    print('hello world')
    amount = request.POST['amount']
    user = request.user
    user_prof = UserProfile.objects.get(user = user)
    crop = request.POST['crop']
    date = datetime.datetime.now()
    crop_info = Crop.objects.get(id = crop)
    bid = Bid.objects.get(bid_for_crop = crop_info)

    new_bid = BidEntry()
    new_bid.bid = bid
    new_bid.merchant_bidding = user_prof
    new_bid.bid_price = amount
    new_bid.bid_time = date

    new_bid.save()
    print("new", new_bid)
    return redirect('individual_crop' , crop_info.id)

def active_bids(request):
    #all_active_bids = []
    date_today = datetime.datetime.today()
    print(date_today)
    
    """ all_bids = Bid.objects.all()    
    print("all bids obj", all_bids)
    for b in all_bids:
        is_act = b.is_bid_active
        print("b is",is_act)
        if is_act == True:
            all_active_bids.append(b)
    print("all bids list", all_active_bids)
    data = {'all_active_bids': all_active_bids}
    print("data", data)
    return render(request, 'bidding/active_bids.html', data) """

    all_bids = Bid.objects.filter(bid_close_date__gte = date_today)
    if all_bids.count() == 0:
        
        messages.info(request, "No active bids now")
       
        a_url = request.META.get('HTTP_REFERER')
       
        return redirect(a_url)
    
    return render(request, 'bidding/active_bids.html', { "all_bids": all_bids }) 
    

def view_bids(request):
    user = request.user
    if user.profile == 'farmer':
        messages.warning(request,"Invalid Request")
        return redirect('dashboard')

    merchant = UserProfile.objects.get(user=user)

    bids = BidEntry.objects.filter(merchant_bidding=merchant)

    data = {
        'bids' : bids
    }
    print(bids)
    return render(request,'bidding/view_bids.html',data)
    

