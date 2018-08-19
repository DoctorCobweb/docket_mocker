# DOCKET MOCKER

use python-escpos to generate fake orders.
send them down the serial slide to KNUCKLE DRAGGER.

notes
-----
uses python-escpos v3.0a4 which can be downloaded from:
https://github.com/python-escpos/python-escpos/releases/download/v3.0a4/python-escpos-3.0a4.zip

to install this module:
1. create a conda env, then activate it

   conda create --name epson
   source activate epson

2. locate python-escpos and move it to your site-packages folder for 'epson' conda env. 

   e.g. on MacOS location is /home/der/anaconda3/envs/epson/lib/python3.7/site-packages

3. install it using 'pip -e' to install from a local path

   `~/anaconda/envs/epson/bin/pip install -e ~/anaconda/envs/epson/python3.7/site-packages/python-escpos-3.0a4`  

4. when you try to import it like this:  

   `from escpos.print import Serial`  

   you will get an error for file not found for 'capabilities.json'
   => to fix: find this file under the /capabilities-data/dist/ folder and copy it over to src/ folder

5. you should be able to import it without errors:  
   `from escpos.print import Serial`  


