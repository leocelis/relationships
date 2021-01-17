import os

from linkedin import linkedin

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

RETURN_URL = 'http://localhost:8000'

authentication = linkedin.LinkedInAuthentication(
    CLIENT_ID,
    CLIENT_SECRET,
    RETURN_URL,
    linkedin.PERMISSIONS.enums.values()
)

# Optionally one can send custom "state" value that will be returned from OAuth server
# It can be used to track your user state or something else (it's up to you)
# Be aware that this value is sent to OAuth server AS IS - make sure to encode or hash it
# authorization.state = 'your_encoded_message'

# print(authentication.authorization_url)  # open this url on your browser
# https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=78dwb3gun5pifi&scope=r_emailaddress,r_liteprofile&state=a38760d62065598acc5d8c33ce11a281&redirect_uri=http://localhost:8080/code/

authentication.authorization_code = 'AQWRIKle12ZyoUE5Kn9RxdBjgx-sn90rw9UW-3sBw1p2682VQGcMOR-fXpWq9Uu0pHrbZbW820QuqMeDlMRIYnkzYCLTf1K4aw-k2Q4Gv5mQooiXcb0Sganq1yQm5irL5sVmFX25PpsCjROpLniE9ZLUqF6cypwE3rKUmRw4gIkwpfgVNx2bPXkRLcj6nd4uXzEbCvge6uSZ3ixz6BFisabfIBeoaDZiBqDGCYBq-4KXUWE2eBpBX5AK--4-xxcXPjH67FpJnRLtXH1Rq_zRUHsyja9GHxZDUKuLXQot-h9mNZlOI0ODp5hxndoeB5B4BPQxpV_oMr3VP37PbddbVRKjooimPQ'
result = authentication.get_access_token()

print("Access Token:", result.access_token)
print("Expires in (seconds):", result.expires_in)

application = linkedin.LinkedInApplication(
    token='AQWRIKle12ZyoUE5Kn9RxdBjgx-sn90rw9UW-3sBw1p2682VQGcMOR-fXpWq9Uu0pHrbZbW820QuqMeDlMRIYnkzYCLTf1K4aw-k2Q4Gv5mQooiXcb0Sganq1yQm5irL5sVmFX25PpsCjROpLniE9ZLUqF6cypwE3rKUmRw4gIkwpfgVNx2bPXkRLcj6nd4uXzEbCvge6uSZ3ixz6BFisabfIBeoaDZiBqDGCYBq-4KXUWE2eBpBX5AK--4-xxcXPjH67FpJnRLtXH1Rq_zRUHsyja9GHxZDUKuLXQot-h9mNZlOI0ODp5hxndoeB5B4BPQxpV_oMr3VP37PbddbVRKjooimPQ')
application.get_connections()
