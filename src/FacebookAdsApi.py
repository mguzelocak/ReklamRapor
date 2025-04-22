import requests
import os
from dotenv import load_dotenv
load_dotenv()

class FacebookAdsAPI:
    """
    Handles interaction with the Facebook Graph API to fetch ad account data
    and ad campaign performance insights. Includes methods to gather ad accounts,
    retrieve insights, and generate summarized reports for analysis.
    """
    def __init__(self):
        """
        Initializes the FacebookAdsAPI with access token and base URL.
        The access token is pulled from environment variables.
        """
        self.access_token = os.getenv("ACCESS_TOKEN").strip()
        self.base_url = "https://graph.facebook.com/v19.0"

    def get_ad_accounts(self) -> list:
        """
        Fetches all ad accounts associated with the access token user.

        Returns:
            list: A list of dicts, each containing 'id' and 'name' of an ad account.
        """

        url = "https://graph.facebook.com/v19.0/me/adaccounts"
        params = {
            "access_token": self.access_token,
            "fields": "id,name"
        }
        res = requests.get(url, params=params)
        if res.status_code != 200:
            print(f"Error fetching ad accounts: {res.status_code} - {res.text}")
            return []
        return res.json().get("data", [])

    def get_insights(self, ad_account_id, token, fields="campaign_name,impressions,clicks,spend", level="campaign", date_preset="last_7d") -> list:
        """
        Retrieves performance insights for a given ad account.

        Args:
            ad_account_id (str): ID of the Facebook Ad Account.
            token (str): Facebook access token with required permissions.
            fields (str): Comma-separated list of metrics to fetch.
            level (str): Aggregation level, e.g., 'campaign'.
            date_preset (str): Facebook date range, e.g., 'last_7d', or "time_range": {"since": "2025-04-01", "until": "2025-04-07"}

        Returns:
            list: List of insight records (dicts).
        """

        url = f"https://graph.facebook.com/v19.0/{ad_account_id}/insights"
        params = {
            "fields": fields,
            "level": level,
            "date_preset": date_preset,
            "access_token": token
        }
        res = requests.get(url, params=params)
        if res.status_code != 200:
            print(f"Error fetching insights for {ad_account_id}: {res.status_code} - {res.text}")
            return []
        return res.json().get("data", [])


    def get_ads_report_dataset(self, date="last_7d") -> list:
        """
        Combines ad insights across all accessible ad accounts into a dataset.
        Calculates cost per result and formats key campaign metrics.

        Args:
            date (str): Facebook date range, e.g., 'last_7d', or "time_range": {"since": "2025-04-01", "until": "2025-04-07"}

        Returns:
            list: A list of dictionaries representing campaign performance.
        """
        dataset = []
        accounts = self.get_ad_accounts()
        # for acc in accounts:
        for acc in accounts:
            insights = self.get_insights(acc["id"], self.access_token, fields="campaign_name,impressions,clicks,spend,actions", date_preset=date)
            for campaign in insights:
                spend = float(campaign.get("spend", 0))
                actions = campaign.get("actions", [])
                # You can change this to 'purchase', 'lead', etc. depending on campaign objective
                action_type = 'link_click'
                result_count = next(
                    (int(action['value']) for action in actions if action.get('action_type') == action_type),
                    0
                )
                cost_per_result = round(spend / result_count, 2) if result_count else None
                dataset.append({
                    "ad_account": acc["id"],
                    "campaign_name": campaign.get("campaign_name"),
                    "impressions": campaign.get("impressions"),
                    "clicks": campaign.get("clicks"),
                    "spend": spend,
                    "results": result_count,
                    "cost_per_result": cost_per_result,
                })
        return dataset

    def main(self) -> None:
        """
        Driver method to fetch and print the ad report dataset.
        Intended for standalone script usage.
        """
        dataset = self.get_ads_report_dataset()
        for row in dataset:
            print(f"Campaign: {row['campaign_name']}, Impressions: {row['impressions']}, Clicks: {row['clicks']}, Spend: {row['spend']}, Results: {row['results']}, Cost per Result: {row['cost_per_result']}\n")
