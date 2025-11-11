import gemini_api
import requests
from flask import Flask, request, jsonify, make_response
class SuggestionProcessor:
    def __init__(self, userstory_raw=None, srs_raw=None):
        self.gemini_client1 = gemini_api.GeminiClient(task='userstory')
        self.gemini_client2 = gemini_api.GeminiClient(task='srs')
        self.gemini_client3 = gemini_api.GeminiClient(task='fusion1')
        self.gemini_client4 = gemini_api.GeminiClient(task='fusion2')
        self.gemini_client5 = gemini_api.GeminiClient(task='total')
        self.gemini_client6 = gemini_api.GeminiClient(task='general')
        self.gemini_client7 = gemini_api.GeminiClient(task='suggest')
        self.useerstory_raw = userstory_raw
        self.srs_raw = srs_raw
    def process(self):
        #state 1
        list_requirement = self.gemini_client1.generate_text(self.useerstory_raw)
        list_srs = self.gemini_client2.generate_text(self.srs_raw)

        #stage 2
        gemini_fusion1 = self.gemini_client3.generate_text(
            f'Here is the user story: {list_requirement} Here is the SRS: {list_srs}'
        )
        gemini_fusion2 = self.gemini_client4.generate_text(
            f'Here is the user story: {list_requirement} Here is the SRS: {list_srs}'
        )


        #stage 3
        total_cucbo = self.gemini_client5.generate_text(
            f'Here is fusion1: {gemini_fusion1} Here is fusion2: {gemini_fusion2} Here is the user story: {list_requirement} Here is the SRS: {list_srs}'
        )

        #stage 4
        general = self.gemini_client6.generate_text(
            f'Here is the user story: {list_requirement} Here is the SRS: {list_srs} Here is the total summary: {total_cucbo}'
        )


        #stage 5
        final = self.gemini_client7.generate_text(
            f'Here is the local information {total_cucbo} Here is the global information including raw user story and srs: {general}'
        )
        return final #danh sach cac de xuat
class UserInteractionHandler:
    def __init__(self, userpromt, final_suggestions, srs_raw):
        self.userpromt = userpromt
        self.final_suggestions = final_suggestions
        self.gemini_client = gemini_api.GeminiClient(task='processing')
        self.srs_raw = srs_raw

    def process(self):
        response = self.gemini_client.generate_text(
            f'Here are the final suggestions: {self.final_suggestions} Here is the user prompt: {self.userpromt} Here is the data you need to modify: {self.srs_raw}'
        )
        return response

class UITranslate:
    def __init__(self, text):
        self.text = text
        self.gemini_client = gemini_api.GeminiClient(task='translate')
    def process(self):
        translated_text = self.gemini_client.generate_text(
            f'Here is the raw data you need to process: {self.text}'
        )
        return translated_text

from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return "Chào bạn, API server đang chạy. Hãy sử dụng endpoint '/process_suggestions' hoặc '/handle_interaction'."

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

# --- Endpoint 1: Chạy SuggestionProcessor ---
@app.route("/process_suggestions", methods=['POST', 'OPTIONS'])
def process_suggestions_api():
    """
    API endpoint để xử lý user story và srs để đưa ra gợi ý.
    Nhận vào JSON: {"userstory_raw": "...", "srs_raw": "..."}
    Trả về JSON: {"suggestions": "..."}
    """
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    print("Processing suggestions...")
    try:
        
        data = request.get_json()
        print(data)
        if not data or 'userstory_raw' not in data or 'srs_raw' not in data:
            return jsonify({"error": "Dữ liệu đầu vào không hợp lệ. Cần 'userstory_raw' và 'srs_raw'."}), 400
        # print("Processing suggestions...")
        userstory_raw = data['userstory_raw']
        srs_raw = data['srs_raw']

        # 1. Khởi tạo processor với dữ liệu từ request
        processor = SuggestionProcessor(userstory_raw=userstory_raw, srs_raw=srs_raw)
        
        # 2. Gọi hàm process

        final_suggestions = processor.process()

        # 3. Trả về kết quả
        return jsonify({"suggestions": final_suggestions}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Endpoint 2: Chạy UserInteractionHandler ---
@app.route("/handle_interaction", methods=['POST', 'OPTIONS'])
def handle_interaction_api():
    """
    API endpoint để xử lý tương tác của người dùng dựa trên gợi ý.
    Nhận vào JSON: {"userpromt": "...", "final_suggestions": "...", "srs_raw": "..."}
    Trả về JSON: {"response": "..."}
    """
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    try:
        data = request.get_json()
        if not data or 'userpromt' not in data or 'final_suggestions' not in data or 'srs_raw' not in data:
            return jsonify({"error": "Dữ liệu đầu vào không hợp lệ. Cần 'userpromt', 'final_suggestions', và 'srs_raw'."}), 400

        userpromt = data['userpromt']
        final_suggestions = data['final_suggestions']
        srs_raw = data['srs_raw']

        # 1. Khởi tạo handler
        handler = UserInteractionHandler(userpromt, final_suggestions, srs_raw)
        
        # 2. Gọi hàm process
        response = handler.process()
        handler2 = UITranslate(response)
        response = handler2.process()

        # 3. Trả về kết quả
        return jsonify({"response": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/handle_translate", methods=['POST', 'OPTIONS'])
def handle_translate():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response() 
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Dữ liệu đầu vào không hợp lệ. Cần 'text'"}), 400

        text = data['text']

        handler = UITranslate(text)
        
        response = handler.process()
        
        return jsonify({"response": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)