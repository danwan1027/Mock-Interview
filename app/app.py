from flask import Flask, jsonify, redirect
import router.router as router
True
app = Flask(__name__)
router.init_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5001)