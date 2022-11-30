from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


import iot_api_client as iot
from iot_api_client.rest import ApiException
from iot_api_client.configuration import Configuration
# my adds from solution:
# https://forum.arduino.cc/t/setting-and-reading-thing-variables-via-the-python-api/1016744
from openapi_client.rest import ApiException


def arduinoCloud(info, cl_id, cl_secret, thing_id):
    """
    Makes a call to the Arduino IoT Cloud API and sends the information to the Thing variable for display on the
    OLED. The code on the arduino may need to take the info string and format it for proper display.
    Jim's key info:
    client ID: "ExaaT5TS1WeBmkQiuPJnplP6zko7CN7H"
    client secret: "PuSvabfvrpCHqLgf6f7DfRcLVi2AhU2PcuPX4RB3XRcr6kZKmOhh1gqhj7iBsTd2"
    Thing ID: "68fbca63-9370-4e52-ae84-f3388241ca88"
    Property ID (derived from the properties API): "8efb3a00-fdc2-420e-89db-ae20ddd56cdb"
    :param info: the information being passed in
    :param cl_id: the arduino cloud API client ID
    :param cl_secret: the arduino cloud API client secret
    :param thing_id: the thing ID (found on the metadata tab)
    :return: True if successful else False
    """
    oauth_client = BackendApplicationClient(client_id="ExaaT5TS1WeBmkQiuPJnplP6zko7CN7H")
    token_url = "https://api2.arduino.cc/iot/v1/clients/token"

    oauth = OAuth2Session(client=oauth_client)
    token = oauth.fetch_token(
        token_url=token_url,
        client_id=cl_id,
        client_secret=cl_secret,
        include_client_id=True,
        audience="https://api2.arduino.cc/iot",
    )

    # store access token in access_token variable
    access_token = token.get("access_token")

    # configure and instance the API client with our access_token
    client_config = Configuration(host="https://api2.arduino.cc/iot")
    client_config.access_token = access_token
    client = iot.ApiClient(client_config)

    """
    ****this can be used to get the properties id****
    # api = iot.PropertiesV2Api(client)
    try:
        resp = api.properties_v2_list(thing_id)
        print(resp)
    except ApiException as e:
        print("Got an exception: {}".format(e))
    """

    # Update the Thing variable
    properties = iot.PropertiesV2Api(client)
    PROPERTY_ID = '8efb3a00-fdc2-420e-89db-ae20ddd56cdb'  # from resp
    propertyValue = {"value": info}
    try:
        # publish properties_v2
        properties.properties_v2_publish(thing_id, PROPERTY_ID, propertyValue)
        return True
    except ApiException as e:
        print("Exception when calling PropertiesV2Api->propertiesV2Publish: %s\n" % e)
        return False
