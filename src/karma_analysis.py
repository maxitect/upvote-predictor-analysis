import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from urllib.parse import urlparse
from utils.db_connection import get_cursor


def analyse_karma_vs_score():
    print("Starting karma analysis...")
    query = """
    WITH filtered_stories AS (
        SELECT
            i.title,
            i.url,
            i.score,
            i.time,
            i."by" as author,
            u.karma as current_karma,
            u.created as user_created
        FROM hacker_news.items i
        JOIN hacker_news.users u ON i."by" = u.id
        WHERE
            i.type = 'story'
            AND (i.dead IS NULL OR i.dead = false)
    )
    SELECT *
    FROM filtered_stories
    """

    print("Executing database query...")

    try:
        with get_cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        if not results:
            print("No data found matching the criteria")
            return pd.DataFrame()

        print(f"Query returned {len(results)} rows")
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        return pd.DataFrame()

    columns = [
        'title', 'url', 'score', 'time', 'author',
        'current_karma', 'user_created'
    ]

    df = pd.DataFrame(results, columns=columns)

    # Print the first few rows to understand the data structure
    print("\nData sample:")
    print(df.head(2))
    print("\nData types:")
    print(df.dtypes)

    # Convert timestamps to datetime - handle both integer timestamps
    # and pandas Timestamp objects
    def safe_to_datetime(ts):
        if isinstance(ts, (int, float)):
            return datetime.fromtimestamp(ts)
        else:
            # If it's already a timestamp or datetime-like object
            return pd.to_datetime(ts)

    df['post_datetime'] = df['time'].apply(safe_to_datetime)
    df['user_created_datetime'] = df['user_created'].apply(safe_to_datetime)

    # Calculate the reference time (October 2024)
    reference_time = datetime(2024, 10, 1)

    # Extract domain from URL
    def extract_domain(url):
        if pd.isna(url):
            return None
        try:
            domain = urlparse(url).netloc
            return domain.replace('www.', '')
        except (ValueError, AttributeError):
            return None

    df['domain'] = df['url'].apply(extract_domain)

    # Calculate linear interpolation of karma
    # From user creation (0 karma) to October 2024 (current karma)
    def interpolate_karma(row):
        try:
            # Time elapsed between user creation and reference (October 2024)
            total_time_span = (
                reference_time - row['user_created_datetime']).total_seconds()

            if total_time_span <= 0:
                return row['current_karma']

            # Time elapsed between user creation and post time
            post_time_span = (row['post_datetime'] -
                              row['user_created_datetime']).total_seconds()

            # Calculate the karma at post time using linear interpolation
            karma_at_post_time = (
                post_time_span / total_time_span) * row['current_karma']

            # Ensure we don't return negative karma
            return max(0, karma_at_post_time)
        except Exception as e:
            print(f"Error calculating karma for row: {e}")
            return 0  # Default value in case of error

    df['interpolated_karma'] = df.apply(interpolate_karma, axis=1)

    print(f"Total stories analyzed: {len(df)}")
    print(f"Average score: {df['score'].mean():.2f}")
    print(
        f"Average interpolated karma at post time: "
        f"{df['interpolated_karma'].mean():.2f}")

    # Analyze correlation between karma and score
    correlation = df['interpolated_karma'].corr(df['score'])
    print(
        f"Correlation between interpolated karma and score: {correlation:.4f}")

    # Visualize the relationship
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='interpolated_karma', y='score', data=df, alpha=0.5)
    plt.title('Relationship Between Author Karma (@ post time) and Post Score')
    plt.xlabel('Interpolated Karma at Post Time')
    plt.ylabel('Score')
    plt.xscale('log')  # Use log scale for karma as it ßcan vary widely

    plt.savefig('karma_vs_score.png')
    print("Plot saved as 'karma_vs_score.png'")

    # Bin karma values and analyze average scores
    karma_bins = [0, 100, 500, 1000, 5000, 10000, 50000, float('inf')]
    df['karma_bin'] = pd.cut(df['interpolated_karma'], bins=karma_bins)
    karma_score = df.groupby('karma_bin').agg({
        'score': ['mean', 'median', 'count']
    }).reset_index()

    print("\nScores by karma bins:")
    print(karma_score)

    # Visualize karma bins vs average score
    plt.figure(figsize=(12, 6))
    sns.barplot(x='karma_bin', y=('score', 'mean'), data=karma_score)
    plt.title('Average Score by Author Karma Level')
    plt.xlabel('Karma Range')
    plt.ylabel('Average Score')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('karma_bins_vs_score.png')
    print("Plot saved as 'karma_bins_vs_score.png'")

    # Time series analysis - how does the karma-score
    # relationship change over time?
    try:
        df['year'] = df['post_datetime'].dt.year
        yearly_correlation = df.groupby('year').apply(
            lambda x: x['interpolated_karma'].corr(
                x['score']) if len(x) > 5 else None
        ).reset_index()
        yearly_correlation.columns = ['year', 'karma_score_correlation']
        yearly_correlation = yearly_correlation.dropna()
    except Exception as e:
        print(f"Error in time series analysis: {e}")
        yearly_correlation = pd.DataFrame(
            columns=['year', 'karma_score_correlation'])

    print("\nKarma-score correlation by year:")
    print(yearly_correlation)

    plt.figure(figsize=(10, 6))
    sns.lineplot(x='year', y='karma_score_correlation',
                 data=yearly_correlation, marker='o')
    plt.title('Karma-Score Correlation by Year')
    plt.xlabel('Year')
    plt.ylabel('Correlation Coefficient')

    plt.savefig('karma_correlation_by_year.png')
    print("Plot saved as 'karma_correlation_by_year.png'")

    # Return the processed dataframe for potential further analysis
    result_df = df[['title', 'domain', 'score', 'post_datetime',
                    'author', 'interpolated_karma']]

    return result_df


if __name__ == "__main__":
    analyse_karma_vs_score()
