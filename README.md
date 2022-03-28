# About
This is a advertisments site on django

[Runing](http://51.250.99.152) in yandex.cloud on ubuntu 20.04 LTS.

# Quick Start
Use command
>$ docker-compose up -d
>
to start site by localhost

To add rubrics go to admin page ~/admin/

login/pass by default is admin/admin

# Functional
~/ - main page with list of all advertisments. Viewed via pagonator by 6 ads on page. On the left menu there is sorting by rubrics, login, adding an ads and search for title or for matches in the description of ad.
Ads can be two types. The first ad from the auto section. This is object of class Car inherits from class Bb. Objects of class Bb are all other ads.

~/add/ - add an ads. Take rubric. And if it auto then make auto ad from clss Car. If other rubric create ads from class Bb. When create auto ad his price are analysis by several params. Take avg price of similar ads (same model, made year delta is 1, mileage delta is 30 fousend). If delta of price is more at 10, 20, 30% or lower than information of it will be translited when user sees detail ad.

~/detail/pk/ - view ad, where pk is id of ad. If current user are made this ad or had perms he can edit or delete that ads. Also form of view make link that shows info about owner of that ad.

~/detail_car/pk/ - view auto ad. Same as previous but with view via CarForm(Bb objects views via BbForm). 

~/edit/pk/ - edit ad by form of class Bb.

~/delete/pk/ - delete ad.

~/car_edit/pk/ - edit auto ad by form of class Car.

~/accounts/login(registrate, logout) - standard user functionality. Class User consist of standart django User and custom class Profile with phone number and birth day fileds. Class Profile linked with class User via OneToOneField user. When calling the functions of creating/changing a class User, a signal is passed to create objects of the object from class Profile.

~/accounts/profile - menu of profile when user can see or edit his data.

~/profile/ads - all ads from current user.
