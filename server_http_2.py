from quart import Quart, send_file
import os

app = Quart(__name__)

@app.route('/<path:filename>')
async def send_file(filename):
    return await send_file(os.path.join('Data', filename))

if __name__ == "__main__":
    import hypercorn.asyncio
    import hypercorn.config

    config = hypercorn.config.Config.from_mapping(bind=["0.0.0.0:8000"], h2=True)
    hypercorn.asyncio.serve(app, config)
