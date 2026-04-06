import pandas as pd
import ast
import matplotlib.pyplot as plt
from collections import Counter

# Load data
data = pd.read_csv('open_world_Ego4D.csv')['scenarios'].dropna().tolist()
data = [ast.literal_eval(d) for d in data]

new_data = []
for domain_list in data:
    is_append = True
    for domain in domain_list:
        if domain == 'Cooking':
            is_append = False
            break
    if is_append:
        new_data.append(domain_list)

data = new_data

data = [domain for domain_list in data for domain in domain_list]

new_data = []
for domain in data:
    if 'Crafting/knitting' in domain:
        new_data.append('Crafting/knitting')
    elif 'jobs related to construction' in domain:
        new_data.append('Construction/Renovation')
    elif 'Household management' in domain:
        new_data.append('Household management')
    else:
        new_data.append(domain)

data = new_data

# # Count the frequency of each domain
# domain_counts = Counter(data)

# # Sort the domain counts by frequency and keep top 20
# sorted_domain_counts = {k: v for k, v in sorted(domain_counts.items(), key=lambda item: item[1], reverse=True)[:10]}

# # Separate the domains and their respective counts
# domains, counts = zip(*sorted_domain_counts.items())

# # Reverse the order to have the largest at the top
# domains = domains[::-1]
# counts = counts[::-1]

# # Create a horizontal bar chart for the top 20 domains
# plt.figure(figsize=(10, 6))
# plt.barh(domains, counts, color='skyblue')

# # plt.ylabel('Domains')
# # plt.xlabel('Number of Videos')
# # plt.title('Top 10 Open-world Domains Frequency')

# plt.yticks(rotation=45)  # Tilt the y-axis labels for better readability

# # Adjust layout to fit all domain names
# plt.tight_layout()

# # Save the histogram
# plt.savefig('domain_open_world.png', dpi=300)

# # Show the plot
# plt.show()


# Count the frequency of each domain
domain_counts = Counter(data)

print(len(domain_counts.keys()))

# Sort the domain counts by frequency and keep top 10
sorted_domain_counts = {k: v for k, v in sorted(domain_counts.items(), key=lambda item: item[1], reverse=True)[:10]}

# Separate the domains and their respective counts
domains, counts = zip(*sorted_domain_counts.items())

# Reverse the order to have the largest at the top
domains = domains[::-1]
counts = counts[::-1]

# Create a horizontal bar chart for the top 10 domains
plt.figure(figsize=(12, 8))  # Adjusted figure size for better clarity
bars = plt.barh(domains, counts, color='#6A5ACD')  # Professional color

# Enhance readability and aesthetics
plt.xlabel('Number of Videos', fontsize=18, labelpad=20, fontweight='bold')
# plt.title('Top 10 Open-world Domains (Excluding Cooking)', fontsize=16, fontweight='bold', pad=30)
plt.xticks(fontsize=18)
plt.yticks(rotation=45, fontsize=18, fontweight='bold')  # Adjust y-axis labels

# Calculate the maximum width of the bars (i.e., the maximum count)
max_width = max(counts)

# Set the x-axis limit to be slightly more than the maximum width
plt.xlim(0, max_width + max_width * 0.1)  # Add 10% more for padding

# Optional: Add data annotations on each bar
for bar in bars:
    plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, 
             f' {int(bar.get_width())}', va='center', ha='left', fontsize=18, fontweight='bold')

plt.tight_layout()  # Adjust layout

# Save the histogram
plt.savefig('domain_open_world_10.pdf', format='pdf', dpi=300)