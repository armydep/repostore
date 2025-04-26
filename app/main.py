from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from typing import Optional
import httpx
import hashlib

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to myproj 🚀"}

@app.get("/mypath")
def handle_mypath_root():
    return {"info": "You called /mypath without extra path."}

@app.get("/maven2/{full_path:path}")
async def handle_mypath(full_path: str, request: Request):
    url = f"https://repo.maven.apache.org/maven2/{full_path}"                
    print(f"Request_IN from client: {full_path}. {request.method}. fwd url: {url}")
    for header, value in request.headers.items():
        print(f"IN_Header: {header} = {value}")
    forwarded_headers = {
                    k: v for k, v in request.headers.items() if k.lower() != "host"
                }
                   
    try:
        if full_path.endswith(".pom"):
            async with httpx.AsyncClient() as client:                
                response = await client.get(url, headers = forwarded_headers)
                for header, value in response.headers.items():
                    print(f"Header from Maven: {header} = {value}")
                etagHeader = response.headers.get("etag", "")                    
                contentLegthHeader = response.headers.get("content-length", "")  
                response_headers = {   
                    k: v for k, v in response.headers.items()
                    if k.lower() != "content-length"
                }
                return Response(content=response.text, media_type="text/xml", headers=response_headers) #dict(response.headers))
        elif full_path.endswith(".xml"):
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers = forwarded_headers)
                for header, value in response.headers.items():
                    print(f"Header from Maven: {header} = {value}")
                etagHeader = response.headers.get("etag", "")                    
                contentLegthHeader = response.headers.get("content-length", "")    
                response_headers = {   
                    k: v for k, v in response.headers.items()
                    if k.lower() != "content-length"
                }                
                return Response(content=response.text, media_type="text/xml", headers=response_headers) 
        elif full_path.endswith(".sha1"):
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers = forwarded_headers)
                for header, value in response.headers.items():
                    print(f"Header from Maven for sha1: {header} = {value}")
                response_headers = {   
                    k: v for k, v in response.headers.items()
                    if k.lower() != "content-length"
                }
                return Response(content=response.text, media_type="text/plain", headers=response_headers) 
        elif full_path.endswith(".jar"): 
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers = forwarded_headers)
                for header, value in response.headers.items():
                    print(f"Header from Maven for jar: {header} = {value}")
                response_headers = {   
                    k: v for k, v in response.headers.items()
                    if k.lower() != "content-length" and not k.lower().startswith("x-")
                }                
                
                content_bytes = response.content
                md5_checksum = hashlib.md5(content_bytes).hexdigest()
                sha1_checksum = hashlib.sha1(content_bytes).hexdigest()

                response_headers["x-checksum-md5"] = md5_checksum
                response_headers["x-checksum-sha1"] = sha1_checksum

                
                for header, value in response_headers.items():
                    print(f"Header ***response*** for jar: {header} = {value}")
                return Response(content=response.content, media_type="application/java-archive", headers=response_headers) 
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}: {str(exc)}")
        return JSONResponse(status_code=502, content={"error": "Failed to fetch from url1", "details": str(exc)})
            
    print("Unknown request type. {full_path}. {request.method}")            
    return {
        "requested_subpath": full_path,
        "method": request.method,
        "info": "Request unsupported"
    }
