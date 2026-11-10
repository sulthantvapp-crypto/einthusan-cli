from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def get_stream_url(path):
    query_url = request.args.get('url')
    
    if not query_url:
        return jsonify({
            'status': 'error',
            'message': 'Please provide a url parameter. Example: ?url=your_einthusan_movie_link'
        }), 400

    try:
        # ഒറിജിനൽ എൻഡ്പോയിന്റ് റിക്വസ്റ്റ്
        api_url = 'https://einthusan-cli.herokuapp.com/api/info?url=' + query_url
        response = requests.get(api_url).json()
        
        stream_url = response['info']['formats'][0]['url']
        
        return jsonify({
            'status': 'success',
            'url': stream_url
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run()
