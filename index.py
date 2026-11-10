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
            'Referer': query_url,
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        # എയിന്ത്വസൻ പേജ് ഫെച്ച് ചെയ്യുന്നു (AJAX ഹെഡറோடு കൂടി)
        r = requests.get(query_url, headers=headers)
        
        if r.status_code != 200:
            return jsonify({
                'status': 'error',
                'message': f'Failed to fetch page, status code: {r.status_code}'
            }), 400

        html_text = r.text

        # വീഡിയോ ലിങ്ക് എക്സ്ട്രാക്റ്റ് ചെയ്യാനുള്ള റെജുക്സ് പാറ്റേൺ
        # (mp4 അല്ലെങ്കിൽ സ്ട്രീമിംഗ് ലിങ്കുകൾ കണ്ടെത്താൻ)
        url_match = re.search(r'https?://[^\s<>"]+?\.mp4[^\s<>"]*', html_text)
        
        stream_url = url_match.group(0) if url_match else None

        # ഒരുപക്ഷേ JSON റെസ്പോൺസ് ആണെങ്കിൽ അത് പാഴ്സ് ചെയ്യുന്നു
        try:
            json_data = r.json()
            if 'info' in json_data and 'formats' in json_data['info']:
                stream_url = json_data['info']['formats'][0]['url']
        except:
            pass

        if stream_url:
            return jsonify({
                'status': 'success',
                'target_url': query_url,
                'stream_url': stream_url
            })
        else:
            return jsonify({
                'status': 'success',
                'target_url': query_url,
                'html_length': len(html_text),
                'message': 'Page fetched, but stream URL pattern needs adjustment.'
            })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run()
