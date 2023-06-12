from fastapi import FastAPI, HTTPException
import uvicorn
import sys
from schemas import SearchBody
from search_repository import SearchRepository

app = FastAPI(
    title="File analyser API"
)


@app.post("/search", status_code=201)
async def create_search(body: SearchBody):
    if len(sys.argv) > 1:
        search_id = await SearchRepository.search_files(sys.argv[1], **body.dict())
        return {"search_id": search_id}
    else:
        print(len(sys.argv))
        raise HTTPException(
            status_code=523, detail="Specify directory! - 'python main.py directory_name'")


@app.get("/searches/{search_id}")
async def get_search_result(search_id: str):
    try:
        search_result = await SearchRepository.get_search_result(search_id)
        response = {"finished": search_result[0]}
        if search_result[0]:
            response["paths"] = search_result[1]
        return response

    except ValueError:
        raise HTTPException(
            404, detail=f"No record with id {search_id} in history!")
    except:
        raise HTTPException(500)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, log_level="info", reload=True)
