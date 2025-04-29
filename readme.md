
1. **Setup Project**:

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  uvicorn app.main:app --reload --port 8080
  ```

2. **Maven Settings**:

  Path: `.m2/settings.xml`

  ```xml
  <settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 https://maven.apache.org/xsd/settings-1.0.0.xsd">
    
    <mirrors>
     <mirror>
      <id>central-proxy</id>
      <name>Local proxy of central repo</name>
      <url>http://localhost:8000/maven2</url>
      <mirrorOf>central</mirrorOf>
     </mirror>
    </mirrors>
  </settings>
  ```

3. **Reverse Proxy with mitmproxy**:

  ```bash
  mitmweb --mode reverse:https://repo.maven.apache.org --listen-host 127.0.0.1 --listen-port 8000
  ```

4. **Alternative Maven Settings**:

  Path: `.m2/settings.xml`

  ```xml
  <settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 https://maven.apache.org/xsd/settings-1.0.0.xsd">
    
    <!-- Uncomment the proxies section if needed -->
    <!--
    <proxies>
     <proxy>
      <id>mitmproxy</id>
      <active>true</active>
      <protocol>http</protocol>
      <host>127.0.0.1</host>
      <port>8888</port>
     </proxy>
    </proxies>
    -->

    <mirrors>
     <mirror>
      <id>central-proxy</id>
      <name>Local proxy of central repo</name>
      <url>http://localhost:8000/maven2</url>
      <mirrorOf>central</mirrorOf>
     </mirror>
    </mirrors>
  </settings>
  ```

5. **Reverse Proxy Command**:

  ```bash
  mitmweb --mode reverse:https://repo.maven.apache.org --listen-host 127.0.0.1 --listen-port 8000
  ```

6. **Maven**
  - resolve 
  ```bash 
  mvn dependency:resolve
  ```
  - package
  ```bash
  mvn package
  ```
  - install
  ```bash
  mvn install
  ```

7. **Test**  
  - pom.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>org.example</groupId>
    <artifactId>JServer</artifactId>
    <version>1.0-SNAPSHOT</version>
    <dependencies>
        <dependency>
            <groupId>org.apache.logging.log4j</groupId>
            <artifactId>log4j-core</artifactId>
            <version>2.10.0</version>
        </dependency>
    </dependencies>
</project>
```
  - run
```bash
rm -rf ~/.m2/repository/org/apache/logging/log4j/log4j-core/2.10.0
mvn dependency:resolve
```
  - compare
 ```bash
  curl http://localhost:8000/maven2/org/apache/logging/log4j/log4j-core/2.10.0/log4j-core-2.10.0.pom
  curl -I http://localhost:8000/maven2/org/apache/logging/log4j/log4j-core/2.10.0/log4j-core-2.10.0.pom
  curl -I https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-core/2.10.0/log4j-core-2.10.0.pom
  curl -I http://localhost:8000/maven2/org/apache/logging/log4j/log4j-core/2.10.0/log4j-core-2.10.0.pom -o remote.txt
  curl -I https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-core/2.10.0/log4j-core-2.10.0.pom -o remote.txt
  sdiff <(sort local.txt) <(sort remote.txt)
```
8. **Generate package**
  - generate
  ```bash
  mvn archetype:generate -DgroupId=com.test.dummy -DartifactId=dummy-artifact -Dversion=1.0.3 -Dpackage=com.test.dummy -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
  ```
  - update pom. add
  ```xml
<properties>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
  </properties>
  <distributionManagement>
    <repository>
        <id>my-repo</id>
	<url>http://localhost:8000/maven2/</url>
    </repository>
  </distributionManagement>
  ```
  - package. 
  ```bash
  cd <package dir>
  mvn package
  ```
9. **Deploy package**
- deploy
```bash
mvn deploy
```
- curl
```bash
curl -X PUT "http://localhost:8000/repostore/maven-local/com/test/dummy/dummy-artifact/1.0.4/dummy-artifact-1.0.4.jar"      -H "Content-Type: application/java-archive"      --data-binary target/dummy-artifact-1.0.4.jar
```

10. **TODO**
- In case of HEAD request return only headers. for both cacheservice and remote service
- Check if better to store headers as well in separated file
- bug: returning 200 for Head request when actually not found returned by the remote
  ```bash
  curl http://localhost:8000/virtual/maven-virtual-1/org/apache/logging/log4j/log4j-core/2.999.0/log4j-core-2.999.0.pom
  ```