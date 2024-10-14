import requests

# Base URL of your Flask application
base_url = "http://127.0.0.1:5000"  # Adjust this if your app is running on a different host or port

# Influencer name and destination URL
influencer_name = "@alex"
destination_url = "https://laeuphoria.com"

def generate_link():    
    # Endpoint URL
    url = f"{base_url}/generate_link/{influencer_name}"

    # POST data
    data = {
        "destination_url": destination_url
    }

    # Send POST request
    response = requests.post(url, data=data)

    # Check the response
    if response.status_code == 200:
        print("Success!")
        print(response.text)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def go_to_link(unique_code):
    url = f"{base_url}/link/{unique_code}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Success!")

def track_influencer(influencer_name):
    url = f"{base_url}/track_influencer/{influencer_name}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Success!")
        print(response.text)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # generate_link()
    go_to_link("5A0230")
    track_influencer("@alex")
