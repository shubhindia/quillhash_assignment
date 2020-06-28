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
        sh "docker build -t shubhindia/quillhashassignment ."
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
			node("shubhindia"){
            
	   	    sh "cd /opt;./deployment.py ${params.Service_Name} ${params.Application_Name} $env.Environment_Name $env.dev_nexus_ip $BUILD_NUMBER ${params.Language} " 
			sh "cd /opt;sudo ansible-playbook ${params.Application_Name}-${params.Service_Name}.yml --extra-vars 'variable_host=$env.Environment_Name variable_serv=${params.Service_Name} variable_app=${params.Application_Name}'"
			

       }
    }
} 


def quote() 
{
    stage('quote') 
    {
        echo 'Please check the jenkins pipeline.'
    }
}
