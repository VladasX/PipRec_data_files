from github import Github
import json

# Create a Github instance:
g = Github("insert_token_here")

# Read project names to scrape urls from
with open("data/projects.csv", 'r') as f:
    f.readline()
    projects = f.read().splitlines()

result = {}
project_count = len(projects)
count = 1

# Get all of the contents of the repository recursively
for proj in projects:
    try:
        file_urls = []
        repo = g.get_repo(proj)
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                # Save only python urls
                if file_content.path.lower().endswith(".py"):
                    file_urls.append(file_content.html_url)
        result[proj] = file_urls
        print("{}/{} projects done".format(count, project_count))
        count += 1
    except:
        # Stop if we reached the limit
        print("Limit reached, stopped at {} project".format(count))
        break


# Save data
with open("data/urls.json", 'w') as outfile:
    json.dump(result, outfile)


