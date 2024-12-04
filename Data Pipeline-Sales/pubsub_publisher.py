from google.cloud import pubsub_v1
import json
import time
import random

# GCP Project ID and Pub/Sub Topic
project_id = "nth-suprstate-438619-c9"
topic_id = "sales-events-topic"

# Initialize Pub/Sub Publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Sample Data Generator
def generate_event():
    event_types = ["purchase", "add_to_cart", "view_item"]
    return {
        "event_id": str(random.randint(1000, 9999)),
        "user_id": f"user_{random.randint(1, 100)}",
        "item_id": f"item_{random.randint(1, 50)}",
        "event_type": random.choice(event_types),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

def publish_messages():
    print(f"Publishing messages to {topic_path}...")
    while True:
        # Generate a new sales event
        event = generate_event()
        data = json.dumps(event).encode("utf-8")
        
        # Publish the message
        future = publisher.publish(topic_path, data)
        print(f"Published: {event}")
        
        # Wait 1 second before sending the next message
        time.sleep(1)

if __name__ == "__main__":
    publish_messages()
