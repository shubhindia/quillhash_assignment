import groovy.json.JsonOutput
import groovy.transform.Field
import groovy.json.JsonSlurper

node ('shubhindia')
		{
        try {

		
					statusFlag = false

			parameters 
			{
				   choice(choices: 'springboot\ndotnetcore\npython\nnode', description: 'Select the application language', name: 'Language')
				   string(name: 'Application_Name', description: 'Please Provide Application Name', defaultValue: 'applicationname-ms')
				   string(name: 'Service_Name', defaultValue: 'Please Provide Service Name', description: 'Which service needs to deploy')
				   choice(choices: 'develop\nqatest\nrelease\nmaster', description: 'Select the Branch Name' , name: 'Branch_Name')
			}
			
			
			JenkinsStages("${Branch_Name}","${Language}")
			
			 
		

	}catch (exc){
 
    statusFlag = true
	RfabricErr(exc)
}
finally {

	if(!statusFlag){
		RfabricSucc()
		}
 
}
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

def Junit() 
{
    stage('Junit') 
    {
        sh "cd ${params.Service_Name} ; mvn test"
    }
}

def Build() 
{
    stage('Build') 
    {
       sh "cd ${params.Service_Name} ; mvn clean package -Dmaven.test.skip=true" 
    }
}


def Fortify() 
{
    stage('Fortify') {
       node ('jenkins-slave01') {
           checkout scm
             }
         node ('jenkins-slave01') {
         sh '/opt/HPE_Security/Fortify_SCA_and_Apps_17.20/bin/sourceanalyzer -b test -clean'
         sh "/opt/HPE_Security/Fortify_SCA_and_Apps_17.20/bin/sourceanalyzer -b test $WORKSPACE/${params.Service_Name}"
         sh '/opt/HPE_Security/Fortify_SCA_and_Apps_17.20/bin/sourceanalyzer -b test -export-build-session file.mbs'
         sh '/opt/HPE_Security/Fortify_SCA_and_Apps_17.20/bin/cloudscan -sscurl https://entssc.ril.com/ssc -ssctoken 94724cf3-01b9-4e37-bf24-5760519c4d70 - start -upload -versionid 10998 -uptoken 8895f7e0-ddb7-49c5-beee-723d1d239761 -b test -scan -autoheap -build-label Xmx2G -build-project CPRfabricTesting -build-version 01' 
     		 }
         }
}


def Xunit(){
     stage('Xunit') 
    {
		echo "This is Xunit"
		//sh "cd ${params.Service_Name} ; dotnet clean ; dotnet test" 
    }
}

def DotNetBuild(){
    stage('Build') 
    {
		echo "This is DotNetBuild"
		sh "cd ${params.Service_Name} ; dotnet publish -c release -r linux-x64 --self-contained -o dll"
    }
}

def DotNetSonar(){
    stage('Build') 
    {
		echo "This is Sonar"
		//sh "cd ${params.Service_Name} ; dotnet publish -c release -r linux-x64 --self-contained -o dll"
    }
}



def sonarPy(){
    
    stage('Sonar') {
                 withSonarQubeEnv('sonar') {
                     sh "${scannerHome}/bin/sonar-scanner -e -Dsonar.projectName=${params.Service_Name} -Dsonar.projectKey=${params.Service_Name} -Dsonar.sources=${params.Service_Name} -Dsonar.sources=${params.Service_Name} "
                }
    }
}

def Nodeunit(){
    stage('Nodeunit') 
    {
		echo "This is Nodeunit"
    }
}
def NodeBuild(){
    stage('NodeBuild') 
    {
		echo "This is NodeBuild"
    }
}

def Sonarqube() 
{
    stage('Sonarqube') 
    {
            
        withSonarQubeEnv('sonar') 
        {
                
                sh "cd ${params.Service_Name} ; ${scannerHome}/bin/sonar-scanner -e -Dsonar.projectName=${params.Service_Name} -Dsonar.projectKey=${params.Service_Name} -Dsonar.sources=${workspace}/${params.Service_Name}  -Dsonar.java.binaries=target/classes"
             
        }
    }
}

def Quality_Gate() 
{
    stage("Quality_Gate")
    {
        sleep "10"
          timeout(time: 1, unit: 'HOURS') 
          {
              def qg = waitForQualityGate()
              if (qg.status == "ERROR") 
              {
                  error "Pipeline aborted due to quality gate failure: ${qg.status}"
              }
          }
      }   
}

def ContainerSecurity(){
		stage ('ContainerSecurity'){
                 aquaMicroscanner imageName:"'$params.Service_Name:latest'" , notCompliesCmd:'exit 0', onDisallowed:'pass',outputFormat:'pdf'
                      
			}
	}	


def Create_Image()
{
    stage('Create_Image') 
    {
        sh "cd ${params.Service_Name} ; sudo docker build --tag=${params.Service_Name} ."
    }
}

def Dev_Image_Push() 
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

def Prod_Image_Push() 
{
    stage('Image_Push') 
    {
        withCredentials([usernamePassword(credentialsId: 'nexus_prod', usernameVariable: 'NEXUS_USER' , passwordVariable: 'NEXUS_PASSWORD' )]) 
        {
            sh "sudo docker login -u ${NEXUS_USER} -p ${NEXUS_PASSWORD} $env.prod_nexus_ip"
            sh "sudo docker tag  $params.Service_Name $env.prod_nexus_ip/${params.Application_Name}-$params.Service_Name"
            sh "sudo docker push $env.prod_nexus_ip/${params.Application_Name}-$params.Service_Name:latest"
        }
    }
}

def Deployment() 
{
    stage('Deployment')
    {
			node("ansible-slave01"){
            
	   	    sh "cd /opt;./deployment.py ${params.Service_Name} ${params.Application_Name} $env.Environment_Name $env.dev_nexus_ip $BUILD_NUMBER ${params.Language} " 
			sh "cd /opt;sudo ansible-playbook ${params.Application_Name}-${params.Service_Name}.yml --extra-vars 'variable_host=$env.Environment_Name variable_serv=${params.Service_Name} variable_app=${params.Application_Name}'"
			

       }
    }
} 
 

@NonCPS
def getCommitedChanges() {
    MAX_MSG_LEN = 100
    def changeString = ""

    echo "Gathering SCM changes"
    def changeLogSets = currentBuild.changeSets
    for (int i = 0; i < changeLogSets.size(); i++) {
        def entries = changeLogSets[i].items
        for (int j = 0; j < entries.length; j++) {
            def entry = entries[j]
            truncated_msg = entry.msg.take(MAX_MSG_LEN)
            changeString += " - ${truncated_msg} [${entry.author}]\n"
        }
    }

    if (!changeString) {
        changeString = " - No new changes"
    }
    return changeString
}
def RfabricSucc()
{

    echo 'Inside Rfabric Succ!'
	stage('Final') 
    {
		 SendEmail("Success");
        
    }
}

def RfabricErr(error)
{

    echo 'Inside Rfabric Err!'+error
	stage('FinalErr') 
    {
	
		SendEmail("Failed");                           
        
    }
}


def SendEmail(status)
{
		def payload = JsonOutput.toJson(
		"application_name":"${params.Application_Name}",
		"subject":" R-Fabric Build $BUILD_NUMBER - "+ status + " (${currentBuild.fullDisplayName})",
		"body":"Changes Commited:\n " + getCommitedChanges() + "\n Check console output at: $BUILD_URL/console"
		)
                            sh "curl -D- -X POST --data \'${payload}\'  -H 'Content-Type: application/json' 'http://10.21.193.59/rfabric/jenkinsemailservice/notify' --insecure"

}

def quote() 
{
    stage('quote') 
    {
        echo 'Please check the jenkins pipeline.'
    }
}
