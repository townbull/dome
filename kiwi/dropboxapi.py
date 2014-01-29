# Include the Dropbox SDK
import dropbox



def dropboxconn():
    # Get your app key and secret from the Dropbox developer website
    app_key = '3hlhqwpriatnh49'
    app_secret = 'b8fy7drsxmdnwmu'

    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

    # Have the user sign in and authorize this token
    authorize_url = flow.start()
    print '1. Go to: ' + authorize_url
    print '2. Click "Allow" (you might have to log in first)'
    print '3. Copy the authorization code.'
    code = raw_input("Enter the authorization code here: ").strip()

    # This will fail if the user enters an invalid authorization code
    access_token, user_id = flow.finish(code)

    client = dropbox.client.DropboxClient(access_token)
    return client.account_info()

# Uploading files
def dropboxupload(filename):
    f = open(filename, 'rb')
    response = client.put_file('/'+filename, f)
    return response

# Listing folders
def dropboxlist():
    folder_metadata = client.metadata('/')
    return folder_metadata

# Downloading files
def dropboxdownload(filename):
    f, metadata = client.get_file_and_metadata(filename)
    out = open(filename, 'wb')
    out.write(f.read())
    out.close()
    return metadata

dropboxconn()
dropboxupload("abc.txt")