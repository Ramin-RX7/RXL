
# Check For Oustide of the Quotations (And other brackets)
"""
import re
Text = ''' "int open(const char *" pathname ", int " flags );'''
matches = re.finditer(r'".*?"|(\w+)', Text)
for match in matches:
    print(match.group(1))
    #if match.group(1):
        #print(f"Found at {match.start(1)}-{match.end(1)}: {match.group(1)}")
"""
