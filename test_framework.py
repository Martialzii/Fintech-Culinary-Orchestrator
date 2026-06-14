# TARGET TEST FRAMEWORK (DELIBERATELY BROKEN)
import sys

def compute_system_average(data_matrix):
    print("[*] Processing telemetry data matrix...")
    # INTENTIONAL BUG: Throws a ZeroDivisionError because items count is zero
    items_count = len(data_matrix)
    total_sum = sum(data_matrix)
    
    system_average = total_sum / items_count
    return system_average

if __name__ == "__main__":
    # Passing an empty list to trigger the crash sequence
    raw_telemetry = []
    result = compute_system_average(raw_telemetry)
    print(f"[+] Operational Metrics Average: {result}")
