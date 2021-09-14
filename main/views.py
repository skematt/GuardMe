from django.shortcuts import render, redirect
from datetime import datetime
from .models import Crime
from django.utils import timezone
from math import radians, sin, cos, acos
import keras
import numpy as np

CHOICES = ['VANDALISM - Flon2Y ($400 & OVER, ALL CHURCH VANDALISMS)', 'OTHER MISCELLANEOUS CRIME', 'BURGLARY FROM VEHICLE', 'THEFT-GRAND ($950.01 & OVER)EXCPT,GUNS,FOWL,LIVESTK,PROD', 'CHILD NEGLECT (SEE 300 W.I.C.)', 'INTIMATE PARTNER - SIMPLE ASSAULT', 'SHOPLIFTING - PETTY THEFT ($950 & UNDER)', 'BURGLARY', 'ARSON', 'ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT', 'BATTERY - SIMPLE ASSAULT', 'CHILD ABUSE (PHYSICAL) - SIMPLE ASSAULT', 'ROBBERY', 'THEFT PLAIN - ATTEMPT', 'VANDALISM - MISDEAMEANOR ($399 OR UNDER)', 'CRIMINAL THREATS - NO WEAPON DISPLAYED', 'THEFT, PERSON', 'BOMB SCARE', 'VEHICLE - STOLEN', 'THEFT PLAIN - PETTY ($950 & UNDER)', 'CHILD ABUSE (PHYSICAL) - AGGRAVATED ASSAULT', 'THROWING OBJECT AT MOVING VEHICLE', 'DISTURBING THE PEACE', 'BATTERY POLICE (SIMPLE)', 'ATTEMPTED ROBBERY', 'CRM AGNST CHLD (13 OR UNDER) (14-15 & SUSP 10 YRS OLDER)', 'ASSAULT WITH DEADLY WEAPON ON POLICE OFFICER', 'TRESPASSING', 'INTIMATE PARTNER - AGGRAVATED ASSAULT', 'SODOMY/SEXUAL CONTACT B/W PENIS OF ONE PERS TO ANUS OTH', 'ORAL COPULATION', 'VEHICLE - ATTEMPT STOLEN', 'THEFT OF IDENTITY', 'THEFT FROM MOTOR VEHICLE - PETTY ($950 & UNDER)', 'BATTERY WITH SEXUAL CONTACT', 'LETTERS, LEWD  -  TELEPHONE CALLS, LEWD', 'VIOLATION OF RESTRAINING ORDER', 'DOCUMENT FORGERY / STOLEN Flon2Y', 'VIOLATION OF COURT ORDER', 'PIMPING', 'SEX,UNLAWFUL(INC MUTUAL CONSENT, PENETRATION W/ FRGN OBJ', 'SEXUAL PENETRATION W/FOREIGN OBJECT', 'THEFT FROM MOTOR VEHICLE - GRAND ($400 AND OVER)', 'BIKE - STOLEN', 'EMBEZZLEMENT, GRAND THEFT ($950.01 & OVER)', 'EXTORTION', 'COUNTERFEIT', 'SHOTS FIRED AT INHABITED DWELLING', 'PURSE SNATCHING', 'BRANDISH WEAPON', 'CREDIT CARDS, FRAUD USE ($950.01 & OVER)', 'RAPE, FORCIBLE', 'THREATENING PHONE CALLS/LETTERS', 'SHOPLIFTING-GRAND THEFT ($950.01 & OVER)', 'DEFRAUDING INNKEEPER/THEFT OF SERVICES, $400 & UNDER', 'CRIMINAL HOMICIDE', 'CHILD ANNOYING (17YRS & UNDER)', 'CRUELTY TO ANIMALS', 'BURGLARY FROM VEHICLE, ATTEMPTED', 'LEWD CONDUCT', 'THEFT FROM PERSON - ATTEMPT', 'BUNCO, PETTY THEFT', 'INDECENT EXPOSURE', 'RESISTING ARREST', 'DISCHARGE FIREARMS/SHOTS FIRED', 'RECKLESS DRIVING', 'CREDIT CARDS, FRAUD USE ($950 & UNDER', 'VIOLATION OF TEMPORARY RESTRAINING ORDER', 'DOCUMENT WORTHLESS ($200.01 & OVER)', 'BURGLARY, ATTEMPTED', 'CHILD STEALING', 'WEAPONS POSSESSION/BOMBING', 'KIDNAPPING', 'CONSPIRACY', 'STALKING', 'OTHER ASSAULT', 'RAPE, ATTEMPTED', 'ILLEGAL DUMPING', 'GRAND THEFT / INSURANCE FRAUD', 'FALSE POLICE REPORT', 'SHOTS FIRED AT MOVING VEHICLE, TRAIN OR AIRCRAFT', 'DRIVING WITHOUT OWNER CONSENT (DWOC)', 'BUNCO, ATTEMPT', 'THEFT FROM MOTOR VEHICLE - ATTEMPT', 'BUNCO, GRAND THEFT', 'KIDNAPPING - GRAND ATTEMPT', 'PANDERING', 'FALSE IMPRISONMENT', 'FAILURE TO YIELD', 'TILL TAP - ATTEMPT', 'CONTRIBUTING', 'TILL TAP - GRAND THEFT ($950.01 & OVER)', 'CONTEMPT OF COURT', 'EMBEZZLEMENT, PETTY THEFT ($950 & UNDER)', 'BOAT - STOLEN', 'DEFRAUDING INNKEEPER/THEFT OF SERVICES, OVER $400', 'INCITING A RIOT', 'BEASTIALITY, CRIME AGAINST NATURE SEXUAL ASSLT WITH ANIM', 'PROWLER', 'PEEPING TOM', 'BATTERY ON A FIREFIGHTER', 'UNAUTHORIZED COMPUTER ACCESS', 'SHOPLIFTING - ATTEMPT', 'BRIBERY', 'LYNCHING - ATTEMPTED', 'CHILD ABANDONMENT', 'THEFT, COIN MACHINE - ATTEMPT', 'DISHONEST EMPLOYEE - GRAND THEFT', 'THEFT, COIN MACHINE - GRAND ($950.01 & OVER)', 'DOCUMENT WORTHLESS ($200 & UNDER)', 'MANSLAUGHTER, NEGLIGENT', 'PICKPOCKET', 'THEFT, COIN MACHINE - PETTY ($950 & UNDER)', 'HUMAN TRAFFICKING - COMMERCIAL SEX ACTS', 'LEWD/LASCIVIOUS ACTS WITH CHILD', 'DRUNK ROLL', 'PURSE SNATCHING - ATTEMPT', 'BIKE - ATTEMPTED STOLEN', 'TELEPHONE PROPERTY - DAMAGE', 'PICKPOCKET, ATTEMPT', 'FAILURE TO DISPERSE', 'DISHONEST EMPLOYEE - PETTY THEFT', 'DRUGS, TO A MINOR', 'DISRUPT SCHOOL', 'PETTY THEFT - AUTO REPAIR', 'TILL TAP - PETTY ($950 & UNDER)', 'DISHONEST EMPLOYEE ATTEMPTED THEFT', 'INCEST (SEXUAL ACTS BETWEEN BLOOD Rlat2IVES)', 'BIGAMY', 'REPLICA FIREARMS(SALE,DISPLAY,MANUFACTURE OR DISTRIBUTE)', 'LYNCHING', 'CHILD PORNOGRAPHY', 'HUMAN TRAFFICKING - INVOLUNTARY SERVITUDE', 'GRAND THEFT / AUTO REPAIR', 'BLOCKING DOOR INDUCTION CENTER', 'TRAIN WRECKING', 'ABORTION/ILLEGAL', 'FIREARMS RESTRAINING ORDER (FIREARMS RO)', 'FIREARMS TEMPORARY RESTRAINING ORDER (TEMP FIREARMS RO)', 'DRUNK ROLL - ATTEMPT']

