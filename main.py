"""
Main script for analyzing hiring bias using LLM evaluations.
"""

import pandas as pd
from config import JOB_DESCRIPTION
from utils import resume_filler, parse_response, build_prompt, call_openai
from dotenv import load_dotenv
import os
import argparse
import signal
import sys

# Define resume types
RESUMES = ["strong", "medium", "weak"]

# Global flag for graceful shutdown
shutdown_requested = False

def signal_handler(signum, frame):
    global shutdown_requested
    print("\nShutdown requested. Saving current progress...")
    shutdown_requested = True

def save_partial_results(rows, start_idx, end_idx, is_final=False):
    """Save partial or final results to CSV"""
    if not rows:
        print("No results to save yet.")
        return
    
    df = pd.DataFrame(rows)
    
    # Clean up data
    df["decision"] = df["decision"].str.upper().str.strip()
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df = df.dropna(subset=["decision", "score"])
    
    # Save results with batch info
    suffix = "_final" if is_final else "_partial"
    output_file = f"results/hiring_bias_results_{start_idx}_{end_idx-1}{suffix}.csv"
    df.to_csv(output_file, index=False)
    print(f"{'Final' if is_final else 'Partial'} results saved to {output_file} ({len(df)} evaluations)")

def main(start_idx=0, end_idx=None):
    global shutdown_requested
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    load_dotenv(override=True)  # Load environment variables from .env file

    # Load the final name combinations (assuming CSV exists from notebook)
    try:
        names_df = pd.read_csv("data/final_name_combinations.csv")
        print(f"{len(names_df)} name combinations loaded.")
    except FileNotFoundError:
        print("Error: data/final_name_combinations.csv not found. Please generate it from the notebook.")
        return

    # Apply batching
    if end_idx is None:
        end_idx = len(names_df)
    names_df = names_df.iloc[start_idx:end_idx]
    print(f"Processing names {start_idx} to {end_idx-1} ({len(names_df)} combinations)")

    rows = []
    total_combinations = len(names_df) * len(RESUMES)
    current_count = 0
    save_interval = 10  # Save every 10 evaluations
    
    try:
        for i, name_row in enumerate(names_df.itertuples(), start=start_idx):
            if shutdown_requested:
                break
                
            name = f"{name_row.first_name} {name_row.last_name}"
            print(f"Processing name {i+1}/{end_idx}: {name} (race: {name_row.race})")
            
            for resume_type in RESUMES:
                if shutdown_requested:
                    break
                    
                current_count += 1
                print(f"  [{current_count}/{total_combinations}] Resume: {resume_type}")
                
                try:
                    resume_text = resume_filler(resume_type, name_row.first_name, name_row.last_name)
                    
                    prompt = build_prompt(
                        name=name,
                        resume=resume_text,
                        job_description=JOB_DESCRIPTION
                    )
                    
                    print("    Calling LLM API...")
                    response = call_openai(prompt)
                    print("    API call completed.")
                    
                    parsed = parse_response(response)
                    
                    if parsed:
                        rows.append({
                            "name": name,
                            "race": name_row.race,
                            "gender": name_row.gender,
                            "gender_confidence": name_row.gender_confidence,
                            "resume_strength": resume_type,
                            "decision": parsed["decision"],
                            "score": parsed["score"],
                            "justification": parsed["justification"]
                        })
                        print(f"    ✓ Parsed successfully: {parsed['decision']} (score: {parsed['score']})")
                    else:
                        print("    ✗ Failed to parse response")
                        
                except Exception as e:
                    print(f"    ✗ Error processing {name} ({resume_type}): {str(e)}")
                    continue
                
                # Periodic save
                if current_count % save_interval == 0:
                    save_partial_results(rows, start_idx, end_idx, is_final=False)
    
    except Exception as e:
        print(f"\nUnexpected error during processing: {str(e)}")
    finally:
        # Always save what we have, even if interrupted
        if rows:
            save_partial_results(rows, start_idx, end_idx, is_final=not shutdown_requested)
        else:
            print("No results to save.")

    if shutdown_requested:
        print("Processing was interrupted. Partial results have been saved.")
    else:
        print(f"\nCompleted processing {len(rows)} evaluations.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze hiring bias with LLM evaluations")
    parser.add_argument("--start", type=int, default=0, help="Starting index for name combinations (0-based)")
    parser.add_argument("--end", type=int, default=None, help="Ending index for name combinations (exclusive)")
    
    args = parser.parse_args()
    main(start_idx=args.start, end_idx=args.end)
