import requests

def get_filtered_posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    
    response = requests.get(url)
    if response.status_code == 200:
        posts = response.json()
        filtered_posts = [
            post for post in posts
            if len(post['title'].split()) <= 6 and len(post['body'].split('\n')) <= 3
        ]
        for post in filtered_posts:
            print(f"Title: {post['title']}\nBody: {post['body']}\n")
    else:
        print(f"Failed to fetch posts, status code {response.status_code}")

def create_post():
    url = "https://jsonplaceholder.typicode.com/posts"
    
    new_post = {
        "title": "New Post Title",
        "body": "This is the body of the new post. It contains less than 3 lines.",
        "userId": 1
    }
    
    response = requests.post(url, json=new_post)
    if response.status_code == 201:
        print("Post created successfully!")
        print(response.json())
    else:
        print(f"Failed to create post, status code {response.status_code}")

def update_post(post_id):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    
    updated_post = {
        "id": post_id,
        "title": "Updated Post Title",
        "body": "This is the updated body of the post.",
        "userId": 1
    }
    
    response = requests.put(url, json=updated_post)
    if response.status_code == 200:
        print("Post updated successfully!")
        print(response.json())
    else:
        print(f"Failed to update post, status code {response.status_code}")

def delete_post(post_id):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    
    response = requests.delete(url)
    if response.status_code == 200:
        print(f"Post {post_id} deleted successfully!")
    else:
        print(f"Failed to delete post {post_id}, status code {response.status_code}")

def main():
    print("Fetching and filtering posts...\n")
    get_filtered_posts()
    
    print("\nCreating a new post...\n")
    create_post()
    
    print("\nUpdating a post...\n")
    update_post(1)
    
    print("\nDeleting a post...\n")
    delete_post(1)

if __name__ == "__main__":
    main()
