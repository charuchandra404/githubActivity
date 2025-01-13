import argparse
import urllib.request
import urllib.error
import json

def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"

    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.load(response)
                return data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: GitHub user '{username}' not found.")
        else:
            print(f"HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
    return None

def display_activity(activity):
    if not activity:
        print("No recent activity found.")
        return
    for event in activity:
        event_type = event.get("type")
        repo_name = event["repo"]["name"]
        if event_type == "PushEvent":
            commit_count = len(event["payload"]["commits"])
            print(f"Pushed {commit_count} commits to {repo_name}")
        elif event_type == "IssuesEvent":
            action = event["payload"]["action"]
            print(f"{action.capitalize()} an issue in {repo_name}")
        elif event_type == "WatchEvent":
            print(f"Starred {repo_name}")
        elif event_type == "ForkEvent":
            print(f"Forked {repo_name}")
        elif event_type == "CreateEvent":
            ref_type = event["payload"]["ref_type"]
            print(f"Created a {ref_type} in {repo_name}")
        else:
            print(f"{event_type.replace('Event', '')} in {repo_name}")

def main():
    parser = argparse.ArgumentParser(description="GitHub Activity CLI")
    parser.add_argument("username",type=str, help="GitHub username")
    args = parser.parse_args()

    print(f"Fetching recent activity for GitHub user '{args.username}'...")
    activity = fetch_github_activity(args.username)
    if activity:
        print("\nRecent Activity:")
        display_activity(activity)
    else:
        print("Unable to fetch activity. Please try again later.")

if __name__ == "__main__":
    main()








