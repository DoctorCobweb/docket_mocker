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

2. locate python-escpos and move it to your site-packages folder

   for 'epson' conda env. 

   e.g. location is /home/der/anaconda3/envs/epson/lib/python3.7/site-packages

3. run pip install -e escpos to install escpos from a local project path.
   => it can then be imported in other src files

4. something like this should now work:

   from escpos.print import Serial
   ...
