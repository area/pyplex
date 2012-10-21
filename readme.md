#Pyplex

##Introduction

This is an implementation of an idea on the Plex forums - that the Raspberry Pi
could use a Plex client that had no interface, and was just designed to be 
operated using an iOS device or similar as a remote. Only the very barest bones
functionality is here, but I hope that it is reasonably easy to extend.

##Requirements

    sudo apt-get install avahi-daemon
    sudo pip install webpy

##How to use

Launch with 

    python pyplex 3000

and then 'Raspberry Plex' should appear as a player you can choose in your Plex
client. Choose your media, and select this as the player to play it on. It should 
begin playing on your Raspberry Pi!

I must reiterate how bare-bones this is. Once you start playing the media, you either
wait for it to finish, or 
    
    killall omxplayer.bin
