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
		switch(branchName){
	
		case "develop":
		
				 env.slave = "jenkins-slave01"
				 env.Environment_Name="dev"
         
				 Checkout()
				switch(language){
		
			case "springboot":
			
					Build()
					Junit()
					Sonarqube()
					
					break; 
			case "node":
			
					Nodeunit()
					NodeBuild()
					sonarPy()
				
					break;
					
			case "python":

					sonarPy()
					
					break;
					
			case "dotnetcore":

					// Xunit()
					DotNetBuild()
					Sonarqube()
					
					break;
               
               
            default: 
                 break;
		
				}
				
				 Fortify()     
                Create_Image()
                //ContainerSecurity()
                Dev_Image_Push()
                Deployment()
				
				//Add Quality_Gate and Deploy to QA environment
				 env.Environment_Name="qa"
				 Quality_Gate()  // Sonarqube Quality_Gate Build Breakerr
				 Deployment()
		
			break;
			
		case "release":

				 env.slave = "jenkins-slave01"
				 env.Environment_Name="preprod"
				 Checkout()
				 
				 switch(language){
					
					case "springboot":
					
						  Build()
						  Junit()
						  Sonarqube()
					
						break;
						
					case "node":
					
						Nodeunit()
						sonarPy()
						NodeBuild()

						break;

					case "python":
					
						Fortify()
						sonarPy()

						break;
						
					case "dotnetcore":
						   
						   // Xunit()
						  DotNetBuild()
						  DotNetSonar()

						break;
						
					default:

						break;

				}
					 Fortify()
					 Quality_Gate()
					 Create_Image()
					 Prod_Image_Push()
					 Deployment()		
			break;
			
		case "master":	
		
				env.slave = "jenkins-slave01"
				env.Environment_Name="prod"
				Deployment()
				
			break;
			
		default:	
			break;

	}
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
        sh "cd ${params.Service_Name} ; sudo docker build -t shubhindia/quillhashassignment ."
    }
}

def Image_Push() 
{
    stage('Image_Push')
    {
   // echo "${git_ver}"
        withCredentials([usernamePassword(credentialsId: 'nexus_prod', usernameVariable: 'NEXUS_USER' , passwordVariable: 'NEXUS_PASSWORD' )]) 
        {
            sh "sudo docker login -u ${NEXUS_USER} -p ${NEXUS_PASSWORD} $env.dev_nexus_ip"
            sh "sudo docker tag  $params.Service_Name $env.dev_nexus_ip/$params.Application_Name-$params.Service_Name"
            sh "sudo docker push $env.dev_nexus_ip/$params.Application_Name-$params.Service_Name:latest"
        }
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
