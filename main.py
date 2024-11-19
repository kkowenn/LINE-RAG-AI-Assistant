import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from app.pinecone_utils import init_pinecone
from app.openai_utils import get_embeddings, generate_chat_response
from app.line_utils import reply_message, loading_message, get_profile

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Initialize Pinecone
pinecone_ctx = init_pinecone()

messages = {}

def init_messages(user_id):
    if user_id not in messages or not messages[user_id]:
        profile = get_profile(user_id)
        logging.info(f"Profile: {profile}")
        if 'display_name' not in profile:
            logging.error("Key 'display_name' not found in profile")
            profile['display_name'] = "Unknown User"

        messages[user_id] = [
            {"role": "system", "content": "คุณเป็นผู้ช่วยอัจฉริยะที่ออกแบบมาเพื่อตอบคำถามโดยใช้ Retrieval-Augmented Generation (RAG) วิธีการของคุณคือการประเมินข้อมูลที่ดึงมาจากฐานข้อมูลตามความเกี่ยวข้องกับคำถามของผู้ใช้ หากข้อมูลที่ดึงมามีคะแนนความเกี่ยวข้องมากกว่า 0.90 และตรงกับบริบทหรือคำหลักที่ผู้ใช้ระบุ ให้ตอบกลับด้วยรายการสินค้าที่สอดคล้องในลักษณะที่เป็นมิตร แต่หากไม่มีข้อมูลที่เกี่ยวข้อง ให้แจ้งผู้ใช้ว่ารอสักครู่เพื่อติดต่อเจ้าหน้าที่"},
            {"role": "user", "content": f"ฉันมีชื่อว่า {profile['display_name']}"},
            {"role": "assistant", "content": f"คุณชื่อ {profile['display_name']}"}
        ]

def handle_text_message(event):
    user_id = event["source"]["userId"]
    prompt = event["message"]["text"]

    init_messages(user_id)

    try:
        # Get embeddings for the incoming message
        embeddings = get_embeddings(prompt)

        # Query Pinecone for the closest matches using keyword arguments
        matches = pinecone_ctx.query(
            vector=embeddings,
            top_k=5,  # Increase top_k to get more matches
            include_metadata=True
        )

        rag_results_text = "ผลลัพธ์จาก RAG:\n"
        if matches["matches"]:
            for i, match in enumerate(matches["matches"]):
                rag_results_text += f"{i + 1}. text: {match['metadata']['text']}, score: {match['score']:.2f}\n"

        if not matches["matches"]:
            rag_results_text = "ไม่พบข้อมูลที่ตรงกับคำค้นหาของคุณ"

        response_chat = generate_chat_response(messages[user_id], prompt, rag_results_text)
        messages[user_id].append({"role": "user", "content": prompt})
        messages[user_id].append({"role": "assistant", "content": response_chat})

        reply = {"type": "text", "text": response_chat}
        reply_message(event["replyToken"], reply)
        return reply

    except Exception as e:
        # Handle errors gracefully
        error_message = f"An error occurred: {str(e)}"
        reply = {"type": "text", "text": error_message}
        reply_message(event["replyToken"], reply)
        return reply


def handle_image_message(event):
    reply = {"type": "text", "text": "hello image"}
    reply_message(event["replyToken"], reply)
    return reply

def handle_audio_message(event):
    reply = {"type": "text", "text": "hello audio"}
    reply_message(event["replyToken"], reply)
    return reply

def handle_file_message(event):
    reply = {"type": "text", "text": "hello file"}
    reply_message(event["replyToken"], reply)
    return reply

def handle_video_message(event):
    reply = {"type": "text", "text": "hello video"}
    reply_message(event["replyToken"], reply)
    return reply

def handle_location_message(event):
    reply = {"type": "text", "text": "hello location"}
    reply_message(event["replyToken"], reply)
    return reply

def handle_sticker_message(event):
    reply = {"type": "text", "text": "hello sticker"}
    reply_message(event["replyToken"], reply)
    return reply

def handle_postback_message(event):
    reply = {"type": "text", "text": "hello postback"}
    reply_message(event["replyToken"], reply)
    return reply

def handle_follow_message(event):
    reply = {"type": "text", "text": "hello follow"}
    reply_message(event["replyToken"], reply)
    return reply

def handle_unfollow_message(event):
    reply = {"type": "text", "text": "hello unfollow"}
    reply_message(event["replyToken"], reply)
    return reply

def handle_beacon_message(event):
    reply = {"type": "text", "text": "hello beacon"}
    reply_message(event["replyToken"], reply)
    return reply

handlers = {
    "text": handle_text_message,
    "image": handle_image_message,
    "audio": handle_audio_message,
    "file": handle_file_message,
    "video": handle_video_message,
    "location": handle_location_message,
    "sticker": handle_sticker_message,
    "postback": handle_postback_message,
    "follow": handle_follow_message,
    "unfollow": handle_unfollow_message,
    "beacon": handle_beacon_message,
}

@app.route("/", methods=["GET"])
def health_check():
    return "OK"

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    req = request.get_json()

    results = []
    for event in req.get("events", []):
        type_event = event["type"]
        if type_event == "message":
            type_event = event["message"]["type"]

        handler = handlers.get(type_event)
        if not handler:
            logging.warning(f"No handler found for event type: {type_event}")
            continue

        loading_message(event["source"]["userId"])
        init_messages(event["source"]["userId"])
        result = handler(event)
        results.append(result)

    return jsonify(results)

if __name__ == "__main__":
    port = os.getenv("PORT", 3001)
    app.run(host="0.0.0.0", port=int(port))
