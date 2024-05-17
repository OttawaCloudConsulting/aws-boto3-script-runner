import boto3

def list_ec2_instances():
    # Create a session using default profile
    session = boto3.Session()

    # Create an EC2 client
    ec2 = session.client('ec2')

    # Describe EC2 instances
    response = ec2.describe_instances()

    print("EC2 Instances:")

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # Get the instance ID
            instance_id = instance['InstanceId']

            # Get the instance name from tags
            instance_name = None
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        instance_name = tag['Value']
                        break

            # Print the instance name (or instance ID if name is not set)
            if instance_name:
                print(f"  - Instance Name: {instance_name}")
            else:
                print(f"  - Instance ID: {instance_id}")

if __name__ == "__main__":
    list_ec2_instances()
