import requests, json, base64,fileinput, re
url  = 'https://synthetics.newrelic.com/synthetics/api/v3/monitors'
api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
############ Newrelick create script_browser check ########

def synthetics_create(name, frequency = 15 , slaThreshold = "10.0", locations = "AWS_US_WEST_1" , type =  "script_browser" ) :
  headers = {
      'X-Api-Key': api_key,
      'Content-Type': 'application/json',
  }
  loc = locations.split(';')

  data = json.dumps({ "name" : name, "frequency" : frequency, "locations" : loc, "type" : type , "status" : "enabled", "slaThreshold" : slaThreshold })
  try :
    response = requests.post( url=url, headers=headers, data=data )
  except Exception as e:
    return 'Exception : Unable to create monitor "' + name + '"' , False
  if response.status_code / 100 != 2 :
    return 'Http-code ' + str(response.status_code) + ' : Unable to create monitor "' + name + '"' + 'You may run it again if you are sure there is no network errors' , False
  return 'Http-code ' + str(response.status_code) + ' : Created monitor "' + name + '"', True
  



############ Newrelick create script_browser check ########

def synthetics_update(name, updated_name = "NA", frequency = "NA" , slaThreshold = "NA", locations = "NA", type =  "NA", status = "NA" ) :
  my_dict = synthetics_listAll("y")
  try :
    my_id = my_dict[name]['id']
  except Exception as e:
    return 'Exception : ' + name + ' does not exist. Please create it first with command "salt-run newrelic.synthetics_create <name>"', False

  headers = {
      'X-Api-Key': api_key,
      'Content-Type': 'application/json',
  }

  data = {} 
  data_raw = { "name" : updated_name, "frequency" : frequency, "locations" : locations, "type" : type , "status" : status, "slaThreshold" : slaThreshold }
  for k,v in data_raw.items() :
    if v != "NA" :
      data[k] = v 
  if "locations" in data :
      data["locations"] = locations.split(';')
  data = json.dumps( data )
  update_url = url + '/' + my_id
  try :
    response = requests.patch( url=update_url, headers=headers, data=data )
  except Exception as e:
    return 'Exception : Unable to update monitor "' + name + '"', False
  if response.status_code / 100 != 2 :
    return 'Http-code ' + str(response.status_code) + ' : Unable to update monitor "' + name + '"' + 'You may run it again if you are sure there is no network errors', False
  return '\nHttp-code ' + str(response.status_code) + ' : Updated monitor "' + name + '"' + str(data), True

################## List all monitors ##########################

def synthetics_listAll( return_dict='n') :
  headers = {
      'X-Api-Key': api_key,
  }
  offset = 0
  my_limit = 100
  list_url = url + '/?offset=' + str(offset) + '&limit=' + str(my_limit)
  try :
    response = requests.get(url=list_url, headers=headers)
  except Exception as e:
    print '\nException : Unable to list monitors\n' 
    return False
  if response.status_code / 100 != 2 :
    print 'Http-code ' + str(response.status_code) + ' : Unable to list all monitors'
    print 'You may run it again if you are sure there is no network errors\n'
    return False
  table = [ '\nHttp-code ' + str(response.status_code) + ' : List of all monitors' ]
  out = json.loads(response.text)
  if out["count"] < my_limit :
    table.append( "\nTotal " +  str(out["count"]) + " monitors found : \n")
  elif out["count"] >= my_limit :
    table.append("\nTotal more than ( or equal to ) " + str(my_limit) + "  monitors found : \n")
  i = 1
  table.append( "\t{:<3})\t{:<9}\t{:<5}\t{:<16}\t{:^38}\t{}\n".format("SN", "STATUS", "FRE", "TYPE", "ID", "NAME") )
  item_list = out["monitors"]
  my_dict = {}
  for item in item_list :
    table.append("\t{:<3})\t{:<9}\t{:<5}\t{:<16}\t{:^38}\t'{}'".format(str(i), item["status"], item["frequency"], item["type"], item['id'], item['name']))
    i = i + 1
    my_dict[item['name']] = {}
    my_dict[item['name']]['id'] = item['id']
    my_dict[item['name']]['status'] = item['status']
    my_dict[item['name']]['frequency'] = item['frequency']
    my_dict[item['name']]['type'] = item['type']
    if i % my_limit ==  0 :
       offset = offset + my_limit
       list_url = url + '/?offset=' + str(offset) + '&limit=' + str(my_limit)
       response = requests.get(url=list_url, headers=headers) 
       out = json.loads(response.text)
       item_list.extend(out["monitors"])
  print "\n"
  if return_dict.upper() == "Y" :
    return my_dict
  else :
    for row in table :
      print row
    return True
  
 

############### Update my check ##################################

def synthetics_updateScript( name, script_file ) :
  my_dict = synthetics_listAll("y")
  try :
    my_id = my_dict[name]['id']
  except Exception as e:
    print '\nException : ' + name + ' does not exist. Please create it first with command "salt-run newrelic.synthetics_create <name>"\n'
    return False
  edit_url = url + '/' + my_id + '/script'
  with open(script_file) as f :
    script = f.read()
  encoded_script = base64.b64encode(script)
  headers = {
      'X-Api-Key': api_key,
      'Content-Type': 'application/json',
  }
  data = json.dumps({ "scriptText" : encoded_script })

  try :
    response = requests.put( url=edit_url, headers=headers, data=data )
  except Exception as e:
    return 'Exception : Unable to update monitor "' + name + '"', False
  if response.status_code / 100 != 2 :
    return 'Http-code ' + str(response.status_code) + ' : Unable to update monitor "' + name + '"' + 'You may run it again if you are sure there is no network errors', False
  return 'Http-code ' + str(response.status_code) + ' : Updated monitor "' + name + '"', True


