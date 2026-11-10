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
        # ഹെറോകു ഡിപെൻഡൻസി ഒഴിവാക്കി നേരിട്ടുള്ള ഹാൻഡ്ലിംഗ്
        # ഇവിടെ ഒറിജിനൽ Einthusan പേജിൽ നിന്ന് ഡാറ്റ എടുക്കാനുള്ള ലോജിക് സെറ്റ് ചെയ്യാം
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(query_url, headers=headers)
        
        # തൽക്കാലത്തേക്ക് ടെസ്റ്റ് ചെയ്യാൻ റെസ്പോൺസ് സ്റ്റാറ്റസ് റിട്ടേൺ ചെയ്യുന്നു
        return jsonify({
            'status': 'success',
            'target_url': query_url,
            'http_status': r.status_code
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run()
