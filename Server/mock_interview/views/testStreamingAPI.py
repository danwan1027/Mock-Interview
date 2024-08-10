from flask import Blueprint, render_template, Response,jsonify, request

testStreamingAPI = Blueprint('testStreamingAPI', __name__)

@testStreamingAPI.route('/testStreamingAPI')
def test():
    return render_template('testStreamingAPI.html')