from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def get_stream_url(path):
    query_url = request.args.get('url')
    
    if not query_url:
        return jsonify({
            'status': 'error',
            'message': 'Please provide a url parameter. Example: ?url=https://einthusan.tv/movie/watch/...'
        }), 400

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': query_url
        }
        
        # എയിന്ത്വസൻ പേജ് ഫെച്ച് ചെയ്യുന്നു
        r = requests.get(query_url, headers=headers)
        
        if r.status_code != 200:
            return jsonify({
                'status': 'error',
                'message': f'Failed to fetch page, status code: {r.status_code}'
            }), 400

        # പേജിൽ നിന്ന് ആവശ്യമായ ഡാറ്റ എക്സ്ട്രാക്റ്റ് ചെയ്യാനുള്ള പാഴ്സിങ്
        # (മുമ്പുണ്ടായിരുന്ന ഹെറോകു ബാക്കെൻഡ് ഡൗൺ ആയതിനാൽ ഫ്ലാസ്ക് വഴി നേരിട്ട് ഹാൻഡ്ല് ചെയ്യുന്നു)
        
        return jsonify({
            'status': 'success',
            'target_url': query_url,
            'html_content_length': len(r.text),
            'message': 'Successfully connected and fetched the movie page.'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run()
