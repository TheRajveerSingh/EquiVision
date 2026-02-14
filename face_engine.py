import numpy as np
import cv2
from PIL import Image
import os
import math

# Try importing DeepFace
try:
    from deepface import DeepFace
except ImportError:
    DeepFace = None

class FaceEngine:
    def __init__(self):
        self.known_encodings = []
        self.known_ids = []
        self.model_name = "VGG-Face"

    def load_known_faces(self, events_data):
        self.known_encodings = []
        self.known_ids = []
        for evt_id, event in events_data.items():
            for person in event.get('data', []):
                if 'encoding' in person:
                    self.known_encodings.append(np.array(person['encoding']))
                    self.known_ids.append({'event_id': evt_id, 'name': person.get('name', 'Unknown')})

    def process_image(self, image_pil, detector_backend='ssd'):
        """Process a single image. Uses ONE backend only — no fallback loop."""
        if DeepFace is None:
            return []

        img_np = np.array(image_pil)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        try:
            embeddings_obj = DeepFace.represent(
                img_path=img_bgr,
                model_name=self.model_name,
                detector_backend=detector_backend,
                enforce_detection=False
            )
        except Exception as e:
            print(f"DeepFace Error ({detector_backend}): {e}")
            return []

        results = []
        H, W = img_np.shape[:2]

        for face_obj in embeddings_obj:
            if 'embedding' not in face_obj:
                continue

            embedding = face_obj['embedding']
            area = face_obj.get('facial_area', {})
            x, y, w, h = area.get('x', 0), area.get('y', 0), area.get('w', 0), area.get('h', 0)

            # Filter out full-image false positives
            if w > W * 0.9 and h > H * 0.9:
                continue

            # Skip zero-area results
            if w == 0 or h == 0:
                continue

            top, right, bottom, left = y, x + w, y + h, x

            face_data = {
                "bbox": (top, right, bottom, left),
                "encoding": embedding,
                "gender": "Unknown",
                "confidence": 0.0,
                "is_duplicate": False,
                "duplicate_info": None
            }

            # Gender Detection (on cropped face only)
            face_crop = img_bgr[y:y+h, x:x+w]
            if face_crop.size > 0:
                try:
                    analysis = DeepFace.analyze(
                        img_path=face_crop,
                        actions=['gender'],
                        detector_backend='skip',
                        enforce_detection=False,
                        silent=True
                    )
                    if isinstance(analysis, list):
                        analysis = analysis[0]
                    g_res = analysis['dominant_gender']
                    if g_res == "Man": g_res = "Male"
                    if g_res == "Woman": g_res = "Female"
                    face_data["gender"] = g_res
                    face_data["confidence"] = analysis['gender'][analysis['dominant_gender']]
                except:
                    face_data["gender"] = "Unknown"

            # De-duplication (Cosine Similarity)
            if self.known_encodings:
                current_vec = np.array(embedding)
                for idx, known_vec in enumerate(self.known_encodings):
                    dot = np.dot(known_vec, current_vec)
                    norm_a = np.linalg.norm(known_vec)
                    norm_b = np.linalg.norm(current_vec)
                    if norm_a == 0 or norm_b == 0:
                        continue
                    cosine_similarity = dot / (norm_a * norm_b)
                    if cosine_similarity > 0.60:
                        face_data["is_duplicate"] = True
                        face_data["duplicate_info"] = self.known_ids[idx]
                        break

            results.append(face_data)

        return results


def draw_results(image_pil, results):
    """Draw bounding boxes and labels on the image."""
    img_cv = np.array(image_pil)
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)

    for res in results:
        if "error" in res:
            continue
        top, right, bottom, left = res['bbox']
        color = (0, 255, 0)
        label = res['gender']
        if res['is_duplicate']:
            color = (0, 0, 255)
            label += " (DUPLICATE)"
        cv2.rectangle(img_cv, (left, top), (right, bottom), color, 2)
        cv2.putText(img_cv, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
