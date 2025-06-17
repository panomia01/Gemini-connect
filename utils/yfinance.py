import requests
import yfinance as yf

def get_esg_scores(ticker: str):
    """
    Fetch the total ESG score for a given ticker symbol using yfinance.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        float: The total ESG score, or None if no data is available.
    """
    try:
        stock = yf.Ticker(ticker)
        esg_data = stock.sustainability
        if esg_data is None or esg_data.empty:
            return None  # Return None if ESG data is unavailable
        esg_dict = esg_data.to_dict()  # Convert pandas DataFrame to dictionary
        esg_scores = esg_dict.get("esgScores", {})  # Extract the nested ESG scores dictionary
        return esg_scores.get("totalEsg")  # Return the totalEsg value
    except Exception as e:
        raise Exception(f"Failed to fetch ESG scores for ticker '{ticker}': {e}")