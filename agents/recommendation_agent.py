from tools.recommendation_tools import generate_strategic_recommendations

class RecommendationAgent:
    """
    The Recommendation Agent reads the ML results and creates
    the final business recommendations.
    """

    def __init__(self):
        pass

    def run(self, context: dict) -> bool:
        print("\n--- [AGENT:REC] Generating strategic recommendations ---")

        if "ml_reports" not in context:
            print("Recommendation Agent Error: Missing ML reports.")
            context["recommendation_report"] = (
                "⚠️ ML results unavailable — unable to generate data-driven recommendations."
            )
            return False

        try:
            rec_text = generate_strategic_recommendations(context)
            context["recommendation_report"] = rec_text

            print("--- [AGENT:REC] Recommendations generated successfully ---\n")
            return True

        except Exception as e:
            print(f"Recommendation Agent Error: {e}")

            context["recommendation_report"] = (
                f"Error while generating recommendations: {e}"
            )
            return False
