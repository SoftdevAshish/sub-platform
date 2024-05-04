import json
import requests
from .models import Subscription


def get_access_token():
    data = {"grant_type": "client_credentials"}
    headers = {"Accept": "application/json", "Accept-Language": "en-US"}

    client_id = "AS88XhceWTHbZ_4p9Lr32QGHbfJPUGyqoTsAymy98SxELYTW2JDOncMZzSOsvKhVXP9ZHTTBg_xaGFay"
    secret_id = "EB7Bgxfs6md3ciavQ2KpqmcFIavgW6nGUxNuo1BdWa0ioTz4wibHNeWy0mIzMol9hnJL-lfp5DrY9ju9"

    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    r = requests.post(
        url, auth=(client_id, secret_id), headers=headers, data=data
    ).json()
    access_token = r["access_token"]

    return access_token


def cancel_subscription_paypal(access_token, subscription_id):
    bearer_token = "Bearer " + access_token
    headers = {"Content-Type": "application/json", "Authorization": bearer_token}
    url = (
        "https://api.sandbox.paypal.com/v1/billing/subscriptions/"
        + subscription_id
        + "/cancel"
    )
    r = requests.post(url, headers=headers)


def update_subscription_paypal(access_token, subscription_id):
    bearer_token = "Bearer " + access_token
    headers = {"Content-Type": "application/json", "Authorization": bearer_token}
    sub_details = Subscription.objects.get(paypal_subscription_id=subscription_id)
    current_subscription_plan = sub_details.subscription_plan
    if current_subscription_plan == "Standard":
        new_subscription_plan_id = "P-7G886984HF913452DMYZWIDQ"  # To Premium Plan
    elif current_subscription_plan == "Premium":
        new_subscription_plan_id = "P-0V263541YJ847252NMYZWHEI"  # To Standard Plan
    url = (
        "https://api.sandbox.paypal.com/v1/billing/subscriptions/"
        + subscription_id
        + "/revise"
    )
    revision_data = {"plan_id": new_subscription_plan_id}
    # Make a POST request to paypal's API for updating/revising  a subscription.
    r = requests.post(url, headers=headers, data=json.dumps(revision_data))
    # Output the response from paypal.
    response_data = r.json()
    print(response_data)
    approve_link = None
    for link in response_data.get("links", []):
        if link.get("rel") == "approve":
            approve_link = link["href"]

    if r.status_code == 200:
        print("Request was a success")
        return approve_link
    else:
        print("Sorry, an error occured!")


def get_current_subscription_paypal(access_token, subID):
    bearer_token = "Bearer " + access_token
    headers = {"Content-Type": "application/json", "Authorization": bearer_token}
    url = f"https://api.sandbox.paypal.com/v1/billing/subscriptions/{subID}"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        subscription_data = r.json()
        current_subscription_plan_id = subscription_data.get("plan_id")
        return current_subscription_plan_id
    else:
        print("Sorry, Failed to retrieve subscription details!")
        return None
