# NeoNASAChallenge

Dashboard per esplorare asteroidi vicini alla Terra usando dati NASA.

## Stack
- Backend: Python + FastAPI
- Frontend: Next.js (App Router)
- Data source: NASA APIs (`https://api.nasa.gov/`)

# activate virtual environment
go to --> apps/api
run in the bash --> source .venv/Scripts/activate

to check if it is active --> which python 
if path ends with --> apps/api/.venv/Scripts/python --> then the venv is active
As long as the output points to a path inside your project's .venv directory

to deactivate it, run in the bash --> deactivate

## Remember

- in /apps/payloads, files payload_success.json, payload_large.json and payload_error.json were produced through the script save_payloads.py in apps/api/test_scripts
- payload_success.json and payload_large.json are the same since the maximum date range is 7 days (this before to implement something that handle a bigger date range)
- payload_error.json
- payload_empty.json and payload_weird_case.json were produced by modifying the payload_success.json file manually
- payload_weird.json can also be produced by calling the API with different filters until you find an unusal response through:
    Very old dates
    Future dates
    Rare categories
    Boundary values
    Different regions/languages
    Missing optional parameters

## process to create good schemas

- saved payloads JSON responses in /apps/payloads
- Inspect JSON through VSCode or jq in command line
- Create a table of observations among data:

    Top-level jeys --> jq "keys" filename.json
    Root Type --> Object {...} or list [...] --> Depending on wether it is one on the other, create 2 different Pydantic schemas (examples):
                                                  if JSON --> {
                                                                "count": 2,
                                                                "results": [
                                                                  {
                                                                    "id": "1",
                                                                    "name": "Asteroid A"
                                                                  },
                                                                  {
                                                                    "id": "2",
                                                                    "name": "Asteroid B"
                                                                  }
                                                                ]
                                                              }
                                                  then it is an
                                                  Object
                                                  and in Pydantic you usually use:
                                                                                    class Asteroid(BaseModel):
                                                                                      id: str
                                                                                      name: str
                                                                                    
                                                                                    class ApiResponse(BaseModel):
                                                                                      count: int
                                                                                      results: list[Asteroids]
                                                  if JSON is --> [
                                                                    {
                                                                      "id": "1",
                                                                      "name": "Asteroid A"
                                                                    },
                                                                    {
                                                                      "id": "2",
                                                                      "name": "Asteroid B"
                                                                    }
                                                                  ]
                                                  then it is a 
                                                  list 
                                                  and in Pydantic you usually use:
                                                                                    class Asteroid(BaseModel):
                                                                                        id: str
                                                                                        name: str
                                                  and you validate the whole list:
                                                                                    class AsteroidList(RootModel[list[Asteroid]]):
                                                                                      pass
    Main useful section --> usually data, results, items, etc.
    Metadata --> Pagination, links, count, status
    Error structure --> error, message, code --> done exploring payload_error.json

- Identify Data your app actually need and classify every important Field in a "field-analysis table"
- 

## Struttura progetto

```text
apps/
  api/
    main.py
    requirements.txt
    .env.example
    .env
  web/
    nasa-asteroids-explorer/



