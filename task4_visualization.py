import os
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # ---------------------------------------------------------
    # 1 — Setup (2 marks)
    # ---------------------------------------------------------
    input_path = os.path.join("data", "trends_analysed.csv")
    output_dir = "outputs"
    
    # Create the outputs/ directory if it doesn't already exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    if not os.path.exists(input_path):
        print(f"Error: Missing required file '{input_path}'. Please run Task 3 first.")
        return

    # Load analyzed dataset into a Pandas DataFrame
    df = pd.read_csv(input_path)

    # ---------------------------------------------------------
    # 2 — Chart 1: Top 10 Stories by Score (6 marks)
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 6))
    
    # Sort data by score and extract the top 10 highest ranking stories
    top_10 = df.sort_values(by="score", ascending=False).head(10)
    
    # Reverse order so the highest score displays at the very top of the horizontal chart
    top_10 = top_10.iloc[::-1]
    
    # Shorten titles longer than 50 characters to keep our y-axis clean
    short_titles = [t[:47] + "..." if len(str(t)) > 50 else t for t in top_10["title"]]
    
    # Plot horizontal bar chart
    plt.barh(short_titles, top_10["score"], color="skyblue", edgecolor="black")
    plt.title("Top 10 Stories by Score")
    plt.xlabel("Score (Upvotes)")
    plt.ylabel("Story Title")
    plt.tight_layout()
    
    # Always save the file BEFORE calling show() to avoid blank outputs
    plt.savefig(os.path.join(output_dir, "chart1_top_stories.png"))
    plt.close()

    # ---------------------------------------------------------
    # 3 — Chart 2: Stories per Category (6 marks)
    # ---------------------------------------------------------
    plt.figure(figsize=(8, 5))
    
    # Group the total count metrics across category dimensions
    cat_counts = df["category"].value_counts()
    
    # Explicit distinct palette list to color each discrete category bar differently
    bar_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    
    # Render the categorical metrics
    plt.bar(cat_counts.index, cat_counts.values, color=bar_colors[:len(cat_counts)], edgecolor="black")
    plt.title("Number of Stories per Category")
    plt.xlabel("Category")
    plt.ylabel("Story Count")
    plt.xticks(rotation=15)
    plt.tight_layout()
    
    plt.savefig(os.path.join(output_dir, "chart2_categories.png"))
    plt.close()

    # ---------------------------------------------------------
    # 4 — Chart 3: Score vs Comments (6 marks)
    # ---------------------------------------------------------
    plt.figure(figsize=(8, 5))
    
    # Segment dataset into separate variables based on popularity flags
    popular_mask = df["is_popular"] == True
    popular_stories = df[popular_mask]
    non_popular_stories = df[~popular_mask]
    
    # Plot non-popular items as small grey dots
    plt.scatter(non_popular_stories["score"], non_popular_stories["num_comments"], 
                color="darkgray", alpha=0.6, label="Standard Stories", edgecolors="none")
    
    # Overplot popular items as distinct large gold highlights
    plt.scatter(popular_stories["score"], popular_stories["num_comments"], 
                color="gold", alpha=0.8, label="Popular Stories", edgecolors="black", s=60)
                
    plt.title("Story Engagement: Score vs Comments")
    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(os.path.join(output_dir, "chart3_scatter.png"))
    plt.close()

    # ---------------------------------------------------------
    # Bonus — Dashboard (+3 marks)
    # ---------------------------------------------------------
    # Set up a structured 2x2 grid framework for a unified presentation dashboard
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("TrendPulse Dashboard", fontsize=22, fontweight="bold", y=0.98)
    
    # --- Top Left Plot: Horizontal top 10 ---
    axes[0, 0].barh(short_titles, top_10["score"], color="skyblue", edgecolor="black")
    axes[0, 0].set_title("Top 10 Stories by Score", fontsize=12)
    axes[0, 0].set_xlabel("Score")
    
    # --- Top Right Plot: Categories distribution ---
    axes[0, 1].bar(cat_counts.index, cat_counts.values, color=bar_colors[:len(cat_counts)], edgecolor="black")
    axes[0, 1].set_title("Stories per Category", fontsize=12)
    axes[0, 1].set_ylabel("Count")
    axes[0, 1].tick_params(axis='x', rotation=15)
    
    # --- Bottom Left Plot: Scatter plot ---
    axes[1, 0].scatter(non_popular_stories["score"], non_popular_stories["num_comments"], color="darkgray", alpha=0.5)
    axes[1, 0].scatter(popular_stories["score"], popular_stories["num_comments"], color="gold", edgecolor="black", s=50)
    axes[1, 0].set_title("Engagement Distribution Matrix", fontsize=12)
    axes[1, 0].set_xlabel("Score")
    axes[1, 0].set_ylabel("Comments")
    
    # --- Bottom Right Space: Hide the unused grid quadrant ---
    axes[1, 1].axis("off")
    
    # Add an informational project metrics box text overlay inside the blank axis space
    info_box_text = (
        "TrendPulse Pipeline Summary\n"
        "===========================\n"
        f"• Cleaned Stories Analysed: {len(df)}\n"
        f"• Hot Highlight Targets: {len(popular_stories)}\n"
        f"• Global Score Peak: {df['score'].max():,}\n"
        f"• Discussion Thread Peak: {df['num_comments'].max():,}"
    )
    axes[1, 1].text(0.1, 0.4, info_box_text, fontsize=14, family="monospace", va="center")
    
    # Adjust tight layout settings cleanly so that titles and labels never clash
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Final dashboard export dump
    plt.savefig(os.path.join(output_dir, "dashboard.png"), dpi=150)
    plt.close()
    
    print("All charts successfully generated and saved to the 'outputs/' directory!")

if __name__ == "__main__":
    main()
