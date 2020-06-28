#/usr/bin/python3
import os
import sys
image_repo = sys.argv[1]
service_name = sys.argv[2]
namespace = sys.argv[3]
path = "./"

def create_yamls():
    print("Creating deployment yaml")
    f = open("deployment-"+service_name+".yaml", "a")
    f.write("apiVersion: v1\n")
    f.write("kind: Service\n")
    f.write("metadata:\n")
    f.write("  name: "+service_name+"-service\n")
    f.write("  namespace: "+namespace+"\n")
    f.write("spec:\n")
    f.write("  selector:\n")
    f.write("    app: "+service_name+"\n")
    f.write("  type: LoadBalancer\n")
    f.write("  ports:\n")
    f.write("  - name: service-http\n")
    f.write("    port: 8080\n")
    f.write("    protocol: TCP\n")
    f.write("\n")
    f.write("---\n")
    f.write("\n")
    f.write("apiVersion: apps/v1\n")
    f.write("kind: Deployment\n")
    f.write("metadata:\n")
    f.write("  name: "+service_name+"\n")
    f.write("  namespace: "+namespace+"\n")
    f.write("  labels:\n")
    f.write("    name: "+service_name+"\n")
    f.write("spec:\n")
    f.write("  replicas: 1\n")
    f.write("  selector:\n")
    f.write("    matchLabels:\n")
    f.write("      app: "+service_name+"\n")
    f.write("  template:\n")
    f.write("    metadata:\n")
    f.write("     labels:\n")
    f.write("       app: "+service_name+"\n")
    f.write("    spec:\n")
    f.write("      containers:\n")
    f.write("      - name: "+service_name+"\n")
    f.write("        image: "+image_repo+"/"+service_name+"\n")
    f.write("        imagePullPolicy: Always\n")
    f.write("        ports:\n")
    f.write("        - containerPort: 8080\n")
    f.close()

    print("Creating ansible playbook")
    f = open("playbook-"+service_name+".yml", "a")
    f.write("- hosts:  localhost\n")
    f.write("\n")
    f.write("  tasks:\n")
    f.write("  - name: make sure we are in correct directory\n")
    f.write("    shell: cd /home/nts/deployments\n")
    f.write("  - name: delete old deployment\n")
    f.write("    shell: kubectl delete -f deployment-quillhashassignment.yaml\n")
    f.write("    ignore_errors: yes\n")
    f.write("  - name: apply k8s yaml\n")
    f.write("    shell: kubectl apply -f deployment-quillhashassignment.yaml\n")

if os.path.exists(path+"deployment-"+service_name+".yaml"):
    print("Already exists")
else:
    create_yamls()
