# Dataset Hunch Analysis

This project tests various hunches about factors that might influence the score of posts in the dataset.

## Setup

1. Create environment from root:

   ```
   conda env create -f environment.yml
   ```

2. Activate environment:

   ```
   conda activate upvote-predictor
   ```

3. Make sure you have access to the PostgreSQL database at:
   ```
   postgres://sy91dhb:g5t49ao@178.156.142.230:5432/hd64m1ki
   ```

## Project Structure

- `utils/db_connection.py` - Contains database connection utilities
- `title_length_score.py` - Analyses relationship between title length and score
- `author_posts_score.py` - Analyses relationship between author activity and score
- `domain_popularity.py` - Analyses relationship between domains and score
- `time_patterns.py` - Analyses time-based patterns in scores
- `main.py` - Entry point for running analyses

## Usage

Run all analyses:

```
python main.py --all
```

Or run specific analyses:

```
python main.py --title --author
```

Available options:

- `--title`: Analyze title length vs score
- `--author`: Analyze author activity vs score
- `--domain`: Analyze domain popularity vs score
- `--time`: Analyze time patterns vs score

## Hunches Being Tested

1. Are shorter titles conducive to a higher score?

   - Analyzes correlation between title length and post score

2. Does posting frequency affect scores?

   - Examines if prolific authors get higher scores

3. Are certain domains more popular?

   - Compares scores across different domains
   - Checks if official news websites get better scores than blogs

4. Are patterns in recent posts more indicative than older ones?
   - Analyzes score trends over time
   - Compares patterns between newer and older posts

## Output

Each analysis will:

- Print key statistics to console
- Generate visualization plots saved as PNG files
