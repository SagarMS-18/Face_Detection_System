import os
import sys
from pathlib import Path
import numpy as np

# Add backend directory to sys.path to import services and config directly
EVAL_DIR = Path(__file__).resolve().parent
BACKEND_DIR = EVAL_DIR.parent / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from config import FACE_MATCH_THRESHOLD
from services.face_service import load_database
from services.embedding_service import generate_face_embedding

def evaluate_system(threshold=FACE_MATCH_THRESHOLD):
    """
    Evaluates the face recognition system against known and unknown test images.
    """
    database = load_database()
    if not database:
        print("ERROR: Database embeddings.pkl is empty or missing.")
        print("Please enroll at least one person before running evaluation.")
        return

    known_dir = EVAL_DIR / "known"
    unknown_dir = EVAL_DIR / "unknown"

    print("==================================================")
    print(f"FACE RECOGNITION SYSTEM EVALUATION (Threshold: {threshold})")
    print("==================================================\n")

    # ----------------------------------------------------
    # 1. EVALUATE KNOWN PERSON IMAGES
    # ----------------------------------------------------
    print("--- 1. Known Person Evaluation ---")
    print(f"{'Image':<30} | {'Actual Person':<15} | {'Predicted':<15} | {'Distance':<10} | {'Result'}")
    print("-" * 85)

    known_total = 0
    known_correct = 0

    if known_dir.exists():
        for person_folder in known_dir.iterdir():
            if person_folder.is_dir():
                actual_person = person_folder.name
                for img_file in person_folder.iterdir():
                    if img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
                        known_total += 1
                        query_emb, err = generate_face_embedding(str(img_file))

                        if err:
                            print(f"{img_file.name:<30} | {actual_person:<15} | {'ERROR':<15} | {'N/A':<10} | {err}")
                            continue

                        # Compare against stored embeddings
                        best_person = None
                        min_dist = float('inf')

                        for p_name, emb_list in database.items():
                            for stored_emb in emb_list:
                                dist = np.linalg.norm(query_emb - stored_emb)
                                if dist < min_dist:
                                    min_dist = dist
                                    best_person = p_name

                        if min_dist <= threshold:
                            predicted = best_person
                        else:
                            predicted = "Unknown"

                        is_correct = (predicted == actual_person)
                        if is_correct:
                            known_correct += 1

                        status_str = "PASS" if is_correct else "FAIL"
                        print(f"{img_file.name:<30} | {actual_person:<15} | {predicted:<15} | {min_dist:<10.4f} | {status_str}")

    known_acc = (known_correct / known_total * 100) if known_total > 0 else 0.0

    print("\nKnown Face Evaluation Summary:")
    print(f"Correct: {known_correct}/{known_total}")
    print(f"Known-Person Accuracy: {known_acc:.2f}%\n")

    # ----------------------------------------------------
    # 2. EVALUATE UNKNOWN PERSON IMAGES
    # ----------------------------------------------------
    print("--- 2. Unknown Person Evaluation ---")
    print(f"{'Image':<30} | {'Actual Person':<15} | {'Predicted':<15} | {'Distance':<10} | {'Result'}")
    print("-" * 85)

    unknown_total = 0
    unknown_correct = 0

    if unknown_dir.exists():
        for img_file in unknown_dir.iterdir():
            if img_file.is_file() and img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
                unknown_total += 1
                query_emb, err = generate_face_embedding(str(img_file))

                if err:
                    print(f"{img_file.name:<30} | {'Unknown':<15} | {'ERROR':<15} | {'N/A':<10} | {err}")
                    continue

                best_person = None
                min_dist = float('inf')

                for p_name, emb_list in database.items():
                    for stored_emb in emb_list:
                        dist = np.linalg.norm(query_emb - stored_emb)
                        if dist < min_dist:
                            min_dist = dist
                            best_person = p_name

                if min_dist <= threshold:
                    predicted = best_person
                else:
                    predicted = "Unknown"

                # For unknown test images, correct prediction is "Unknown"
                is_correct = (predicted == "Unknown")
                if is_correct:
                    unknown_correct += 1

                status_str = "PASS (Rejected)" if is_correct else "FAIL (False Match)"
                print(f"{img_file.name:<30} | {'Unknown':<15} | {predicted:<15} | {min_dist:<10.4f} | {status_str}")

    unknown_rate = (unknown_correct / unknown_total * 100) if unknown_total > 0 else 0.0

    print("\nUnknown Face Evaluation Summary:")
    print(f"Correctly Rejected: {unknown_correct}/{unknown_total}")
    print(f"Unknown Rejection Rate: {unknown_rate:.2f}%\n")

    print("==================================================")
    print("FINAL SUMMARY RESULTS")
    print("==================================================")
    print(f"Known-person accuracy  : {known_acc:.2f}% ({known_correct}/{known_total})")
    print(f"Unknown rejection rate : {unknown_rate:.2f}% ({unknown_correct}/{unknown_total})")
    print("==================================================")

if __name__ == "__main__":
    evaluate_system()
