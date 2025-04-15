import argparse
from src.title_length_score import analyse_title_length_vs_score
from src.author_posts_score import analyse_author_activity_vs_score
from src.domain_popularity import analyse_domain_popularity
from src.time_patterns import analyse_time_patterns
from src.karma_analysis import analyse_karma_vs_score


def main():
    parser = argparse.ArgumentParser(description='Analyze dataset hunches')
    parser.add_argument('--all', action='store_true', help='Run all analyses')
    parser.add_argument('--title', action='store_true',
                        help='Analyze title length vs score')
    parser.add_argument('--author', action='store_true',
                        help='Analyze author activity vs score')
    parser.add_argument('--domain', action='store_true',
                        help='Analyze domain popularity vs score')
    parser.add_argument('--time', action='store_true',
                        help='Analyze time patterns vs score')
    parser.add_argument('--karma', action='store_true',
                        help='Analyze karma vs score')

    args = parser.parse_args()

    if args.all or not any([
        args.title, args.author, args.domain, args.time, args.karma
    ]):
        print("\n=== Running all analyses ===\n")
        run_all_analyses()
    else:
        if args.title:
            print("\n=== Analyzing title length vs score ===\n")
            analyse_title_length_vs_score()

        if args.author:
            print("\n=== Analyzing author activity vs score ===\n")
            analyse_author_activity_vs_score()

        if args.domain:
            print("\n=== Analyzing domain popularity vs score ===\n")
            analyse_domain_popularity()

        if args.time:
            print("\n=== Analyzing time patterns vs score ===\n")
            analyse_time_patterns()

        if args.karma:
            print("\n=== Analyzing karma vs score ===\n")
            analyse_karma_vs_score()


def run_all_analyses():
    print("\n=== Analyzing title length vs score ===\n")
    analyse_title_length_vs_score()

    print("\n=== Analyzing author activity vs score ===\n")
    analyse_author_activity_vs_score()

    print("\n=== Analyzing domain popularity vs score ===\n")
    analyse_domain_popularity()

    print("\n=== Analyzing time patterns vs score ===\n")
    analyse_time_patterns()

    print("\n=== Analyzing karma vs score ===\n")
    analyse_karma_vs_score()


if __name__ == "__main__":
    main()
