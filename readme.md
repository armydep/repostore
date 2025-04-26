

1. maven settings
path: .m2/settings.xml
'''
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 https://maven.apache.org/xsd/settings-1.0.0.xsd">
  
  <!--proxies>
    <proxy>
      <id>mitmproxy</id>
      <active>true</active>
      <protocol>http</protocol>
      <host>127.0.0.1</host>
      <port>8888</port>
    </proxy>
  </proxies-->

  <mirrors>
    <mirror>
      <id>central-proxy</id>
      <name>Local proxy of central repo</name>
      <!--url>http://localhost:9999/maven2</url-->
      <url>http://localhost:8000/maven2</url>
	  <mirrorOf>central</mirrorOf>
    </mirror>
  </mirrors>

</settings>
'''
2. reversee
3. mitmproxy:
    '''mitmweb --mode reverse:https://repo.maven.apache.org --listen-host 127.0.0.1 --listen-port 8000'''