import os
from flask import Flask
import router.router as router

app = Flask(__name__)
router.init_routes(app)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5001))
    debug = os.getenv("DEBUG", "False") == "True"
    app.run(host='0.0.0.0', port=port, debug=debug)
