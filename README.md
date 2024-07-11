# Reddit Data Collector

## Description

This script fetches posts and comments from a specified subreddit using PRAW (Python Reddit API Wrapper) and processes the data into a CSV file. It includes options to search for posts with specific keywords and to collect all or only top-level comments.

## Prerequisites

- Python 3.x
- PRAW
- pandas

## Installation

1. **Clone the repository:**

    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install the required libraries:**

    ```sh
    pip install praw pandas
    ```

## Configuration

1. **Reddit API Credentials:**

    Obtain `client_id`, `client_secret`, and `user_agent` from your Reddit account's [App Preferences](https://www.reddit.com/prefs/apps). Update these variables in the script:

    ```python
    client_id = 'your_client_id'
    client_secret = 'your_client_secret'
    user_agent = 'your_user_agent'
    ```

2. **Subreddit and Search Keyword:**

    Set the desired subreddit and search keyword:

    ```python
    subreddit_name = "YourSubreddit"
    search_keyword = "YourSearchKeyword"
    ```

## Usage

1. **Initialize Reddit API:**

    ```python
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    subreddit = reddit.subreddit(subreddit_name)
    ```

2. **Collect Posts and Comments:**

    Use the `collect_posts_and_comments` function to fetch data. Customize the parameters as needed:

    ```python
    from enum import Enum

    class CommentCollectionMode(Enum):
        ALL_COMMENTS = 0
        TOP_LEVEL_COMMENTS = 1
        BOTH = 2

    posts_and_comments = collect_posts_and_comments(search_keyword=search_keyword, limit=None, comment_mode=CommentCollectionMode.BOTH)
    ```

3. **Save Data to CSV:**

    The collected data is saved to a CSV file, sorted by the creation date:

    ```python
    posts_df = pd.DataFrame(posts_and_comments,
                            columns=['Title', 'Score', 'ID', 'URL', 'Total_Num_Comments', 'Num_Top_Level_Comments', 'Body', 'Created', 'Comments_all', 'Comments_top_level'])
    posts_df_sorted = posts_df.sort_values(by='Created', ascending=False)
    posts_df_sorted.to_csv(f'{subreddit_name}_posts_and_comments_sorted.csv', index=False, encoding='utf-8')
    ```

## Example

```python
import praw
import pandas as pd
from datetime import datetime
from enum import Enum

class CommentCollectionMode(Enum):
    ALL_COMMENTS = 0
    TOP_LEVEL_COMMENTS = 1
    BOTH = 2

def fetch_posts(subreddit, limit: int = None, search_keyword: str = None):
    if search_keyword:
        r
