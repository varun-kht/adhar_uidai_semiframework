import pandas as pd

from load_data import load_processed_data
from features import generate_features
from models import compute_anomaly_score, compute_trend_score
from scoring import compute_priority_score, add_explanations


def main():
   
    # Step 1: Load cleaned, merged dataset 
    df = load_processed_data("data/processed/aadhaar_state_monthly.csv")

 
    # Step 2: Feature Engineering
    df = generate_features(df)
 
    # Step 3: Compute Analytical Scores
    trend_df = compute_trend_score(df)
    anomaly_df = compute_anomaly_score(df)

     
    # Step 4: Merge Scores
     
    score_df = (
        trend_df.merge(anomaly_df, on="state", how="inner")
        .merge(
            df.groupby("state")["biometric_volume"].mean().reset_index(),
            on="state",
            how="inner",
        )
    )

    
    # Step 5: Priority Scoring + Ranking
    
    scored_df = compute_priority_score(score_df)

    
    # Step 6: Explainability Layer
     
    final_df = add_explanations(scored_df)
 
    # Step 7: Save Final Output
    
    output_path = "data/processed/state_priority_ranking.csv"
    final_df.to_csv(output_path, index=False)

    # Debug / Verification (run once)
    print("Pipeline completed successfully.")
    print("Final columns saved:")
    print(final_df.columns.tolist())
    print("Top 5 States by Priority:")
    print(final_df.head(5))


if __name__ == "__main__":
    main()
