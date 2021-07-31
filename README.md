# razer_blade_14_2021_rgb_logo_simple_control
## prerequisite
  python3  
  libusb  
  pyusb

## usage
  sudo python ctrl.py [-h] [--logo LOGO] [--rgb R G B] [--default]  
  optional arguments:  
  -h, --help            
  show help message  
  --logo LOGO, -l LOGO  
  0 for off, 1 for static and 2 for breathing  
  --rgb R G B, -r R G B  
  rgb decimal ints(0-255): 11 22 33 for example  
  --default, -d     
  perform default action: 0 and 2 2 2
    
  just try it out
  
## how it works
  the rgb keys and the logo are controlled through usb protocal  
  this little script does almost the same as the official software does   
  sends some message to the device and it's done  
  see the script for yourself and do some research if you're interested
  
## misc
  for advanced keyboard rgb effects you may want to check out [OpenRGB](https://gitlab.com/CalcProgrammer1/OpenRGB)   
  i wrote it mainly to silent the rgb keys on linux  
  the logo seems to have only 3 basic effects  
  
  that't all, so long
