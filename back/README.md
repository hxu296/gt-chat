# Back

This is the backend for the project. It is a python fastapi server that uses the LangChain + OpenAI API to generate answer for to `/qa` GET endpoint.

To run the server locally:

1. Set up python environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Set up environment variables
```
export OPENAI_API_KEY=<your key>
export SUPABASE_URL=<supabase project url>
export SUPABASE_KEY=<supabase project *service* key, not annon key>
```

3. Run Local Server
```
python main.py
```