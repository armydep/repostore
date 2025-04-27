
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