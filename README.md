# galactacto

Local helper scripts and frontend to run the Galactactocus LiveKit agent with a custom browser client.

## Prerequisites
- Python 3.11+
- Node not required (frontend served as vanilla static assets)
- Populate `AGENT/keys.env` with your LiveKit/OpenAI/Bey credentials
- Install Python dependencies: `pip install -r requirements.txt`

## Running the agent
1. `cd AGENT`
2. `python main.py`
   - The agent connects to the room specified by the LiveKit CLI when you start it.

## Serving the frontend + token endpoint
1. In a separate terminal: `cd AGENT`
2. `python token_server.py --port 8080`
   - Serves static frontend files from `../frontend`
   - Provides `/token?identity=<name>&room=<room>` for LiveKit access tokens

## Using the browser client
1. Open `http://localhost:8080` in your browser
2. Enter the room name the agent will join (defaults to `galactactocus-room`)
3. Choose a display name and click **Connect**
4. Type messages in the chat pane; the agent replies using the Bey avatar video stream

## Troubleshooting
- Ensure the agent process is running and has joined the same room as your browser client
- The token server prints helpful logs — check them if token requests fail
- If your browser cannot connect, verify that the LiveKit credentials in `keys.env` are valid and have matching project/tenant access
