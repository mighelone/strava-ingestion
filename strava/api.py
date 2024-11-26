import requests

from .models import StravaToken


def refresh_access_token(
    client_id: str, client_secret: str, refresh_token: str
) -> StravaToken:
    """
    Refresh a Strava access token.

    Strava's access tokens are short-lived (6 hours). To get a new one, you need to
    use your client id, client secret, and the refresh token that was returned the
    last time you got an access token.

    :param client_id: Your Strava client ID.
    :param client_secret: Your Strava client secret.
    :param refresh_token: The refresh token returned by Strava the last time you
        got an access token.
    :return: A StravaToken with the new access token and refresh token.
    """
    token_url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }

    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    return StravaToken.model_validate(response.json())
