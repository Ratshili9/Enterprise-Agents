from tools.recommendation_tools import generate_strategic_recommendations


class RecommendationAgent:
    """
    The Recommendation Agent synthesizes information from all previous steps 
    (Insights, Search, ML) to generate high-value, actionable recommendations.
    """

    def __init__(self):
        pass

    def run(self, context: dict) -> bool:
        """
        Orchestrates the recommendation generation and saves the report path to context.
        """
        print("--- [AGENT:Rec] Synthesizing final recommendations ---")

        if 'ml_reports' not in context:
            print(
                "Recommendation Agent Error: Missing ML analysis results. Cannot proceed.")
            # Still generate a basic recommendation, but flag failure
            context['recommendation_report'] = "ML results were unavailable, unable to provide data-driven recommendations."
            return False

        try:
            # 1. Generate the recommendation content
            recommendation_content = generate_strategic_recommendations(
                context)

            # 2. Save the content to context
            context['recommendation_report'] = recommendation_content

            print("--- [AGENT:Rec] Recommendations successfully generated ---")
            return True

        except Exception as e:
            print(f"Recommendation Agent Error: {e}")
            context['recommendation_report'] = f"Error generating recommendations: {e}"
            return False
