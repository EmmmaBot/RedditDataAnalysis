import praw
import pandas as pd
from datetime import datetime

class CommentCollectionMode(Enum):
    ALL_COMMENTS = 0
    TOP_LEVEL_COMMENTS = 1
    BOTH = 2

def fetch_posts(subreddit, limit: int = None, search_keyword: str = None):
    if search_keyword:
        return subreddit.search(search_keyword, limit=limit)
    return subreddit.new(limit=limit)

def get_comments(post, collect_all_comments: bool = False):
    post.comments.replace_more(limit=None)
    return [comment.body for comment in post.comments if collect_all_comments or comment.is_root]

def collect_posts_and_comments(limit: int = None,
                               comment_mode: CommentCollectionMode = CommentCollectionMode.TOP_LEVEL_COMMENTS,
                               search_keyword: str = None):
    all_posts = []
    posts = fetch_posts(subreddit, limit, search_keyword)

    for post in posts:
        all_comments = []
        top_level_comments = []

        if comment_mode in (CommentCollectionMode.ALL_COMMENTS, CommentCollectionMode.BOTH):
            all_comments = get_comments(post, True)
        if comment_mode in (CommentCollectionMode.TOP_LEVEL_COMMENTS, CommentCollectionMode.BOTH):
            top_level_comments = get_comments(post, False)

        all_posts.append([
            post.title,
            post.score,
            post.id,
            post.url,
            post.num_comments,
            len(top_level_comments),
            post.selftext,
            datetime.fromtimestamp(post.created_utc),
            all_comments,
            top_level_comments
        ])
    return all_posts

# Reddit API credentials
client_id = 'your_client_id'
client_secret = 'your_client_secret'
user_agent = 'your_user_agent'

# Initialize PRAW
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

subreddit_name = "YourSubreddit"
search_keyword = "YourSearchKeyword"

subreddit = reddit.subreddit(subreddit_name)

# Example Usage
posts_and_comments = collect_posts_and_comments(search_keyword=search_keyword, limit=None, comment_mode=CommentCollectionMode.BOTH)

print(f'Total number of posts: {len(posts_and_comments)}')

posts_df = pd.DataFrame(posts_and_comments,
                        columns=['Title', 'Score', 'ID', 'URL', 'Total_Num_Comments', 'Num_Top_Level_Comments', 'Body', 'Created', 'Comments_all', 'Comments_top_level'])

# Save sorted data by the 'Created' column
posts_df_sorted = posts_df.sort_values(by='Created', ascending=False)

# Save to a CSV file
posts_df_sorted.to_csv(f'{subreddit_name}_posts_and_comments_sorted.csv', index=False, encoding='utf-8')
