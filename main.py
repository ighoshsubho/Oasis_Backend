import os
from fastapi import FastAPI, HTTPException, status, Request, Response
from fastapi_redis_cache import FastApiRedisCache, cache, cache_one_day
from helpers import scrapeGitHub, scrapeLeetCode
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = FastAPI(
    title="Jobs API",
    description="An API that helps you fetch GitHub data with ease for your next big project.",
    version="6",
    contact={
        "name": "Oasis",
        "url": "https://github.com/Oasis-Got-Fired-Get-Hired",
    },
    license_info={
        "name": " MIT license",
    },
)

LOCAL_REDIS_URL = f"{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}"

@app.on_event("startup")
def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=os.environ.get("REDIS_URL", LOCAL_REDIS_URL),
        prefix="jobsapi-cache",
        response_header="X-JobsAPI-Cache",
        ignore_arg_types=[Request, Response]
    )

# Root endpoint
@app.get("/")
@cache_one_day()
async def read_root(request: Request, response: Response):
    return {
        "title": "Jobs API",
        "description": "An API that helps you fetch GitHub data with ease for your next big project.",
        "version": "3",
        "contact": {
            "name": "Oasis",
            "url": "https://github.com/Oasis-Got-Fired-Get-Hired",
        },
        "license_info": {
            "name": " MIT license",
        },
        "endpoints": {
            "api/github/username": "Stats of a GitHub user",
            "api/leetcode/username": "Stats of a LeetCode user",
        },
    }

# Endpoint to get GitHub data
@app.get("/api/github/{username}")
@cache(expire=10)
async def github(username:str, request: Request, response: Response):
    try:
        data = scrapeGitHub.scrapr_github_data(username)
        return {
            "Name": data["Name"],
            "Bio": data["Bio"],
            "Followers": data["Followers"],
            "Repositories": data["Repositories"],
            "Contributions": data["Contributions"],
            "Orgs" : data["Orgs"]
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {username} not found",
        )

# Endpoint to get GitHub data
@app.get("/api/leetcode/{username}")
@cache(expire=10)
async def leetcode(username:str, request: Request, response: Response):
    try:
        data = scrapeLeetCode.scrape_leetcode_data(username)
        return {
            'Views': data['views'],
            'Solutions': data['solutions'],
            'Discussions': data['discussions'],
            'Reputation': data['reputation'],
            'Languages': data['languages'],
            'Skills':data['skills'],
            'Problems solved':data['problems solved'],
            'Contribution count':data['contribution count'],
            'Badges':data['badges']
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {username} not found",
        )