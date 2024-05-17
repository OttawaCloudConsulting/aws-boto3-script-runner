import boto3

def list_s3_buckets_and_contents():
    # Create a session using default profile
    session = boto3.Session()

    # Create an S3 client
    s3 = session.client('s3')

    # List all buckets
    response = s3.list_buckets()

    # Get the list of bucket names
    buckets = [bucket['Name'] for bucket in response['Buckets']]

    # Print all bucket names
    print("S3 Buckets:")
    for bucket in buckets:
        print(f"  - {bucket}")

    # Check if there is at least one bucket
    if buckets:
        first_bucket_name = buckets[0]
        print(f"\nContents of the first bucket: {first_bucket_name}")

        # List objects in the first bucket
        objects_response = s3.list_objects_v2(Bucket=first_bucket_name)

        if 'Contents' in objects_response:
            for obj in objects_response['Contents']:
                print(f"  - {obj['Key']}")
        else:
            print("  No objects found in the bucket.")
    else:
        print("No S3 buckets found.")

if __name__ == "__main__":
    list_s3_buckets_and_contents()
