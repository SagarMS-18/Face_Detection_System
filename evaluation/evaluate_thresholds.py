import os
import sys
from pathlib import Path
import numpy as np

# Add backend directory to sys.path to import services and config directly
EVAL_DIR = Path(__file__).resolve().parent
BACKEND_DIR = EVAL_DIR.parent / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from services.face_service import load_database
from services.embedding_service import generate_face_embedding

def benchmark_thresholds():
    """
    Evaluates system performance across multiple candidate threshold values:
    [0.40, 0.45, 0.50, 0.55, 0.60]
    """
    database = load_database()
    if not database:
        print("ERROR: Database embeddings.pkl is empty or missing.")
        print("Please enroll individuals before running threshold evaluation.")
        return

    candidate_thresholds = [0.40, 0.45, 0.50, 0.55, 0.60]
    known_dir = EVAL_DIR / "known"
    unknown_dir = EVAL_DIR / "unknown"

    # Pre-extract embeddings for evaluation images to speed up threshold comparisons
    known_samples = []
    if known_dir.exists():
        for person_folder in known_dir.iterdir():
            if person_folder.is_dir():
                actual_person = person_folder.name
                for img_file in person_folder.iterdir():
                    if img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
                        emb, err = generate_face_embedding(str(img_file))
                        if not err:
                            known_samples.append((actual_person, emb, img_file.name))

    unknown_samples = []
    if unknown_dir.exists():
        for img_file in unknown_dir.iterdir():
            if img_file.is_file() and img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
                emb, err = generate_face_embedding(str(img_file))
                if not err:
                    unknown_samples.append((emb, img_file.name))

    print("==========================================================")
    print("FACE RECOGNITION THRESHOLD EVALUATION MATRIX")
    print("==========================================================")
    print(f"Total Known Test Samples   : {len(known_samples)}")
    print(f"Total Unknown Test Samples : {len(unknown_samples)}")
    print("----------------------------------------------------------\n")

    print(f"{'Threshold':<12} | {'Known Accuracy (%)':<20} | {'Unknown Rejection Rate (%)':<25}")
    print("-" * 65)

    for threshold in candidate_thresholds:
        # 1. Evaluate Known Accuracy
        known_correct = 0
        for actual_person, query_emb, _ in known_samples:
            min_dist = float('inf')
            best_person = None
            for p_name, emb_list in database.items():
                for stored_emb in emb_list:
                    dist = np.linalg.norm(query_emb - stored_emb)
                    if dist < min_dist:
                        min_dist = dist
                        best_person = p_name

            predicted = best_person if min_dist <= threshold else "Unknown"
            if predicted == actual_person:
                known_correct += 1

        known_acc = (known_correct / len(known_samples) * 100) if known_samples else 0.0

        # 2. Evaluate Unknown Rejection Rate
        unknown_correct = 0
        for query_emb, _ in unknown_samples:
            min_dist = float('inf')
            best_person = None
            for p_name, emb_list in database.items():
                for stored_emb in emb_list:
                    dist = np.linalg.norm(query_emb - stored_emb)
                    if dist < min_dist:
                        min_dist = dist
                        best_person = p_name

            predicted = best_person if min_dist <= threshold else "Unknown"
            if predicted == "Unknown":
                unknown_correct += 1

        unknown_rate = (unknown_correct / len(unknown_samples) * 100) if unknown_samples else 0.0

        print(f"{threshold:<12.2f} | {known_acc:<20.2f} | {unknown_rate:<25.2f}")

    print("----------------------------------------------------------")
    print("Recommendation: Select the threshold that balances high known accuracy")
    print("with a high unknown rejection rate for your specific dataset.")
    print("==========================================================")

if __name__ == "__main__":
    benchmark_thresholds()
