import re
import os
import pandas as pd 

def modify_parameters(input_path, output_path, custom_probs):
    istate_pattern = re.compile(r"^\[(\w+)\]\.istate\s*=\s*([\d\.]+)\s*\[0\]\s*,\s*([\d\.]+)\s*\[1\];")
    updated_lines = []

    with open(input_path, "r") as infile:
        for line in infile:
            match = istate_pattern.match(line)
            if match:
                node = match.group(1)

                if node in custom_probs:
                    p_off = float(match.group(2))
                    p_on = float(match.group(3))
                    value = custom_probs[node]
                    if isinstance(value, dict) and "factor" in value:
                        factor = value["factor"]
                        p_on *= factor
                        p_off = 1 - p_on 
                    else:
                        p_off = float(match.group(2))
                        p_on = float(match.group(2))
                        p_off, p_on = value  # Direct set

                    new_line = f"[{node}].istate = {p_off:.4f} [0] , {p_on:.4f} [1];\n"
                    updated_lines.append(new_line)
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)

    with open(output_path, "w") as outfile:
        outfile.writelines(updated_lines)