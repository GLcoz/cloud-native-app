from kubernetes import client, config
import boto3

# Specify the region when creating the ECR client
ecr_client = boto3.client('ecr', region_name='us-east-1')  # Ensure 'us-east-1' is your desired region

# Load Kubernetes configuration from a specific file
config.load_kube_config(config_file="C:\\path\\to\\your\\kubeconfig")  # Replace with the path to your kubeconfig file

# Create a Kubernetes API client
api_client = client.ApiClient()

# Define the deployment
deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="my-flask-app"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "my-flask-app"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "my-flask-app"}
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-flask-container",
                        image="568373317874.dkr.ecr.us-east-1.amazonaws.com/my_monitoring_app_image:latest",
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    )
)

# Create the deployment
apps_v1_api = client.AppsV1Api(api_client)
apps_v1_api.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

# Define the service
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="my-flask-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "my-flask-app"},
        ports=[client.V1ServicePort(port=5000, target_port=5000)]
    )
)

# Create the service
core_v1_api = client.CoreV1Api(api_client)
core_v1_api.create_namespaced_service(
    namespace="default",
    body=service
)

print("Deployment and service created successfully.")
