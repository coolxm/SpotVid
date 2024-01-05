This downloads a spotify playlist to  a specified directory  
It does this by downloading the stream from youtube, with the option of high quality, low quality and audio  

A lot of this is tactfully copied from other people, but I wrote this a couple years ago and do not remember enough to cite it, I have learnt from my mistakes and am dedicated to do better later.

What I do remember is big thanks to pyTube for making the switch from my old library really easy  

It takes a while to run but this was done partly because Im still figuring out multithreading, it already hits 100mb/s on my computer and 80mb of ram so thats quite nice. Also easy on cpu resources. It also says in the GUI when it is done (that took suprisingly long to code tbh) so thats a nice qol.  

If someone has a better way to compile this then what I am using please do tell...  

## Requirements

You need a spotify key stored in spotAuth.json file in this format  
{  
    "client_id": "client_id",  
    "client_secret" : "client_secret"  
}