def main(request):
    return render(request, 'main/main.html')

def input_data(request):
    if request.method == 'POST' and request.POST.get('crime') in CHOICES:
        crime = Crime()
        crime.reported_time = datetime.strptime(request.POST.get('date') + ' ' + request.POST.get('time'), '%Y-%m-%d %H:%M')
        crime.crime = request.POST.get('crime')
        crime.latitude = request.POST.get('latitude')
        crime.longitude = request.POST.get('longitude')
        crime.address = request.POST.get('address')
        crime.save()
        temp = f"/view/{request.POST.get('latitude')}/{request.POST.get('longitude')}/"
        return redirect(temp)
    return render(request, 'main/input_data.html', {'choices': CHOICES, 'date': datetime.now().strftime('%Y-%m-%d'), 'time': datetime.now().strftime('%H:%M')})

def view(request):
    crimes = list(reversed(Crime.objects.all()[len(Crime.objects.all()) - 10:]))
    for crime in crimes:
        crime.reported_time = timezone.localtime(crime.reported_time)
        crime.date = crime.reported_time.strftime('%Y/%m/%d')
        crime.time = crime.reported_time.strftime('%I:%M %p')
        crime.location = f'Lat: {crime.latitude} Long: {crime.longitude}'
    return render(request, 'main/view.html', {'crimes': crimes})

def predict(request, latitude, longitude):
    date_list = [0] * 7
    date_list[datetime.now().weekday()] = 1
    time = (datetime.now().hour + (datetime.now().minute / 60)) / 24
    temp = date_list + [time, (float(latitude) / 200 + 0.5), (float(longitude) / 400 + 0.5)]
    temp = np.array(temp).reshape(-1, 10)
    model = keras.models.load_model('main/Model.h5')
    predictions = model.predict(temp)[0]
    X = []
    m = 0
    for a in range(3):
        for b in range(len(predictions)):
            if predictions[b] > predictions[m]:
                m = b
        X.append({'crime': CHOICES[m], 'percentage': round(predictions[m] * 100, 2)})
        predictions[m] = 0
    return render(request, 'main/predict.html', {'date': datetime.now().strftime('%Y/%m/%d'), 'time': datetime.now().strftime('%H:%M %p'), 'latitude': round(float(latitude), 4), 'longitude': round(float(longitude), 4), 'predictions': X})