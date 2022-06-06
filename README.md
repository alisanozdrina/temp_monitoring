# temp_monitoring
to copy repo into your local directory:<br />
$git clone https://github.com/alisanozdrina/temp_monitoring.git <br /> 
$cd temp_monitoring
to execute the script on cobalt<br />
$source /cvmfs/ara.opensciencegrid.org/trunk/centos7/setup.sh <br /> 
$python makeReport.py STATION1B 7<br />
in case you want ara1 data for the last 7 days <br /> 
If you need ara3 data:<br />
$python makeReport.py STATION3 7 <br />  

to update script up to the newest version execute: <br />
$git pull origin main <br />
in temp_monitoring directory <br />
