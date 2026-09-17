"""
Olist E-Commerce Dashboard - AI Insights Generator
----------------------------------------------------
This script takes the key summary numbers from the Power BI dashboard
and sends them to Google's Gemini API to generate a written business
insights report automatically.

HOW TO USE:
1. Paste your Gemini API key in the API_KEY variable below.
2. Run this file: python generate_insights.py
3. It will print the AI-generated insights AND save them to
   'ai_insights_report.txt' in the same folder.
"""

from google import genai

# -----------------------------
# STEP 1: Configure your API key
# -----------------------------
API_KEY = "PASTE_YOUR_GEMINI_API_KEY_HERE"   # <-- replace this with your real key

client = genai.Client(api_key=API_KEY)

# -----------------------------
# STEP 2: Your dashboard's key numbers
# -----------------------------
# These are pulled directly from your Power BI dashboard.
# You can edit these anytime the dashboard numbers change.

dashboard_data = {
    "total_revenue": "₹15.84M",
    "total_orders": "99,440",
    "total_customers": "96,096",
    "average_order_value": "₹160.99",
    "repeat_customer_rate": "3.12%",
    "avg_review_score": "4.09 / 5",
    "avg_delivery_days": 12.50,
    "cancellation_rate": "0.63%",
    "top_product_category": "health_beauty (₹1,441.25K revenue)",
    "second_category": "watches_gifts (₹1,305.54K revenue)",
    "top_state_by_revenue": "SP (São Paulo) - ₹5,921.68K",
    "customer_segments": {
        "High Value": {"count": 4424, "total_revenue": "₹45,94,027.05", "avg_revenue": "₹923.05"},
        "Medium Value": {"count": 27932, "total_revenue": "₹72,84,233.53", "avg_revenue": "₹243.90"},
        "Low Value": {"count": 63064, "total_revenue": "₹50,91,411.47", "avg_revenue": "₹79.66"},
        "No Purchase": {"count": 676, "total_revenue": "₹0"},
    },
    "cohort_retention_insight": (
        "Across every customer cohort from Sep 2016 to Oct 2018, "
        "approximately 98% of purchase activity happens in the customer's "
        "first month. Repeat purchases in later months drop to very small "
        "numbers (tens, sometimes single digits) regardless of cohort size."
    ),
    "review_score_by_state_insight": (
        "Average review scores are consistently high (4.1-4.2 out of 5) "
        "across all states with almost no regional variation, ruling out "
        "service quality as a driver of low repeat purchases."
    ),
}

# -----------------------------
# STEP 3: Build the prompt
# -----------------------------
prompt = f"""
You are a business data analyst. Based on the following e-commerce dashboard
data (from the Olist Brazilian e-commerce dataset), write a clear, professional
business insights summary. 

Structure your response with these sections:
1. Executive Summary (2-3 sentences)
2. Key Findings (bullet points, 4-6 findings)
3. Business Recommendations (3-4 actionable recommendations)

Keep the tone professional but easy to understand. Avoid generic statements -
be specific using the numbers provided.

DASHBOARD DATA:
{dashboard_data}
"""

# -----------------------------
# STEP 4: Call the Gemini API
# -----------------------------
def generate_report():
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    print("Generating AI insights... please wait.\n")
    try:
        report = generate_report()
        print(report)

        # Save to a text file
        with open("ai_insights_report.txt", "w", encoding="utf-8") as f:
            f.write(report)

        print("\n\n✅ Report saved to 'ai_insights_report.txt'")

    except Exception as e:
        print("Something went wrong:", e)
        print("\nCheck that your API key is correct and pasted properly above.")
