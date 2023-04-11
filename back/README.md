# Back

The backend for the project is a python fastapi server that uses the LangChain + OpenAI API to generate answer for to `/qa` GET endpoint.

__Deployment__

Change the Railway build command to `bash build.sh` and it should work out of the box.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/FZffm_?referralCode=wOsORh)

__To run the server locally:__

Step 1: Set up python environment and fetch OpenAI embeddings
```
python3 -m venv venv
bash build.sh
```

Step 2: Set up environment variables
```
export OPENAI_API_KEY=<your key>
export SUPABASE_URL=<supabase project url>
export SUPABASE_KEY=<supabase project *service* key, not annon key>
```

Step 3: Run Local Server
```
python main.py
```

## Contributing

Pull requests are always welcomed!