import groovy.json.JsonOutput
import groovy.transform.Field
import groovy.json.JsonSlurper

node ('shubhindia')
		{
		JenkinsStages("master","python")
}
def JenkinsStages(branchName,language)
{
   echo "branchName -"+branchName
   echo language
	stage('stages'){
		Checkout()
		Create_Image()
		Image_Push()
		Deployment()
		

  }	
	
}

def Checkout() 
{
    stage('Checkout')
    {
    
        checkout scm
        
    }
    
}	

def Create_Image()
{
    stage('Create_Image') 
    {
        sh "cd quillhashassignment;docker build -t shubhindia/quillhashassignment ."
    }
}

def Image_Push() 
{
    stage('Image_Push')
    {
            sh "docker push shubhindia/quillhashassignment:latest"
    }
}


def Deployment() 
{
    stage('Deployment')
    {
	   	    sh "cd /home/nts/deployments;python3 deployment.py shubhindia quillhashassignment quillhash"
	            sh "cd /home/nts/deployments;ansible-playbook playbook-quillhashassignment.yml"
    }
} 

