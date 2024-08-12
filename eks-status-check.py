import boto3

client = boto3.client('eks',region_name="us-east-1" )

clusters = client.list_clusters()
print(clusters['clusters'])

for cluster in clusters:
    response = client.describe_cluster(
        name=cluster
    )
    cluster_info = response['cluster']
    cluster_status = cluster_info['status']
    cluster_endpoint = cluster_info['endpoint']
    cluster_version = cluster_info['version']

    print(f"Cluster {cluster} {cluster_status} {cluster_version}")
    print(f"{cluster_endpoint}")