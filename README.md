# quadroscope

A four cameara raspberry stack system. It is supposed to create 
animated GIFs out of 4 simultaneously created pictures made by 4
separate raspberry cameras.

![picture of the prototype](assets/camera-1.jpg)
![picture of the prototype](assets/camera-2.jpg)

# notes

- The 4 separate raspberries are linked via a dlink switch, because that was the most
straitforward way to link them
- The reason 4 separate board is needed is that the boards only support 1 camera at a time
and we could not find an easy workaround for it.
- there are many state of the art solutions in the code. Since this was supposed to be a Quick 
prototype we did not adress certain problems. The system is not roboust
- there are 3 slave and 1 master raspberry. The master has the GUI running on the linked
2,2 tft screen. 
- timing is solved through 3 separate GPIO channels being sent out by the master PI. 
This is because one GPIO output has problem driving 3 different PI's input.

# tools & useful commands

ssh into boss.

Run `./log` to see the live output of all the cameras.
![this is the first test picture](https://external.xx.fbcdn.net/safe_image.php?d=AQDgC7bbt9VW-qar&url=http%3A%2F%2Fvintagedigitalism.hu%2Fwp-content%2Fuploads%2F2016%2F03%2Funnamed1.gif&ext=gif)




# disclaimer

- This is a fast prototype.
- This is my first python project.

Created in [MeetLab](http://meetlab.hu) Budapest

