import requests
import getpass

def configure_session_and_url(group_folder_name=None): ### insert group folder name or leave empty for personal root
  '''
  interactively setup your sciencedata.dk homeurl, username and password
  in the case of shared folders owned by someone else, ask for owner username
  '''
  sciencedata_homeurl = "https://sciencedata.dk/files/" ### your personal homeurl 
  username = input("sciencedata.dk username (format '123456@au.dk'): ")
  password = getpass.getpass("sciencedata.dk password: ")
  ### establish a request session
  s = requests.Session()
  s.auth = (username, password)
  root_folder_url = sciencedata_homeurl
  if s.get(sciencedata_homeurl).ok:
    print("personal connection established")
    if group_folder_name != None:
      ### SETTING FOR GROUP FOLDER (you either have to be its owner, or at least know user name of its owner)
      group_owner_url = "https://sciencedata.dk/files/" + group_folder_name + "/"
      if s.get(group_owner_url).ok: ### if you are group 
        root_folder_url = group_owner_url ### use the url as the endpoint
        print("group connection established with you as owner")
      else: # otherwise use endpoint for "shared with me"
        group_owner = input("\"" + group_folder_name + "\" owner's username: ") ### in the case Vojtech is the group owner
        group_member_url = "https://sciencedata.dk/sharingin/" + group_owner + "/" + group_folder_name + "/" 
        if s.get(group_member_url).ok:
          root_folder_url = group_member_url
          print("group connection established with you as member")
        else:
          print("group connection failed")
  print("endpoint for requests has been configured to: " + root_folder_url)
  return s, root_folder_url