def synthetics_formatScript(filename) :
  file = fileinput.FileInput(filename, inplace=True, backup='.bak')
  for line in file:
     if 'selenium-webdriver' not in line and 'driver.Builder' not in line :
       line  = line.replace("browser", "$browser")
       line = line.replace("driver", "$driver")
       line = re.sub("\$+","$", line)
       print line.replace("\n", "")
  return "Script file : " + filename + ', Backup file : ' + filename + '.bak'


############### Update my checkwith Alert policy  ##################################

def synthetics_alertPolicy_add( name, policy_id, action="true", runbook="" ) :
  my_dict = synthetics_listAll("y")
  try :
    my_id = my_dict[name]['id']
  except Exception as e:
    return 'Exception : ' + name + ' does not exist. Please create it first with command "salt-run newrelic.synthetics_create <name>"', False
  policy_url = 'https://api.newrelic.com/v2/alerts_synthetics_conditions/policies/' + str(policy_id) + '.json'
  headers = {
      'X-Api-Key': api_key,
      'Content-Type': 'application/json',
  }
  data = json.dumps({ 
  "synthetics_condition": {
    "name": "SYNTHETICS_MONITOR_FAILURE_" + name,
    "monitor_id": my_id,
    "runbook_url": runbook,
    "enabled": action
  }
  })

  try :
    response = requests.post( url=policy_url, headers=headers, data=data )
  except Exception as e:
    return 'Exception : Unable to update alert policy ' + str(policy_id) + ' for monitor "' + name + '"', False
  if response.status_code / 100 != 2 :
    return 'Http-code ' + str(response.status_code) + ' : Unable to update alert policy ' + str(policy_id) + ' for monitor "' + name + '"', 'You may run it again if you are sure there is no network errors', False
  return '\nHttp-code ' + str(response.status_code) + ' : Updated alert policy ' + str(policy_id) + ' for monitor "' + name + '"', True


############### Update my checkwith Alert policy  ##################################

def synthetics_alertPolicy_update( name,  policy_id, action="true", runbook="" ) :
  my_dict = synthetics_listAll("y")
  try :
    my_id = my_dict[name]['id']
  except Exception as e:
    return 'Exception : ' + name + ' does not exist. Please create it first with command "salt-run newrelic.synthetics_create <name>"', False
  my_con = synthetics_alertPolicy_list( policy_id)
  try :
    for i in my_con['synthetics_conditions'] :
        if i['name'] == 'SYNTHETICS_MONITOR_FAILURE_' + name :
            my_con_id = i['id']
            break
  except Exception as e:
    return 'Exception : ' + name + ' does not have any alert condition defined. Please create alert condition first with command "salt-run newrelic.alertPolicy_add <monitor-name> <policy-id> <true/false [defalut true]> <runbook-url [optional]>"', False


  policy_url = 'https://api.newrelic.com/v2/alerts_synthetics_conditions/' + str(my_con_id) + '.json'
  headers = {
      'X-Api-Key': api_key,
      'Content-Type': 'application/json',
  }
  data = json.dumps({
  "synthetics_condition": {
    "name": "SYNTHETICS_MONITOR_FAILURE_" + name,
    "monitor_id": my_id,
    "runbook_url": runbook,
    "enabled": action
  }
  })

  try :
    response = requests.put( url=policy_url, headers=headers, data=data )
  except Exception as e:
    return 'Exception : Unable to update alert condition for policy ' + str(policy_id) + ' for monitor "' + name + '"', False
  if response.status_code / 100 != 2 :
    return '\nHttp-code ' + str(response.status_code) + ' : Unable to update alert condition for policy ' + str(policy_id) + ' for monitor "' + name + '"', 'You may run it again if you are sure there is no network errors', False
  return 'Http-code ' + str(response.status_code) + ' : Updated alert condition policy ' + str(policy_id) + ' for monitor "' + name + '"', False
                 


############  Alerts Synthetics Conditions > List #######

def synthetics_alertPolicy_list( policy_id ) :
  policy_list_url = 'https://api.newrelic.com/v2/alerts_synthetics_conditions.json'
  headers = {
      'X-Api-Key': api_key,
      'Content-Type': 'application/json',
  }
  params = {
  "policy_id" : policy_id
  }
  try :
    response = requests.get( url=policy_list_url, headers=headers, params=params )
    out = json.loads(response.text)
  except Exception as e:
    return '\nException : Unable to list conditions for alert policy ' + str(policy_id), False
  if response.status_code / 100 != 2 :
    return 'Http-code ' + str(response.status_code) + ' : Unable to list conditions for alert policy ' + str(policy_id), 'You may run it again if you are sure there is no network errors', False
  return '\nHttp-code ' + str(response.status_code) + ' : List of conditions for alert policy ' + str(policy_id) , out, True


