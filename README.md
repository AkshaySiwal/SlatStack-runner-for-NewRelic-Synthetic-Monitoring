# SlatStack-runner-for-NewRelic-Synthetic-Monitoring

A newrelic runner for saltstack has been created to perform tasks like creation and updation of synthetics alerts on newrelic using newrelic APIs from SaltStack. 



## Function available in newrelic saltstack-runner :



1) [synthetics_create][create-url]

2) [synthetics_update][synthetics_update]

3) [synthetics_listAll][synthetics_listAll]

4) [synthetics_updateScript][synthetics_updateScript]

5) [synthetics_formatScript][synthetics_formatScript]

6) [synthetics_alertPolicy_ctrl][synthetics_alertPolicy_ctrl]



## Commands to create/edit any alert on Newrelic  


### 1) Command to create a synthetic alert : 

 ```salt-run newrelic.synthetics_create <alert_name, required> <alert_frequency, default=15 minutes [number]>  <slaThreshold, default = "10.0" [string]) <locations default = [ "AWS_US_WEST_1" ] [list])> <type  default="script_browser" [string]> ```


 Example : salt-run newrelic.synthetics_create my_sample_alert





### 2) Command to list all created synthetic alert : 

 ```salt-run newrelic.synthetics_listAll <return_dict default='n'>```
Args : 

return_dict default = n , to print output in form of table

return_dict default = y , to print output in form of dictionary 

Example : salt-run newrelic.synthetics_listAll





### 3) Command to update a synthetic alert :  

```salt-run newrelic.synthetics_update <alert_current_name, required>  <updated_name,default = "NA"[string]> <alert_frequency, default="NA" minutes [number]>  <slaThreshold, default = "NA" [string]) <locations default = "NA" [list])> <type  default="NA" [string]> <status , default = "NA">```
 Example :

To rename alert :      salt-run newrelic.synthetics_update "my_sample_alert"  "new_name_for_alert"

To change alert frequeny :    salt-run newrelic.synthetics_update "new_name_for_alert" frequency=60



### 4) Command to update/upload alert script a synthetic alert : 

```salt-run newrelic.synthetics_updateScript <alert_name, required>  <path_to_alert_script, required>```
Example :

To upload/update alert script :     salt-run newrelic.synthetics_update_script "my_sample_alert" /tmp/akshay.js 





### 5) Command to convert alert script to required format of synthetic alert : 

It will format script and save it same file and will convert backup file with orignal content with .bkp extenstion 

```salt-run newrelic.synthetics_formatScript <path_to_alert_script, required>```
Example :

To change format :   salt-run newrelic.synthetics_formatScript /tmp/akshay.js





 ### 6) Command to add alert notification policy to synthetic alert : 

It will attached newrelic alert to given notification policy and you can enable/disable it with this function.

```salt-run newrelic.synthetics_alertPolicy_ctrl <alert_name, required>  <policy_id, required> <action, default="true", [string]>  <runbook, default="" [string]>```
Example :

To rename alert :    salt-run newrelic.synthetics_alertPolicy_ctrl "my_sample_alert"  124473




[synthetics_create]: https://github.com/AkshaySiwal/SlatStack-runner-for-NewRelic-Synthetic-Monitoring#ommand-to-create-a-synthetic-alert
[synthetics_update]: https://github.com/AkshaySiwal/SlatStack-runner-for-NewRelic-Synthetic-Monitoring#Command-to-list-all created synthetic alert
[synthetics_listAll]: https://github.com/AkshaySiwal/SlatStack-runner-for-NewRelic-Synthetic-Monitoring#Command-to-update-a-synthetic-alert
[synthetics_updateScript]: https://github.com/AkshaySiwal/SlatStack-runner-for-NewRelic-Synthetic-Monitoring#Command-to-update/upload-alert-script-a-synthetic-alert
[synthetics_formatScript]: https://github.com/AkshaySiwal/SlatStack-runner-for-NewRelic-Synthetic-Monitoring#Command-to-convert-alert-script-to-required-format-of-synthetic-alert
[synthetics_alertPolicy_ctrl]: https://github.com/AkshaySiwal/SlatStack-runner-for-NewRelic-Synthetic-Monitoring#Command-to-add-alert-notification-policy-to-synthetic-alert
